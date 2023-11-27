import pymongo
from faker import Faker
from faker.providers import emoji
from random import randint
import hashlib

client = pymongo.MongoClient("mongodb+srv://ae13:TWusC2KhvJhlUWjA@cluster0.qpa8lev.mongodb.net/?retryWrites=true&w=majority")
db = client['flaskAppTest']
fake = Faker(["en_US"])

items = []

# for i in range(int(input("How Many Items: "))):
#     # print(x)
#     a =  {"name":fake.unique.emoji(),"price":randint(1,100),"quantity":randint(1,20)}
#     items.append(a)

items = [
    {"name": "Toyota Camry", "price": 28000, "quantity": 10, "image_url": "https://imgd.aeplcdn.com/1056x594/n/ixkkpua_1557403.jpg?q=80"},
    {"name": "Honda Civic", "price": 25000, "quantity": 8, "image_url": "https://imgd.aeplcdn.com/664x374/n/cw/ec/27074/civic-exterior-right-front-three-quarter-148156.jpeg?q=80"},
    {"name": "Ford F-150", "price": 35000, "quantity": 6, "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f0/2018_Ford_F-150_XLT_Crew_Cab%2C_front_11.10.19.jpg"},
    {"name": "Jeep Wrangler", "price": 40000, "quantity": 5, "image_url": "https://cdni.autocarindia.com/Utils/ImageResizer.ashx?n=https://cms.haymarketindia.net/model/uploads/modelimages/jeep-wrangler-model.jpg&w=730&h=484&q=75&c=1"},
    {"name": "Tesla Model 3", "price": 45000, "quantity": 3, "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/91/2019_Tesla_Model_3_Performance_AWD_Front.jpg"},
    {"name": "BMW X5", "price": 55000, "quantity": 4, "image_url": "https://stimg.cardekho.com/images/carexteriorimages/930x620/BMW/X5-2023/10452/1688992642182/front-left-side-47.jpg"},
    {"name": "Hyundai Sonata", "price": 26000, "quantity": 12, "image_url": "https://imgd.aeplcdn.com/1280x720/cw/cars/discontinued/hyundai/sonata-2011-2015.jpg?q=80"},
    {"name": "Mercedes-Benz C-Class", "price": 48000, "quantity": 2, "image_url": "https://imgd.aeplcdn.com/1056x594/n/ksvkl3a_1579019.jpg?q=80"},
    {"name": "Ford Mustang", "price": 32000, "quantity": 6, "image_url": "https://imgd.aeplcdn.com/1920x1080/cw/ec/23766/Ford-Mustang-Exterior-126883.jpg?wm=0&q=80&q=80"},
    {"name": "Chevrolet Malibu", "price": 28000, "quantity": 8, "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/01/2019_Chevrolet_Malibu_%28facelift%29_LT%2C_front_10.19.19.jpg"},
    {"name": "Audi Q7", "price": 60000, "quantity": 4, "image_url": "https://stimg.cardekho.com/images/carexteriorimages/930x620/Audi/Q7/10558/1689594791308/front-left-side-47.jpg"},
    {"name": "Kia Sorento", "price": 29000, "quantity": 10, "image_url": "https://cdni.autocarindia.com/Utils/ImageResizer.ashx?n=https://cdni.autocarindia.com/ExtraImages/20230102054522_Sorento.jpg&w=700&q=90&c=1"},
    {"name": "Subaru Outback", "price": 32000, "quantity": 7, "image_url": "https://media.ed.edmunds-media.com/subaru/outback/2024/oem/2024_subaru_outback_4dr-suv_onyx-edition-xt_fq_oem_1_1280.jpg"},
    {"name": "Volkswagen Jetta", "price": 24000, "quantity": 11, "image_url": "https://imgd.aeplcdn.com/642x336/cw/ec/17725/Volkswagen-Jetta-Right-Front-Three-Quarter-55817.jpg?wm=0&t=120020370&t=120020370&q=80"},
    {"name": "Mazda CX-5", "price": 31000, "quantity": 5, "image_url": "https://hips.hearstapps.com/hmg-prod/images/2022-mazda-cx-5-2p5-turbo-signature-123-1657559083.jpg?crop=0.741xw:0.834xh;0.124xw,0.166xh&resize=768:*"},
    {"name": "Lexus RX 350", "price": 48000, "quantity": 3, "image_url": "https://www.lexus.com/content/dam/lexus/images/models/rx/2024/visualizer/350/exterior/19-inch-five-spoke-alloy-wheels/eminent-white-pearl/small-1.jpg"},
    {"name": "GMC Sierra", "price": 36000, "quantity": 6, "image_url": "https://images.cars.com/cldstatic/wp-content/uploads/gmc-sierra-1500-at4x-2022-01-exterior-red-front-scaled.jpg"},
    {"name": "Chrysler Pacifica", "price": 33000, "quantity": 9, "image_url": "https://hips.hearstapps.com/hmg-prod/images/2024-chrysler-pacifica-103-64c163bd834cd.jpg?crop=0.642xw:0.724xh;0.160xw,0.225xh&resize=768:*"}
]

db.Groceries.update_many({},{"$set":{"bidding": []}})

cursor = db.Groceries.find()
# for s in cursor:
    # b = f"{s['_id']}{s['name']}"
    # a = hashlib.sha256(b.encode())
    # db.Groceries.update_one({'_id':s['_id']},{"$set":{"pageID": a.hexdigest()}})
    
# for s in cursor:
    # db.Groceries.update_one({'_id':s['_id']},{"$set":{"bidding":[]}})