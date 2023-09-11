default prev_room = None
default cur_room = None
default prev_location = None
default cur_location = None
default cur_map_id = None
# Variable to check the map screen: if it is True then the player is viewing the map.
default map_open = False

# list of closed rooms is checked change_room
# is composed of id = room_id and Commitment()
# expired elements are checked in after_spending_time, if you don't want an expiration: hour_stop = None
# TODO: Wiki
default closed_rooms = {}

init 1 python:
    if not cur_room and rooms.length > 0:
        cur_room = rooms[0]
    if not cur_location and locations.length > 0:
        cur_location = locations[0]
    if not cur_map_id and cur_location:
        cur_map_id = cur_location.map_id
