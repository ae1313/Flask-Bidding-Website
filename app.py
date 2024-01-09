from flask import Flask, render_template,request,redirect
import pymongo
import json
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client['flaskAppTest']

app = Flask(__name__)
bcrypt = Bcrypt(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/cart')
def cart():
    items = []
    cursor = db.Groceries.find()
    for s in cursor:
        items.append(s)
    
    for i in items:
        for j in i:
            if j == "price":
                i[j]=float(i[j])
    print(items)
    
    return render_template("cart.html", items=items)

@app.route('/car')
def car():
    if not request.args.get('id') == None:
        page = request.args.get('id')
        print(page)
        cursor = db.Groceries.find_one({"pageID":page})
        return render_template("bidding.html",car=cursor)
    else:
        return render_template("index.html")


@app.route('/bidding',methods=["POST"])
def bidding():
    if request.method == "POST":
        data = request.data.decode("utf8")
        data = json.loads(data)
        id = data["id"]
        s = db.Groceries.find_one({"pageID":id})
        bid = int(data["data"])
        bids = s['bidding']
        min = s["price"]/2
        print(s)
        print(data)
        
        if bids == [] and bid > min:
            
            db.Groceries.update_one({"pageID":id}, {"$push":{"bidding":{"name":"adam","bid":bid}}})
            return "True"
        elif bids == []:
            return "False"
        elif bids[0]["bid"] < bid:
            return "True"
        
        
        # # if s["bidding"] == [] and data["data"] > s["price"]/2:
        # if bids == [] and info > min:
        #     print('hi')
        # # TODO: GITHUB
        # db.groceried.update_one({"pageID":data["id"]}, {"$push":{"bidding":{"name":"adam","bid":data["data"]}}})
        return "Big Fail"

@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        if not db.users.find_one({"email":request.form.get("email")}):
            user=dict(request.form)
            user["password"] = bcrypt.generate_password_hash(user["password"]).decode("utf-8")
            db.users.insert_one(user)
            return redirect("\signin")
        else:
            return redirect("\signup")
        
@app.route('/signin',methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("signin.html")
        
         
    elif request.method == "POST":
        try:
            email = request.form.get("email")
            canidate = request.form.get("password")
        except:
            return(redirect('/signin?e=1'))
        
        
        if db.users.find_one({"email":request.form.get("email")}):
            canidate = request.form.get("password")
            hash = db.users.find_one({"email": request.form.get("email")})["password"]
            if bcrypt.check_password_hash(hash, canidate):  
                return redirect("/cart")
            else: 
                return redirect("/signin?e=1")
        else:
            # return redirect("\signin")
            return redirect("/signin?e=1")
        return redirect("/signin?e=1")


    
if __name__ == "__main__":
    app.debug=True
    app.run()
    print("hi")


client.close()