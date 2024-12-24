import pandas as pd
from datetime import datetime, timedelta


class Room:
    def __init__(self, room_number, status = "Available"):
        self.__room_number = room_number
        self.__status = status

    def get_room_number(self):
        return self.__room_number

    def get_status(self):
        return self.__status

    def to_dict(self):
        return {
            "Room Number": self.get_room_number(),
            "Room Type": self.get_room_type(),
            "Status": self.get_status()
        }


class SingleRoom(Room):
    def __init__(self, room_number = None, price = 150, status = "Available"):
        super().__init__(room_number, status)
        self.__room_type = "SingleRoom"
        self.__price_per_night = price

    def get_price(self):
        return self.__price_per_night

    def get_room_type(self):
        return self.__room_type

    def to_dict(self):
        room_data = super().to_dict()
        return room_data


class DoubleRoom(Room):
    def __init__(self, room_number = None, price = 250, status = "Available"):
        super().__init__(room_number, status)
        self.__room_type = "DoubleRoom"
        self.__price_per_night = price

    def get_price(self):
        return self.__price_per_night

    def get_room_type(self):
        return self.__room_type

    def to_dict(self):
        room_data = super().to_dict()
        return room_data


class LuxuryRoom(Room):
    def __init__(self, room_number = None, price = 500, statues = "Available"):
        super().__init__(room_number, statues)
        self.__room_type = "LuxuryRoom"
        self.__price_per_night = price
        print("Additional Services For Luxury Room: Free Massage & Spa, Free Breakfast.\n")

    def get_price(self):
        return self.__price_per_night

    def get_room_type(self):
        return self.__room_type

    def to_dict(self):
        room_data = super().to_dict()
        return room_data


class Guest:
    def __init__(self, name, contact, membership = False):
        self.__name = name
        self.__contact = contact
        self.__membership = membership

    def get_name(self):
        return self.__name

    def get_contact(self):
        return self.__contact

    def get_membership(self):
        return self.__membership

    def to_dict(self):
        return {
            "name": self.get_name(),
            "contact": self.get_contact(),
            "membership": self.get_membership()
        }


class Reservation:
    def __init__(self, name, contact, room_type, reserved_date, day, is_check_in = "un-check-in"):
        self.name = name
        self.contact = contact
        self.type = room_type
        self.reserved_date = str(reserved_date)
        self.day = day
        self.is_check_in = is_check_in
        self.reservation_id = datetime.now().strftime("%y%m%d%H%M%S")
        if room_type == "SingleRoom":
            self.amount = float(SingleRoom().get_price()) * float(self.day)
        elif room_type == "DoubleRoom":
            self.amount = float(DoubleRoom().get_price()) * float(self.day)
        elif room_type == "LuxuryRoom":
            self.amount = float(LuxuryRoom().get_price()) * float(self.day)

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "guest_name": self.name,
            "contact": self.contact,
            "room_number": "Un-Arrange",
            "room_type": self.type,
            "reserved_date": self.reserved_date,
            "day": self.day,
            "is_check-in": self.is_check_in,
            "order_amount": self.amount
        }


class HotelManagementSystem:
    def __init__(self, rooms_file = "rooms.csv", guests_file = "guests.csv", reservations_file = "reservations.csv",
                 house_keeping_file = "housekeeping_schedule.csv", feedback_file = "feedback.csv"):
        self.rooms_file = rooms_file
        self.guests_file = guests_file
        self.reservations_file = reservations_file
        self.housekeeping_file = house_keeping_file
        self.feedback_file = feedback_file

        # load the data from csv file to dataframe
        self.rooms = self.load_data(self.rooms_file)
        self.guests = self.load_data(self.guests_file)
        self.reservations = self.load_data(self.reservations_file)
        self.housekeeping_schedule = self.load_data(self.housekeeping_file)
        self.feedback = self.load_data(self.feedback_file)

    def load_data(self, file_path):
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:                                                                                       #没找到文件会自动生成一个空的dataframe
            return pd.DataFrame()

    def save_data(self, file_path, data):
        data.to_csv(file_path, index=False)
        with open(file_path, "a") as f:
            f.flush()

    def add_room(self, room):
        room_number = room.get_room_number()
        room_type = room.get_room_type()

        if not self.rooms[
            (self.rooms["Room Number"] == room_number) & (self.rooms["Room Type"] == room_type)
        ].empty:
            print(f"room {room_number} has been exist")
        else:

            new_room = pd.DataFrame([room.to_dict()])
            self.rooms = pd.concat([self.rooms, new_room], ignore_index=True)
            self.save_data(self.rooms_file, self.rooms)
            print(f"room {room_number} added successfully")

    def get_available_rooms(self):
        available_rooms = self.rooms[self.rooms["Status"] == "Available"]
        available_sroom = available_rooms[available_rooms["Room Type"] == "SingleRoom"]
        print(f"{available_sroom.size} Available Single Room")
        available_droom = available_rooms[available_rooms["Room Type"] == "DoubleRoom"]
        print(f"{available_droom.size} Available Double Room")
        available_lroom = available_rooms[available_rooms["Room Type"] == "LuxuryRoom"]
        print(f"{available_lroom.size} Available Luxury Room")
        print("available room list：")
        print(available_rooms.to_string(index=False))

    def add_reservation(self, order):
        # add reservation
        new_reservation = pd.DataFrame([order.to_dict()])
        self.reservations = pd.concat([self.reservations, new_reservation], ignore_index=True)
        self.save_data(self.reservations_file, self.reservations)

        # Print Reservation Info
        checkin_date = datetime.strptime(order.reserved_date, "%Y%m%d")
        days_to_add = order.day
        checkout_date = checkin_date + timedelta(days=days_to_add)
        print(f"Dear {order.name}, Your reservation of one {order.type} from {checkin_date.strftime('%Y-%m-%d')} "
              f"to {checkout_date.strftime('%Y-%m-%d')} is received!"
              f"\nOrder Number: {order.reservation_id}")

    def make_reservation(self, client_name, client_contact):
        # client_name = input("Please Enter Your Name >> ")
        # client_contact = input("Please Enter Your Phone-Number >> ")

        while True:
            room_type = input("What Type of Room You Want Book?\n"
                              "Enter 1 For Single Room\n"
                              "Enter 2 For Double Room\n"
                              "Enter 3 For Luxury Room\n"
                              "Your Option is >> ")
            if room_type == "1":
                room_type = "SingleRoom"
                break
            elif room_type == "2":
                room_type = "DoubleRoom"
                break
            elif room_type == "3":
                room_type = "LuxuryRoom"
                break
            else:
                print("Wrong Input! Please try again.")
                continue

        while True:
            reserved_date = input("Please input the data for your reservation (YYYYMMDD)>> ")
            try:
                valid_date = datetime.strptime(reserved_date, "%Y%m%d")
                if valid_date <= datetime.now():
                    print("The reservation date must be in the future. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid date format! Please enter the date in YYYYMMDD format.")

        while True:
            try:
                days = int(input("Please enter your reservation days >> "))
                if days > 0:
                    break
                else:
                    print("The number of days must be greater than 0. Please try again.")
            except ValueError:
                print("Invalid input! Please enter a positive integer.")

        # establish and save reservation in the list.
        self.add_reservation(Reservation(client_name, int(client_contact), room_type, int(reserved_date), int(days)))

        # save client info
        # reserving_guest = Guest(client_name, client_contact)
        # self.add_guest(reserving_guest)


    def view_reservations(self):
        print("\ncurrent list：")
        print(self.reservations.to_string(index=False))

    def room_status_modify(self, room_number):
        # locate the Index of Modifying Room
        room_index = self.rooms[self.rooms["Room Number"] == room_number].index
        if not room_index.empty:
            # obtain the current status of the room
            current_status = self.rooms.loc[room_index, "Status"].iloc[0]
            # switch room status
            new_status = "Occupied" if current_status == "Available" else "Available"
            # update info
            self.rooms.loc[room_index, "Status"] = new_status
            self.save_data(self.rooms_file, self.rooms)  # 保存到文件
            print(f"room {room_number}'s status is modify from' {current_status} to  {new_status}。")
        else:
            print(f"can't find the room {room_number}，can't update the status。")

    def check_in(self):
        while True:
            # check in with the reservation id.
            reserve_id = input("Enter the reservation_id >> ")
            if validate_text(reserve_id, "back"):
                return
            else:
                order_index = self.reservations[
                    (self.reservations["reservation_id"] == int(reserve_id)) &
                    (self.reservations["is_check-in"] == "un-check-in")
                    ].index
                if not order_index.empty:
                    room_type = str(self.reservations.loc[order_index, "room_type"].iloc[0])
                    available_rooms = self.rooms[
                        (self.rooms["Status"] == "Available") &
                        (self.rooms["Room Type"] == room_type)
                        ]
                    if not available_rooms.empty:
                        # 获取第一间可用房间的房号
                        room_number_arranged = available_rooms.iloc[0]["Room Number"]
                        print(f"System Automatically arranged the Room[{room_number_arranged}] for this order")

                        # update the reservation list
                        self.reservations.loc[order_index, "room_number"] = room_number_arranged
                        self.reservations.loc[order_index, "is_check-in"] = "Checked-in"
                        self.save_data(self.reservations_file, self.reservations)

                        # update the rooms list
                        self.room_status_modify(room_number_arranged)
                        return
                    else:
                        print(f"No available rooms for {room_type}.")
                else:
                    print("Unfound Valid Reservation.")
                    return self.check_in()

    def check_out(self):
        while True:
            # check out with the room number
            room_to_checkout = input("Enter the Room Number >> ")
            if not validate_text(room_to_checkout, "back"):
                reserve_index = self.reservations[
                    (self.reservations["room_number"] == room_to_checkout) &
                    (self.reservations["is_check-in"] == "Checked-in")
                    ].index
                if not reserve_index.empty:
                    room_index = self.rooms[self.rooms["Room Number"] == room_to_checkout].index
                    # print(reserve_index, room_index)
                    order_amount = float(self.reservations.loc[reserve_index, "order_amount"].iloc[0])
                    print(f"The Amount for this order is ${order_amount}\n")

                    # update the reservation list
                    self.reservations.loc[reserve_index, "is_check-in"] = "Checked-out"
                    self.save_data(self.reservations_file, self.reservations)

                    # update the room list
                    self.rooms.loc[room_index, "Status"] = "Available"
                    self.save_data(self.rooms_file, self.rooms)
                    break
                else:
                    print("Not a valid Room Number to check out! ")
                    return self.check_out()
            else:
                return

    def add_guest(self, guest):
        name = guest.get_name()
        contact = guest.get_contact()
        # check if the guest exist
        existing_guest = self.guests[
            (self.guests["name"] == name) &
            (self.guests["contact"].astype(str) == str(contact))
            ]

        if not existing_guest.empty:
            print(f"\n The customer {name} has been exist in the list 。")
            return

        # add guest to dataset
        new_guest = pd.DataFrame([guest.to_dict()])
        self.guests = pd.concat([self.guests, new_guest], ignore_index=True)
        self.save_data(self.guests_file, self.guests)
        print(f"\nCustom {name} is added successfully！")

    def register_to_member(self, name, contact):
        # locate the Index of Modifying Room
        self.guests = self.load_data(self.guests_file)
        guest_index = self.guests[
            (self.guests["name"] == name) &
            (self.guests["contact"] == int(contact))].index

        if not guest_index.empty:  # check if the guest is a member.
            current_status = self.guests.loc[guest_index, "membership"].iloc[0]
            if current_status:
                print(f"Dear {name} is already a member, there is no need to apply again.")
            else:
                # switch the status
                new_status = True
                # undate information
                self.guests.loc[guest_index, "membership"] = new_status
                self.save_data(self.guests_file, self.guests)  # 保存到文件
                print(f"Customer {name} has been upgraded to membership.")
        else:
            print(f"Unfound Guest {name}, unable to modify membership.")

    def housekeeping_request(self, name, contact):
        def time_input(room):
            while True:  # 循环直到用户输入有效的时间
                try:
                    get_available_time = int(input("Please input the available hour for housekeeping (24-hour) >> "))
                    if 0 <= get_available_time <= 24:
                        print(f"Dear {name}, housekeeping service for Room [{room}] is scheduled within "
                              f"{get_available_time:02d}:00 - {get_available_time + 1:02d}:00.")
                        return get_available_time
                    else:
                        print("Invalid input! Please enter a number between 0 and 24.")
                except ValueError:
                    print("Invalid input! Please enter a valid number.")

        def add_housekeeping_schedule(room, time):
            date = datetime.now()
            add_data = {
                "Room": room,
                "Schedule Time": time,
                "Date": datetime.now().strftime("%y-%m-%d")
            }
            add_schedule = pd.DataFrame([add_data])
            self.housekeeping_schedule = pd.concat([self.housekeeping_schedule, add_schedule], ignore_index=True)
            self.save_data(self.housekeeping_file, self.housekeeping_schedule)

        get_room_number = self.reservations[
            (self.reservations["guest_name"] == name) &
            (self.reservations["contact"] == contact) &
            (self.reservations["is_check-in"] == "Checked-in")
            ]
        if not get_room_number.empty:
            # print(int(len(get_room_number)))
            if int(len(get_room_number)) == 1:
                room_num = get_room_number["room_number"].iloc[0]
                available_hour = time_input(room_num)
                period = f"{available_hour:02d}:00-{available_hour + 1:02d}:00"
                add_housekeeping_schedule(room_num, period)
                # print(period)
            elif int(len(get_room_number)) > 1:
                print(f"You have checked in for following room:\n"
                      f"{get_room_number["room_number"].to_string(index=False)}")
                room_num = input(f"Dear {name}, please enter the Room Number for housekeeping request >> ")
                available_hour = time_input(room_num)
                period = f"{available_hour:02d}:00-{available_hour + 1:02d}:00"
                add_housekeeping_schedule(room_num, period)
                # print(period)
        else:
            print(f"Dear {name}, Can not find your Check-in record!")

    def housekeeping_schedule_display(self):
        timetable = self.housekeeping_schedule
        timetable['Date'] = pd.to_datetime(timetable['Date'], format="%y-%m-%d")
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # filtering the pass data
        request_timetable = timetable[timetable['Date'] >= current_date]
        request_timetable = request_timetable.drop(columns=['Date'])
        # insert the status of the room in the request_timetable
        request_timetable = request_timetable.merge(self.rooms[['Room Number', 'Status']],
                                                    left_on='Room', right_on='Room Number',
                                                    how='left').drop(columns=['Room Number'])

        # get the Available status room number to arrange the housekeeping schedule
        available_rooms = self.rooms[self.rooms["Status"] == "Available"].copy()

        room_type_mapping = {
            "SingleRoom": "09:00-14:00",
            "DoubleRoom": "09:00-14:00",
            "LuxuryRoom": "07:00-09:00"
        }
        available_rooms["Schedule Time"] = available_rooms["Room Type"].map(room_type_mapping)
        default_timetable = available_rooms[["Room Number", "Schedule Time", "Status"]].copy()
        default_timetable = default_timetable.rename(columns={"Room Number": "Room"})

        # combine the request list and default list.
        combine_timetable = pd.concat([request_timetable, default_timetable], ignore_index=True)

        # sorting the combined timetable with the schedule time
        # building a temporary column used to sort
        combine_timetable["Start Time"] = pd.to_datetime(combine_timetable["Schedule Time"].str.split('-').str[0]
                                                         , format='%H:%M')

        # sorting by temporary column and drop the temporary colum
        combine_timetable = (combine_timetable.sort_values(by="Start Time").drop(columns="Start Time")
                             .reset_index(drop=True))

        print(f"Today's Housekeeping Schedule")
        print(combine_timetable)

    def fb(self, name, contact):
        rate = int(input("Please Rate for your experience in Hotel(1-10) >> "))
        comment = str(input("Please feel free to leave comment to us >> "))
        new_feedback = {
            "name": name,
            "contact": contact,
            "rate": rate,
            "comment": comment
        }
        fb_df = pd.DataFrame([new_feedback])
        self.feedback = pd.concat([self.feedback, fb_df], ignore_index=True)
        self.save_data(self.feedback_file, self.feedback)
        # print(self.feedback)

    def message_delivery(self, obj, msg_type):
        if obj == "member":
            TA = True
            TA_df = self.guests[self.guests["membership"] == TA]
        elif obj == "regular":
            TA = False
            TA_df = self.guests[self.guests["membership"] == TA]
        elif obj == "all":
            TA_df = self.guests
        print(f"{msg_type} Messages have been sent to following customers:")
        print(TA_df)


def validate_text(input_text, target_text):
    # compare the input_text and target_text, and output a boolean value.
    return str(input_text).strip().lower() == str(target_text).strip().lower()


# Main Program
print("Welcome the Hotel Management System! ")
hms = HotelManagementSystem()
while True:
    print("Options:")
    print("Enter 1. Customer Page")
    print("Enter 2. Administrator Page")
    print("Enter E. Exit")
    choice1 = input("\nEnter your Operation Code >> ")
    if choice1 == "1":
        customer_name = input("Please Enter Your Name >> ")
        customer_contact = int(input("Please Enter Your Contact >> "))
        reserving_guest = Guest(customer_name, customer_contact)
        hms.add_guest(reserving_guest)
        while True:
            print("Options for Customer:")
            print("Enter 1. Make a Reservation")
            print("Enter 2. Register to membership")
            print("Enter 3. Request a Housekeeping")
            print("Enter 4. Feedback")
            print("Enter E. Back to Main Manu")
            choice2 = input("\nEnter your Operation Code >> ")
            if choice2 == "1":
                hms.make_reservation(customer_name, customer_contact)
            elif choice2 == "2":
                hms.register_to_member(customer_name, customer_contact)
            elif choice2 == "3":
                hms.housekeeping_request(customer_name, customer_contact)
            elif choice2 == "4":
                hms.fb(customer_name, customer_contact)
            elif choice2 == "e":
                break
            else:
                print("Invalid choice. Please try again.")
    elif choice1 == "2":
        while True:
            print("Options for Administrator:")
            print("Enter 1. Manage Reservation")
            print("Enter 2. Check in")
            print("Enter 3. Check out")
            print("Enter 4. View Housekeeping Schedule")
            print("Enter 5. Manage Rooms")
            print("Enter 6. Customer Relationship Management")
            print("Enter E. Back to the Main Manu")
            choice3 = input("\nEnter your Operation Code >> ")
            if choice3 == "1":
                while True:
                    print("Options for Manage Reservation:")
                    print("Enter 1. Make Reservation")
                    print("Enter 2. Check Reservation")
                    print("Enter E. Back to the Admin Page")
                    choice4 = input("\nEnter your Operation Code >> ")
                    if choice4 == "1":
                        customer_name = input("Please Enter Your Name >> ")
                        customer_contact = input("Please Enter Your Contact >> ")
                        hms.make_reservation(customer_name, customer_contact)
                    elif choice4 == "2":
                        hms.view_reservations()
                    elif choice4.lower() == "e":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif choice3 == "2":
                hms.check_in()
            elif choice3 == "3":
                hms.check_out()
            elif choice3 == "4":
                hms.housekeeping_schedule_display()
            elif choice3 == "5":
                while True:
                    print("Options for Manage Reservation:")
                    print("Enter 1. View Available Rooms")
                    print("Enter 2. View All the Rooms Status")
                    print("Enter 3. Modify Room Status")
                    print("Enter E. Back to the Admin Page")
                    choice5 = input("\nEnter your Operation Code >> ")
                    if choice5 == "1":
                        hms.get_available_rooms()
                    elif choice5 == "2":
                        print(hms.rooms)
                    elif choice5 == "3":
                        room_num = input("Input the room number for the operation >> ")
                        hms.room_status_modify(room_num)
                    elif choice5.lower() == "e":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif choice3 == "6":
                while True:
                    print("Options for CRM:")
                    print("Enter 1. View Membership Guests")
                    print("Enter 2. Upgrade Guest to Membership")
                    print("Enter 3. Message to Guests")
                    print("Enter E. Back to the Admin Page")
                    choice6 = input("\nEnter your Operation Code >> ")
                    if choice6 == "1":
                        member_df = hms.guests[hms.guests["membership"] == True]
                        print(member_df)
                    elif choice6 == "2":
                        guest_to_upgrade = input("Input the Guest Name >> ")
                        guest_to_upgrade_number = input("Input the Guest Contact >> ")
                        hms.register_to_member(guest_to_upgrade, guest_to_upgrade_number)
                    elif choice6 == "3":
                        receivers = input("The Member to deliver message \n"
                                          "(all / member/ regular) >> ").lower()
                        content = input("Input the Content of the message >> ")
                        hms.message_delivery(receivers, content)

                    elif choice6.lower() == "e":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif choice3.lower() == "e":
                break
    elif choice1.lower() == "e":
        break
    else:
        print("Invalid choice. Please try again.")