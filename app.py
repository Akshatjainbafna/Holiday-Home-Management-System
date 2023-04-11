from flask import Flask, render_template, request, make_response, session
from flask_mongoengine import MongoEngine
from missingRequiredField import checkFields
from flask_session import Session
from models import Owner, HolidayHomes, Rooms
import json
import requests
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# middlewares
app.secret_key = "abc"  
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb://localhost:27017/inkredo"}

# initalize mongodb odm
db = MongoEngine()
db.init_app(app)


@app.route("/create_user", methods=['POST'])
def create_user():
    data = request.form
    x = checkFields(data, fields=['user_name'])
    if (x):
        return make_response("Missing required field: " + x, 400)

    user = Owner.objects(user_name=data['user_name']).first()
    print(user)
    if not user:
        new_user = Owner(user_name=data['user_name']).save()
        session["user_name"] = data['user_name']
        return make_response(json.dumps(new_user.user_name), 200)
    else:
        return make_response('Username already in use', 200)



@app.route("/create_home", methods=['POST'])
def create_home():
    if 'user_name' in session:
        data = request.form
        x = checkFields(data, fields=['owner1', 'owner2', 'home_name'])
        if (x):
            return make_response("Missing required field: " + x, 400)

        owner1 = Owner.objects(user_name=data['owner1']).first()
        owner2 = Owner.objects(user_name=data['owner2']).first()

        if owner1 and owner2:
            owners = [data['owner1'], data['owner2']]
            home = HolidayHomes(
                owners=owners, 
                home_name=data['home_name'],
                city=data['city']
                ).save()
            return make_response('Holiday home created!', 200)
        else:
            return make_response('Owner isnt found!', 404)
    else:
        return make_response('Unauthorized Access', 401)


@app.route("/add_room", methods=['POST'])
def add_room():
    if 'user_name' in session:
        data = request.form
        x = checkFields(data, fields=['home_name'])
        if (x):
            return make_response("Missing required field: " + x, 400)

        holiday_home = HolidayHomes.objects(home_name=data['home_name']).first()

        if holiday_home:
            room = Rooms(
                holiday_homes=holiday_home,
                rents=data['rents'],
                room_name=data['room_name'],
                rules=data['rules']
            ).save()
            return make_response('Room created!', 200)
        else:
            return make_response('Holiday Home isnt found!', 404)
    else:
        return make_response('Unauthorized Access', 401)


@app.route("/add_images_of_home", methods=['POST'])
def add_images_of_home():
    if 'user_name' in session:
        data = request.form
        image = request.files['home_picture']
        filenameOfImage = secure_filename(image.filename)

        x = checkFields(data, fields=['home_name'])
        if (x):
            return make_response("Missing required field: " + x, 400)

        holiday_home = HolidayHomes.objects(home_name=data['home_name']).first()

        if holiday_home:
            address_of_image = f'/static/{filenameOfImage}'
            fileHandler = open('.' + address_of_image, "wb")
            fileHandler.write(image.read())
            fileHandler.close()

            holiday_home.update(set__image = address_of_image)
            return make_response('Image uploaded!', 200)
        else:
            return make_response('Holiday Home isnt found!', 404)
    else:
        return make_response('Unauthorized Access', 401)


@app.route("/get_all_owners", methods=['GET'])
def get_all_owners():
    if 'user_name' in session:
        all_owners = Owner.objects.all()

        response = []

        for owner in all_owners:
            allTheHomesOfOwner = []
            for home in HolidayHomes.objects(owners = owner.user_name).all():
                print(home)
                allTheHomesOfOwner.append(home.home_name)

            string_of_owner = owner.to_json()
            dict_of_owner = json.loads(string_of_owner)
            dict_of_owner['homes'] = allTheHomesOfOwner
            response.append(dict_of_owner)

        return make_response(json.dumps(response), 200)
    else:
        return make_response('Unauthorized Access', 401)


@app.route("/get_all_homes", methods=['GET'])
def get_all_homes():
    if 'user_name' in session:
        response = HolidayHomes.objects.all()
        return make_response(response.to_json(), 200)
    else:
        return make_response('Unauthorized Access', 401)



@app.route("/get_homes_of_owners", methods=['GET'])
def get_homes_of_owners():
    if 'user_name' in session:
        data = request.form
        
        owner_obj = Owner.objects(user_name = data['owner']).first()
        response = HolidayHomes.objects(owners = owner_obj.user_name).all()
        return make_response(response.to_json(), 200)
    else:
        return make_response('Unauthorized Access', 401)


@app.route("/get_home_in_a_city", methods=['GET'])
def get_home_in_a_city():
    if 'user_name' in session:
        data = request.form
        api = '56cc01e53fba330279561106f976e85c'
        city = data['city']
        response = HolidayHomes.objects(city = city).all()

        URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}'
        weatherRes = requests.get(URL)

        if weatherRes.status_code == 200:
            weatherData = response.json()
             # getting the main dict block
            main = weatherData['main']
            # getting temperature
            temperature = main['temp']
            string_of_owner = response.to_json()
            dict_of_owner = json.loads(string_of_owner)
            dict_of_owner['temp'] = temperature

            return make_response(json.dumps(dict_of_owner), 200)
        
        return make_response(response.to_json(), 200)
    else:
        return make_response('Unauthorized Access', 401)

@app.route("/get_rooms_of_home", methods=['GET'])
def get_rooms_of_home():
    if 'user_name' in session:
        data = request.form
        x = checkFields(data, fields=['home_name'])
        if (x):
            return make_response("Missing required field: " + x, 400)

        holiday_home = HolidayHomes.objects(home_name=data['home_name']).first()

        if holiday_home:
            rooms = Rooms.objects(
                holiday_homes=holiday_home
            ).all()
            return make_response(rooms.to_json(), 200)
        else:
            return make_response('Holiday Home isnt found!', 404)
    else:
        return make_response('Unauthorized Access', 401)


@app.route("/get_images_of_home", methods=['GET'])
def get_images_of_home():
    if 'user_name' in session:
        data = request.form
        x = checkFields(data, fields=['home_name'])
        if (x):
            return make_response("Missing required field: " + x, 400)

        holiday_home = HolidayHomes.objects(home_name=data['home_name']).only('image').first()

        if holiday_home:
            return make_response(holiday_home.to_json(), 200)
        else:
            return make_response('Holiday Home isnt found!', 404)
    else:
        return make_response('Unauthorized Access', 401)
    
@app.route("/delete_home", methods=['DELETE'])
def delete_home():
    if 'user_name' in session:
        data = request.form
        x = checkFields(data, fields=['home_name'])
        if (x):
            return make_response("Missing required field: " + x, 400)

        holiday_home = HolidayHomes.objects(home_name=data['home_name']).first()
        list_of_rooms_in_home = Rooms.objects(holiday_homes = holiday_home).all()
        list_of_rooms_in_home.delete()
        holiday_home.delete()

        return make_response('Delete holiday home successfully!', 200)

    else:
        return make_response('Unauthorized Access', 401)
    
@app.route("/update_room_info", methods=['POST'])
def update_home():
    if 'user_name' in session:
        data = request.form
        x = checkFields(data, fields=['room_name'])
        if (x):
            return make_response("Missing required field: " + x, 400)
        
        room = Rooms.objects(room_name = data['room_name']).first()

        availability = True if data['availability'] == 'true' else False

        if room:
            room.update(set__rents = data['rents'], set__availability = availability, set__check_out = data['check_out'], set__check_in = data['check_in'], set__rules = data['rules'])
            return make_response('Updated room info successfully!', 200)
        else:
            return make_response('Holiday Home isnt found!', 404)
    else:
        return make_response('Unauthorized Access', 401)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
