from flask import Flask, redirect, url_for, render_template, send_file, request
import requests
from io import BytesIO

app=Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/index", methods=["POST","GET"])
def index():
    print(request.method)
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
    return f"<h1>{theLINK}</h1>"
    # r=requests.get(link)
    # return send_file(BytesIO(r.content),attachment_filename="TEST.mp3", as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)