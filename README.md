What is this project?(Technical Precepective)

A small CRUD web application build using lightweight and fast python microframework.

What is this project?
A web app that helps to manage beautiful holiday homes of NRIs so it can be rented and monetize.

What you can do on this app?(with end points, method allowed, data required with content tye x-www-form-urlencoded)

Register users or if already registered login and start a session to play around with the API endpoints
-> /create_user -- [POST] -- {'user_name'}

Create Holiday home
-> /create_home -- [POST] -- {'owner1', 'owner2', 'home_name', 'city'}

Add Rooms for a particular house home 
-> /add_room -- [POST] -- {'home_name'}

Add image for Holiday home
-> /add_images_of_home -- [POST] -- {'home_picture', 'home_name'}

Get all the owners and their homes
-> /get_all_owners -- [GET] 

Get all homes
-> /get_all_homes -- [GET]

Get homes of a particular owner 
-> /get_homes_of_owners --[GET] -- {'owner'}

Get homes in a particular city with the weather of that city
-> /get_home_in_a_city -- [GET] -- {'city'}

Get rooms in a home
-> /get_rooms_of_home -- [GET] -- {'home_name'}

Get Image of a home
-> /get_images_of_home -- [GET] -- {'home_name'}

Update room info weather, like changing availability status, check out etc
-> /update_room_info -- [POST] -- {'room_name', 'rents', 'availability', 'check_out', 'check_in', 'rules'}

Delete a house(Deleting a house will also delete all its rooms)
-> /delete_home -- [DELETE] -- {'home_name'}


How to run the app?
It's suprisingly simpler than you'd think.

Step 1: Clone the repository.

Step 2: pip install -r requirements.txt

Step 3: Assuming that you have MongoDB installed and running. Run the command python app.py from the directory where app.py file is kept.

Step 4: You can test the APIs and Perform all the CRUD operations with the specified methods. Simply Open Postman, or install if you haven't already install and just hit the requests like to get all the Homes of a particular city just hit http://localhost:5001/get_home_in_a_city with GET method and add {city: 'Delhi'} with content type: x-www-form-urlencoded in body of the request.

Another Endpoint to create a home:
![image_2023-04-11_191922680](https://user-images.githubusercontent.com/86974814/231183952-eef3bba0-0ae7-49a0-8cc2-fdc092e44a2a.png)


What are my learnings?

a> Get to play with open weather api using which you can get temperature of your town.

Step 1: Make sure you have requests package to send http requests, account on openweathermap.org from where you have to create a API_key

city = 'Indore'
api = <Enter your api key here in string format>

URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}'
weatherRes = requests.get(URL)
if weatherRes.status_code == 200:
    weatherData = weatherRes.json()
    print(weatherData)
    # getting the main dict block
    main = weatherData['main']
    # getting temperature
    temperature = main['temp']


b> **Their are couple of ways to send json formmated text:**

1.  jsonify: This is a helper function in Flask that returns a JSON response object. It takes any number of arguments, which can be Python objects that can be serialized to JSON. It automatically sets the content type of the response to application/json. Here is example:

    return jsonify(object/dict)


2.  make_response: make_response is a helper function in Flask that creates a response object from the provided arguments. It takes any number of arguments, which can be the response body, status code, headers, or a tuple of these values. It returns a response object that can be returned from the view function. Here's an example:

    res = make_response(response.to_json(), 200)
    res.headers['Content-type'] = 'application/json'
    return res

    Here if you don't mention content-type as JSON it will be "text/html; charset=utf-8"

    In this example, make_response is used to create a response object with the JSON data and a 200 status code. The headers are set separately using the headers attribute of the response object.


3.  Response: Response is a class in Flask that can be used to create a response object with the specified parameters. It takes a single argument, which is the response body, and can accept optional arguments for the status code, headers, and content type. Here's an example:

    return Response(data, status=200, content_type='application/json')

    **In general, jsonify(class_object) helper function is useful when you want to create a response object from multiple values, make_response(JSON_DATA, STATUS CODE) helper funciton is useful when you need to modify the headers after creating the response object. Response(JSON_DATA, STATUS CODE) class is useful when you want to create a response object with a single call and with specified parameters.**


4.  json.dumps(): Takes a str, list or dictonary object and convert it into a JSON string.
   
    return make_response(json.dumps(dictObject), 200)

    It will retrun a JSON string but as we haven't set the content type to applicaiton/json it will be 'text/html'


5.  to_json(): We can convert a MongoEngine query object to JSON format which we can send in response. to_json() method comes with MongoEngine's Document class and creates a JSONified version of document.

    holiday_home = HolidayHomes.objects(home_name=data['home_name']).first()
    return make_response(holiday_home.to_json(), 200)
