from flask import Flask, render_template

app=Flask(__name__)

# @app.route("/")
# def home():
#     return "HI prum py <h1>BOB</h1>"

# @app.route("/<name>")
# def user(name):
#     return f"HI <h1>{name}</h1>"

@app.route("/<temp>")
def index(temp):
    return render_template("index.html",content=temp,lst=["vahe","guut","jio"])


if __name__=="__main__":
    app.run()