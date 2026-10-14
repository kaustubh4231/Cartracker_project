# Campus Golf Cart Booking System

A Python-based command-line tool built to manage and schedule campus golf carts. It handles booking requests, assigns carts automatically, prevents double-booking, and suggests upcoming time slots if all carts are occupied.

I built this project to solve transit congestion and scheduling conflicts across common campus transit points (hostels, library, academic blocks) using clean modular Python and basic file persistence.

---

## What It Does

- **Smart Slot Booking:** Books trips across 15-minute operating windows (08:00 to 19:45) and assigns the first available cart.
- **Alternative Slot Suggestions:** If all carts are full at a requested time, it searches ahead and suggests the next 3 available slots.
- **File Persistence:** Saves and updates all bookings in a comma-delimited flat file (`bookings.txt`) so records persist across restarts without needing an external database.
- **Input Checking:** Validates passenger counts (1–4), checks operating hours, normalizes single-digit time inputs (e.g., `9:00` -> `09:00`), and ensures pickup and drop-off locations aren't identical.
- **Fleet Status & Cancellation:** Lets users check cart availability for any specific time slot, view all active bookings in an aligned table, or cancel a trip using its Booking ID (`GC1001`, `GC1002`, etc.).

---

## System Configuration

- **Fleet:** 4 Carts (`Cart 1` to `Cart 4`)
- **Capacity:** Up to 4 passengers per cart
- **Operating Hours:** 08:00 to 19:45 (15-min intervals)
- **Stops:** Hostel Area, Main Gate, Academic Block, Library, Sports Complex
- **Storage:** Plain text CSV (`bookings.txt`)

---

## Project Structure

```text
├── golf_cart_booking.py   # Main CLI application
├── bookings.txt           # Text-based storage for bookings (auto-created)
└── README.md              # Project documentation
