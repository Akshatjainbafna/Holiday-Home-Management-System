import mongoengine as me

# Create your models here.

class Owner(me.Document):
    user_name = me.StringField(required=True, unique=True)

class HolidayHomes(me.Document):
    owners = me.ListField(me.StringField(), min_length=2)
    home_name = me.StringField(max_length=150, unique=True)
    city = me.StringField(max_length=100)
    no_rooms = me.IntField(default=0)
    image = me.StringField(default='./default.png')

class Rooms(me.Document):
    holiday_homes = me.ReferenceField(HolidayHomes, reverse_delete_rule=me.CASCADE)
    rents = me.IntField()
    room_name = me.StringField(max_length=20, default = None, unique=True)
    availability = me.BooleanField(default = True)
    check_in = me.StringField(default = None)
    check_out = me.StringField(default = None)
    rules = me.StringField(max_length = 1000)