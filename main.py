from flask import Flask, redirect, url_for, render_template, send_file, request,send_from_directory
from downloadGurmatVechar import enterUrl , deleteAllAudios
import os
app=Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/index", methods=["POST","GET"])
def index():
    if request.method=="POST":
        theLink=request.form["link"]
        theLink=theLink.replace("/","   ")
        return redirect(url_for("download_file", theLINK=theLink))
    else:    
        return render_template("index.html",cwd=str(os.getcwd()),lst=str(os.listdir()))

id=0
@app.route("/download/<theLINK>")
def download_file(theLINK):
    removeAllZips()
    global id
    id+=1
    theLINK=theLINK.replace("   ","/")

    linkSplitLst=theLINK.split('%2F')
    if len(linkSplitLst)==1:
        linkSplitLst=theLINK.split('/')
    dirName=linkSplitLst[-1].lower()+str(id) #using id to aviod collisions if same link files are being downloaded
    print(os.getcwd())
    os.chdir("./audios")
    os.mkdir(dirName)
    os.chdir("../")
    zipPath=dirName+".zip"

    res=enterUrl(theLINK,dirName)
    deleteAllAudios("audios/"+dirName)
    if res!=True:
        return f"<h1>{res}</h1>"
    
    return send_file(zipPath,download_name=zipPath, as_attachment=True)



def removeAllZips():
    for thing in os.listdir("./"):
        if ".zip" in thing:
            os.remove(thing)
if __name__=="__main__":
    app.run(debug=True)
    # app.run()