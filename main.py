from flask import Flask, redirect, url_for, render_template, send_file, request,send_from_directory
import requests
from io import BytesIO
from downloadGurmatVechar import enterUrl
import os
app=Flask(__name__)

@app.route("/")
def home():
    removeAllZips()
    return redirect(url_for('index'))

@app.route("/index", methods=["POST","GET"])
def index():
    if request.method=="POST":
        theLink=request.form["link"]
        theLink=theLink.replace("/","   ")
        print("The Link: "+str(theLink))
        return redirect(url_for("download_file", theLINK=theLink))
    else:    
        return render_template("index.html")

@app.route("/download/<theLINK>")
def download_file(theLINK):
    removeAllZips()
    theLINK=theLINK.replace("   ","/")

    zipPath=enterUrl(theLINK)
    if zipPath==False:
        return "<h1>Not good link</h1>"
    return send_file(zipPath,download_name=zipPath, as_attachment=True)


def removeAllZips():
    for thing in os.listdir("./"):
        if ".zip" in thing:
            os.remove(thing)
if __name__=="__main__":
    app.run(debug=True)