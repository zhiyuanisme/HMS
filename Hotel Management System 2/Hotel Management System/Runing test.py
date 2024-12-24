import HMS

E = HMS
"""initialize HMS"""
hms = E.HotelManagementSystem()
name = "Jack"
contact = 100000001
"""add room"""
# for i in range(3, 10):
#     room_num = str(111 * i)
#     room_num = "L" + room_num
#     hms.add_room(E.LuxuryRoom(room_num))

"""modify room status"""
# hms.room_status_modify("S106")

"""View Available Room"""
# hms.get_available_rooms()

"""print out the price per night"""
# print(f"Luxury Room Price: ${str(LuxuryRoom("L888").get_price())} per night")

"""add guest"""
# n1_guest = Guest("Wang Wen", 123456789)
# n2_guest = Guest("Zhao Mingrun", 987654321, membership=1)
# hms.add_guest(n1_guest)
# hms.add_guest(n2_guest)

"""Modify guest membership"""
# hms.register_to_member(name="running2", contact="123333333")

"""Make a Reservation"""
# hms.make_reservation(name, contact)

"""View Reservation"""
# hms.view_reservations()

"""Check in"""
# hms.check_in()

"""Check out"""
# hms.check_out()

"""housekeeping requesting"""
# hms.housekeeping_request(name, contact)

"""Display the housekeeping schedule"""
# hms.housekeeping_schedule_display()

"""Feedback Function"""
# hms.fb(name, contact)

# hms.message_delivery("all", msg_type="Event")