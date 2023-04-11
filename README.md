What is this project?(Technical Precepective)

A small CRUD web application build using lightweight and fast python microframework.

What is this project?
A web app that helps to manage beautiful holiday homes of NRIs so it can be rented and monetize.

What you can do on this app?(with end points, method allowed, data required with content tye x-www-form-urlencoded)

Register users
-> /create_user -- [POST] -- {'user_name'}

Create Holiday home
-> /create_home -- [POST] -- {'owner1', 'owner2', 'home_name'}

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
