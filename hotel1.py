import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime, timedelta
from PIL import Image, ImageTk


# Room class
class Room:
    def __init__(self, number, room_type, room_price):

        self.room_number = number
        self.room_type = room_type
        self.is_booked = False
        self.price = room_price
        self.booking_date_time = "N/A"
        self.check_out_date_time = "N/A"

    def display_details(self):
        status = "Booked" if self.is_booked else "Available"
        return {
            "Room No": self.room_number,
            "Room Type": self.room_type,
            "Price": f"{self.price:.2f} INR",
            "Status": status,
            "Booking DateTime": self.booking_date_time,
            "Check-out DateTime": self.check_out_date_time
        }


# Customer class
class Customer:
    def __init__(self, name, address, phone, room_number):
        self.name = name
        self.address = address
        self.phone = phone
        self.room_number = room_number


# Hotel Management class
class Management:
    def __init__(self):
        self.rooms = [
            Room(101, "Single", 1000.00),
            Room(102, "Single", 1000.00),
            Room(201, "Double", 2000.00),
            Room(202, "Double", 2000.00),
            Room(301, "Deluxe", 3000.00),
            Room(302, "Deluxe", 3000.00),
            Room(401, "Premium", 5000.00),
            Room(402, "Premium", 5000.00)
        ]
        self.customers = []

    def get_current_time_ist(self):
        utc_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
        return utc_time.strftime("%d-%m-%y %H:%M:%S")


# Main Application class
class HotelManagementApp:
    def __init__(self, root):
        self.hotel = Management()
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')

        # Load Background Image using PIL
        self.bg_image_path = ("C:/Users/user/Pictures/Screenshots/Screenshot 2024-11-06 140232.png")
        self.bg_image = Image.open(self.bg_image_path)

        # Resize image initially to fit the window size
        self.bg_image_resized = self.bg_image.resize((self.root.winfo_width(), self.root.winfo_height()),
                                                     Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_resized)

        # Set the background label
        self.bg_label = tk.Label(root, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        # Add the window resizing event to dynamically update background
        self.root.bind("<Configure>", self.resize_background)

        # Welcome Label
        tk.Label(root, text="Welcome to the Hotel Management System", font=("Helvetica", 18, "bold"),
                 bg='lightblue').pack(pady=10)

        # Buttons
        tk.Button(root, text="Show Available Rooms", command=self.show_available_rooms, font=("Arial", 12),
                  bg='#4CAF50', fg='white').pack(pady=5)
        tk.Button(root, text="Check-Out", command=self.check_out_customer, font=("Arial", 12), bg='#FF9800',
                  fg='white').pack(pady=5)
        tk.Button(root, text="Generate Bill", command=self.generate_bill, font=("Arial", 12), bg='#FF9800',
                  fg='white').pack(pady=5)

        # Input Fields for Room Number and Customer Name (below the buttons)
        self.room_number_label = tk.Label(root, text="Enter Room Number (101-402):", font=("Arial", 12), bg='lightblue')
        self.room_number_label.pack(pady=5)

        self.room_number_entry = tk.Entry(root, font=("Arial", 12))
        self.room_number_entry.pack(pady=5)

        self.customer_name_label = tk.Label(root, text="Enter Customer Name:", font=("Arial", 12), bg='lightblue')
        self.customer_name_label.pack(pady=5)

        self.customer_name_entry = tk.Entry(root, font=("Arial", 12))
        self.customer_name_entry.pack(pady=5)

        self.book_button = tk.Button(root, text=" Book Room", command=self.book_room, font=("Arial", 12), bg='#4CAF50',
                                     fg='white')
        self.book_button.pack(pady=10)

        # Output Area for displaying room details with scrolling
        self.output_frame = tk.Frame(root, bg='lightblue')
        self.output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Scrollable Canvas
        self.canvas = tk.Canvas(self.output_frame)
        self.scrollbar = ttk.Scrollbar(self.output_frame, orient="vertical", command=self.canvas.yview)
        self.horizontal_scrollbar = ttk.Scrollbar(self.output_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        # Pack the canvas and scrollbars
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.horizontal_scrollbar.pack(side="bottom", fill="x")  # Ensure it fills the width

        # Store previous available room state for optimization
        self.previous_rooms_state = {}

    def resize_background(self, event):
        # Resize the background image to fit the window size (only if size has changed)
        new_width = event.width
        new_height = event.height
        if new_width != self.bg_image_resized.width or new_height != self.bg_image_resized.height:
            self.bg_image_resized = self.bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_resized)
            self.bg_label.config(image=self.bg_image_tk, text="Background")

    def show_available_rooms(self):
        # Clear previous output only if necessary
        rooms_state = {room.room_number: room.is_booked for room in self.hotel.rooms}
        if rooms_state != self.previous_rooms_state:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            available_rooms_label = tk.Label(self.scrollable_frame, text="Available Rooms:", font=("Arial", 18, "bold"),
                                             bg='lightblue')
            available_rooms_label.grid(row=0, columnspan=2, pady=20)

            row = 1
            for room in self.hotel.rooms:
                if not room.is_booked:
                    details = room.display_details()
                    for col, (key, value) in enumerate(details.items()):
                        tk.Label(self.scrollable_frame, text=f"{key}:", font=("Arial", 14), bg='lightblue').grid(
                            row=row, column=col * 2, padx=10, sticky="e")
                        tk.Label(self.scrollable_frame, text=value, font=("Arial", 14), bg='lightblue').grid(row=row,
                                                                                                             column=col * 2 + 1,
                                                                                                             padx=10,
                                                                                                             sticky="w")
                    row += 1

            if row == 1:  # No available rooms
                tk.Label(self.scrollable_frame, text="No rooms available.", font=("Arial", 14), bg='lightblue').grid(
                    row=1, columnspan=2, pady=10)

            # Update the previous rooms state to prevent unnecessary updates
            self.previous_rooms_state = rooms_state

    def book_room(self):
        room_number = self.room_number_entry.get()
        customer_name = self.customer_name_entry.get()

        # Validate Room Number and Customer Name
        if room_number.isdigit() and 101 <= int(room_number) <= 402:
            room_number = int(room_number)
            if customer_name:
                room_found = False
                for room in self.hotel.rooms:
                    if room.room_number == room_number and not room.is_booked:
                        self.hotel.customers.append(Customer(customer_name, "", "", room_number))
                        room.is_booked = True
                        room.booking_date_time = self.hotel.get_current_time_ist()
                        messagebox.showinfo("Success", f"Room {room_number} booked by {customer_name}.")
                        room_found = True
                        # Refresh the available rooms immediately after booking
                        self.show_available_rooms()  # This will update the displayed available rooms
                        break

                if not room_found:
                    messagebox.showerror("Error", "Room not available.")
                else:
                    # Clear the room number and customer name fields after booking
                    self.room_number_entry.delete(0, tk.END)
                    self.customer_name_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Customer Name is required.")
        else:
            messagebox.showerror("Error", "Please enter a valid room number.")

    def check_out_customer(self):
        room_number = self.ask_for_room_number()  # Ask for room number through a dialog box
        if room_number is not None:  # Only proceed if a valid room number is entered
            customer_found = False
            for i, customer in enumerate(self.hotel.customers):
                if customer.room_number == room_number:
                    for room in self.hotel.rooms:
                        if room.room_number == room_number:
                            room.is_booked = False  # Mark the room as available
                            room.check_out_date_time = self.hotel.get_current_time_ist()  # Log the check-out time
                            messagebox.showinfo("Success", f"Room {room_number} checked out.")  # Show success message
                            self.hotel.customers.pop(i)  # Remove customer from the list
                            customer_found = True
                            break
                    break  # Exit the outer loop once the room is found and processed

            if not customer_found:  # If no customer was found for the room
                messagebox.showerror("Error", "No customer found for this room.")
            else:
                # After successful check-out, refresh the available rooms display
                self.show_available_rooms()  # Automatically update the room list to show available rooms

    def generate_bill(self):
        room_number = self.ask_for_room_number()
        if room_number is not None:
            customer_found = False
            for customer in self.hotel.customers:
                if customer.room_number == room_number:
                    for room in self.hotel.rooms:
                        if room.room_number == room_number:
                            messagebox.showinfo("Bill", f"Bill for Room {room_number}: {room.price:.2f} INR")
                            customer_found = True
                            break
                    break
            if not customer_found:
                messagebox.showerror("Error", "No customer found for this room.")

    def ask_for_room_number(self):
        try:
            room_number = int(simpledialog.askstring("Room Number", "Enter Room Number (101-402):"))
            if room_number < 101 or room_number > 402:
                messagebox.showerror("Invalid Room Number", "Room number must be between 101 and 402.")
                return None
            return room_number
        except (ValueError, TypeError):
            messagebox.showerror("Invalid Input", "Please enter a valid room number.")
            return None


# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()