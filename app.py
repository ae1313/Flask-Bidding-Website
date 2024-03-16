from flask import Flask, render_template, request, redirect, session
import pymongo
import json
from flask_bcrypt import Bcrypt
import os
from dotenv import dotenv_values
from pymongo.server_api import ServerApi
import datetime
from hashlib import sha256

pswds = dotenv_values(".env")
uri = pswds["MONGO_URI"]

client = pymongo.MongoClient(uri)
db = client["flaskAppTest"]

app = Flask(__name__)
app.secret_key = "VERY VERY SECRET DO NOT SHARE PLS :)"
bcrypt = Bcrypt(app)


def mongodo(a):
    exec(a)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/browse")
def browse():
    if session.get("email"):
        items = []
        cursor = db.Groceries.find()
        for s in cursor:
            items.append(s)

        for i in items:
            for j in i:
                if j == "price":
                    i[j] = float(i[j])
        admin = db.users.find_one({"email": session["email"]})["admin"]
        if admin:
            return render_template("cart.html", items=items, admin=True)
        return render_template("cart.html", items=items)
    else:
        return redirect("/signin")


@app.route("/car")
def car():
    if not session.get("email"):
        return redirect("/signin")

    if not request.args.get("id") == None:
        page = request.args.get("id")
        print(page)
        cursor = db.Groceries.find_one({"pageID": page})
        return render_template("bidding.html", car=cursor)
    else:
        return render_template("index.html")


@app.route("/bidding", methods=["POST"])
def bidding():
    if request.method == "POST":
        data = request.data.decode("utf8")
        data = json.loads(data)
        id = data["id"]
        s = db.Groceries.find_one({"pageID": id})
        bid = int(data["data"])
        bids = s["bidding"]
        min = s["price"] / 2
        username = db.users.find_one({"email": session["email"]})["username"]
        print(s)
        print(data)

        if bids == [] and bid > min:

            db.Groceries.update_one(
                {"pageID": id}, {"$push": {"bidding": {"name": username, "bid": bid}}}
            )
            db.users.update_one(
                {"email": session["email"]},
                {
                    "$push": {
                        "bids": {
                            "amount": bid,
                            "id": data["id"],
                            "car": db.Groceries.find_one({"pageID": data["id"]})[
                                "name"
                            ],
                        }
                    }
                },
            )
            return "Good"
        elif bids == []:
            return "False"
        elif bids[0]["bid"] < bid:
            db.Groceries.update_one(
                {"pageID": data["id"]},
                {
                    "$push": {
                        "bidding": {
                            "$each": [{"name": username, "bid": bid}],
                            "$position": 0,
                        }
                    }
                },
            )
            db.users.update_one(
                {"email": session["email"]},
                {
                    "$push": {
                        "bids": {
                            "amount": bid,
                            "id": data["id"],
                            "car": db.Groceries.find_one({"pageID": data["id"]})[
                                "name"
                            ],
                        }
                    }
                },
            )

            return "Succeed"

        # # if s["bidding"] == [] and data["data"] > s["price"]/2:
        # if bids == [] and info > min:
        #     print('hi')
        # # TODO: GITHUB

        return "Big Fail"


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        if not db.users.find_one({"email": request.form.get("email")}):
            user = dict(request.form)
            user["admin"] = False
            user["password"] = bcrypt.generate_password_hash(user["password"]).decode(
                "utf-8"
            )
            db.users.insert_one(user)
            return redirect("\signin")
        else:
            return redirect("\signup")


@app.route("/signin", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("signin.html")

    elif request.method == "POST":
        try:
            email = request.form.get("email")
            canidate = request.form.get("password")
        except:
            return redirect("/signin?e=1")

        if db.users.find_one({"email": email}):
            canidate = request.form.get("password")
            hash = db.users.find_one({"email": email})["password"]
            if bcrypt.check_password_hash(hash, canidate):
                session["email"] = email
                print(session.get("email"))
                return redirect("/browse")

            else:
                return redirect("/signin?e=1")
        else:
            # return redirect("\signin")
            return redirect("/signin?e=1")
        return redirect("/signin?e=1")


@app.route("/session_check", methods=["GET"])
def session_check():
    return session.get("email")


@app.route("/signout", methods=["GET"])
def sign_out():
    session.pop("email", None)
    print(type(session.get("email")))
    return redirect("/signin")


@app.route("/dash", methods=["GET"])
def dash():
    if not session.get("email"):
        return redirect("/signin")
    user = db.users.find_one({"email": session["email"]})
    return render_template("dash.html", user=user)
    print(user)
    if False:
        # if user["bids"]:
        print(user)
        # bids= user["bids"]
        # return render_template("dash.html",bids)
    else:
        return redirect("/browse")


@app.route("/stop", methods=["POST"])
def stop_bid():
    data = request.data.decode("utf-8")
    id = json.loads(data)["id"]
    db.Groceries.update_one({"pageID": id}, {"$set": {"status": "closed"}})


@app.route("/start", methods=["POST"])
def open_bid():
    data = request.data.decode("utf-8")
    id = json.loads(data)["id"]
    db.Groceries.update_one({"pageID": id}, {"$set": {"status": "live"}})


@app.route("/admin", methods=["GET"])
def admin():
    pass
    return render_template("index.html")


@app.route("/new", methods=["GET"])
def serve_new():
    if not db.users.find_one({"email": session["email"]})["admin"]:
        return redirect("/cart")

    return render_template("new.html")


@app.route("/new", methods=["Post"])
def create_new():
    if not db.users.find_one({"email": session["email"]})["admin"]:
        return "Not Authorized", 403
    car = dict(request.form)
    car["bidding"] = []
    salt = str(datetime.time())
    b = f"aaaa{car['name']}hi_mom{salt}"
    pageID = sha256(b.encode()).hexdigest()
    car["quantity"] = int(car["quantity"])
    car["price"] = int(car["price"])
    car["pageID"] = pageID
    car["status"] = "live"
    db.Groceries.insert_one(car)
    print(car)
    return redirect("/browse")


if __name__ == "__main__":
    app.debug = True
    app.run()
    client.close()
