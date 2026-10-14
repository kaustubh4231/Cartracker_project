# Smart Golf Cart Booking System
# First Year Programming Project

# Predefined lists and constants
LOCATIONS = ["Hostel Area", "Main Gate", "Academic Block", "Library", "Sports Complex"]
CARTS = ["Cart 1", "Cart 2", "Cart 3", "Cart 4"]
CART_CAPACITY = 4
DATA_FILE = "bookings.txt"

# Build operating time slots from 08:00 to 19:45
TIME_SLOTS = []
for hour in range(8, 20):
    for minute in [0, 15, 30, 45]:
        h_str = str(hour)
        if len(h_str) == 1:
            h_str = "0" + h_str
        m_str = str(minute)
        if len(m_str) == 1:
            m_str = "0" + m_str
        TIME_SLOTS.append(h_str + ":" + m_str)


# -------------------------------------------------------------
# HELPER FUNCTIONS FOR USER INPUT
# -------------------------------------------------------------

def get_number_input(prompt, min_val, max_val):
    while True:
        user_val = input(prompt).strip()
        try:
            num = int(user_val)
            if min_val <= num <= max_val:
                return num
            else:
                print("Please enter a number between", min_val, "and", max_val)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def choose_location(prompt):
    print(prompt)
    for i in range(len(LOCATIONS)):
        print(str(i + 1) + ". " + LOCATIONS[i])
    choice = get_number_input("Select location (1-5): ", 1, len(LOCATIONS))
    return LOCATIONS[choice - 1]


def get_time_input(prompt):
    while True:
        t = input(prompt).strip()
        # Handle inputs like "9:00" -> "09:00"
        if len(t) == 4 and t[1] == ":":
            t = "0" + t
        if t in TIME_SLOTS:
            return t
        print("Invalid slot. Operating hours are 08:00 to 19:45 (in 15-min intervals).")


# -------------------------------------------------------------
# CORE BOOKING & ALLOCATION LOGIC
# -------------------------------------------------------------

def find_busy_carts(bookings, time):
    busy_list = []
    for b in bookings:
        if b["time"] == time:
            busy_list.append(b["cart"])
    return busy_list


def get_available_cart(bookings, time):
    busy_carts = find_busy_carts(bookings, time)
    for cart in CARTS:
        if cart not in busy_carts:
            return cart
    return None


def generate_booking_id(bookings):
    highest_id = 1000
    for b in bookings:
        current_num = int(b["booking_id"].replace("GC", ""))
        if current_num > highest_id:
            highest_id = current_num
    return "GC" + str(highest_id + 1)


def find_alternative_slots(bookings, current_time):
    alternatives = []
    start_index = TIME_SLOTS.index(current_time) + 1
    
    for i in range(start_index, len(TIME_SLOTS)):
        slot = TIME_SLOTS[i]
        cart = get_available_cart(bookings, slot)
        if cart is not None:
            alternatives.append(slot)
        if len(alternatives) == 3:
            break
    return alternatives


# -------------------------------------------------------------
# FILE HANDLING
# -------------------------------------------------------------

# def load_bookings():
#     bookings = []
#     try:
#         f = open(DATA_FILE, "r")
#         lines = f.readlines()
#         f.close()
        
#         for line in lines:
#             line = line.strip()
#             if line != "":
#                 parts = line.split(",")
#                 if len(parts) == 7:
#                     booking = {
#                         "booking_id": parts[0],
#                         "name": parts[1],
#                         "pickup": parts[2],
#                         "destination": parts[3],
#                         "time": parts[4],
#                         "passengers": int(parts[5]),
#                         "cart": parts[6]
#                     }
#                     bookings.append(booking)
#         print("Loaded", len(bookings), "booking(s) from", DATA_FILE)
#     except FileNotFoundError:
#         print("No existing bookings file found. Starting fresh.")
#     return bookings


def load_bookings():
    bookings = []

    try:
        f = open(DATA_FILE, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            line = line.strip()

            if line != "":
                parts = line.split(",")

                if len(parts) == 7:
                    booking = {
                        "booking_id": parts[0],
                        "name": parts[1],
                        "pickup": parts[2],
                        "destination": parts[3],
                        "time": parts[4],
                        "passengers": int(parts[5]),
                        "cart": parts[6]
                    }

                    bookings.append(booking)

        print("Loaded", len(bookings), "booking(s) from", DATA_FILE)

    except FileNotFoundError:
        # Create the file if it does not exist
        f = open(DATA_FILE, "w")
        f.close()
        print("New bookings file created:", DATA_FILE)

    return bookings

def save_bookings(bookings):
    f = open(DATA_FILE, "w")
    for b in bookings:
        line = b["booking_id"] + "," + b["name"] + "," + b["pickup"] + "," + \
               b["destination"] + "," + b["time"] + "," + str(b["passengers"]) + "," + b["cart"] + "\n"
        f.write(line)
    f.close()


# -------------------------------------------------------------
# MENU FEATURES
# -------------------------------------------------------------

def book_cart(bookings):
    print("\n--- Book a Golf Cart ---")
    while True:
        name = input("Enter passenger name: ").strip()
        if name != "":
            name = name.replace(",", " ")  # avoid csv breakage
            break
        print("Name cannot be empty.")

    pickup = choose_location("\nSelect Pickup Location:")
    while True:
        destination = choose_location("\nSelect Destination Location:")
        if destination != pickup:
            break
        print("Pickup and Destination cannot be the same! Choose again.")

    time = get_time_input("\nEnter preferred time slot (HH:MM): ")
    passengers = get_number_input("Enter passenger count (1-4): ", 1, CART_CAPACITY)

    cart = get_available_cart(bookings, time)
    
    if cart is not None:
        new_booking = {
            "booking_id": generate_booking_id(bookings),
            "name": name,
            "pickup": pickup,
            "destination": destination,
            "time": time,
            "passengers": passengers,
            "cart": cart
        }
        bookings.append(new_booking)
        save_bookings(bookings)
        print("\nBooking Confirmed!")
        print("Booking ID :", new_booking["booking_id"])
        print("Cart       :", new_booking["cart"])
        print("Time       :", new_booking["time"])
    else:
        print("\nAll carts are currently booked at", time)
        alts = find_alternative_slots(bookings, time)
        if len(alts) == 0:
            print("No later slots available today.")
            return

        print("\nAvailable upcoming slots:")
        for idx in range(len(alts)):
            print(str(idx + 1) + ". " + alts[idx])
        print("0. Cancel booking")

        choice = get_number_input("Pick an alternative slot: ", 0, len(alts))
        if choice != 0:
            chosen_slot = alts[choice - 1]
            cart = get_available_cart(bookings, chosen_slot)
            new_booking = {
                "booking_id": generate_booking_id(bookings),
                "name": name,
                "pickup": pickup,
                "destination": destination,
                "time": chosen_slot,
                "passengers": passengers,
                "cart": cart
            }
            bookings.append(new_booking)
            save_bookings(bookings)
            print("\nBooking Confirmed for alternative slot!")
            print("Booking ID :", new_booking["booking_id"])
            print("Cart       :", new_booking["cart"])
            print("Time       :", new_booking["time"])
        else:
            print("Booking cancelled.")


def check_cart_status(bookings):
    print("\n--- Check Cart Availability ---")
    t = get_time_input("Enter time slot to check (HH:MM): ")
    busy_carts = find_busy_carts(bookings, t)
    
    print("\nStatus of carts at " + t + ":")
    print("-" * 35)
    for c in CARTS:
        if c in busy_carts:
            print(c + " : BOOKED")
        else:
            print(c + " : AVAILABLE")
    print("-" * 35)


def view_all_bookings(bookings):
    print("\n--- All Active Bookings ---")
    if len(bookings) == 0:
        print("No bookings found.")
        return

    print("ID       | Name            | Pickup          | Destination     | Time  | Cart")
    print("-" * 75)
    for b in bookings:
        print(b["booking_id"] + "   | " + b["name"][:15].ljust(15) + " | " + 
              b["pickup"][:15].ljust(15) + " | " + b["destination"][:15].ljust(15) + " | " + 
              b["time"] + " | " + b["cart"])
    print("-" * 75)
    print("Total Bookings:", len(bookings))


def cancel_booking(bookings):
    print("\n--- Cancel a Booking ---")
    b_id = input("Enter Booking ID to cancel: ").strip().upper()
    found = None
    for b in bookings:
        if b["booking_id"] == b_id:
            found = b
            break

    if found is None:
        print("Booking ID not found.")
        return

    print("Found booking for", found["name"], "at", found["time"], "using", found["cart"])
    confirm = input("Are you sure you want to cancel? (y/n): ").strip().lower()
    if confirm == "y":
        bookings.remove(found)
        save_bookings(bookings)
        print("Booking", b_id, "has been successfully cancelled.")
    else:
        print("Cancellation aborted.")


# -------------------------------------------------------------
# MAIN PROGRAM LOOP
# -------------------------------------------------------------

def main():
    bookings = load_bookings()

    while True:
        print("\n==================================")
        print(" GOLF CART BOOKING SYSTEM ")
        print("==================================")
        print("1. Book a Golf Cart")
        print("2. Check Cart Availability by Time")
        print("3. View All Bookings")
        print("4. Cancel a Booking")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            book_cart(bookings)
        elif choice == "2":
            check_cart_status(bookings)
        elif choice == "3":
            view_all_bookings(bookings)
        elif choice == "4":
            cancel_booking(bookings)
        elif choice == "5":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice, please enter a number from 1 to 5.")


main()