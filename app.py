from flask import Flask, render_template,request
import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://ae13:TWusC2KhvJhlUWjA@cluster0.qpa8lev.mongodb.net/?retryWrites=true&w=majority")
db = client['flaskAppTest']

app = Flask(__name__)
@app.route('/')
def index():
    username = "Aden"
    password = "Passcode"
    return render_template("index.html",username=username,password=password)

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


if __name__ == "__main__":
    app.debug=True
    app.run()
    print("hi")


client.close()