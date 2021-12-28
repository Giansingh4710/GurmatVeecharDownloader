from flask import Flask, redirect, url_for, render_template, send_file, request,send_from_directory
import requests
from io import BytesIO
from downloadGurmatVechar import enterUrl

app=Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/index", methods=["POST","GET"])
def index():
    # print(request.method)
    if request.method=="POST":
        theLink=request.form["link"]
        theLink=theLink.replace("/","   ")
        print("The Link: "+str(theLink))
        return redirect(url_for("download_file", theLINK=theLink))
    else:    
        return render_template("index.html")

@app.route("/download/<theLINK>")
def download_file(theLINK):
    theLINK=theLINK.replace("   ","/")

    zipPath=enterUrl(theLINK)
    if zipPath==False:
        return "<h1>Not good link</h1>"
    return send_file(zipPath,download_name=zipPath, as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)