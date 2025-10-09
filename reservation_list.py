import customtkinter as ctk
from tkinter import ttk
from db_config import connect_db
from Conf import Conf


PRIMARY = "#000000"
ACCENT = "#1c1c1c"
SECONDARY = "#5a5a5a"
LIGHT = "#f8f9fa"
DARK = "#1a1a1a"
SUCCESS = "#343a40"

class ReservationListWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Reservation List")
        self.root.geometry("1000x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure([0,1,2,3,4], weight=1)


        header = ctk.CTkFrame(self.root, fg_color=PRIMARY, height=70, corner_radius=0)
        header.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(
            header,
            text="📋 Reservation List",
            text_color="white",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=15)


        search_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=12)
        search_frame.grid(row=1, column=0, padx=40, pady=10, sticky="ew")
        search_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            search_frame,
            text="Search Stay ID / Room No:",
            font=("Segoe UI", 14, "bold"),
            text_color=DARK
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Type Stay ID or Room No...",
            font=("Segoe UI", 13)
        )
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            fg_color=PRIMARY,
            hover_color="#1a1a1a",
            font=("Segoe UI", 13, "bold"),
            corner_radius=10,
            width=120,
            command=self.search_reservation
        ).grid(row=0, column=2, padx=10)

        ctk.CTkButton(
            search_frame,
            text="↺ Refresh",
            fg_color=ACCENT,
            hover_color="#5c636a",
            font=("Segoe UI", 13, "bold"),
            corner_radius=10,
            width=100,
            command=self.load_reservations
        ).grid(row=0, column=3, padx=10)

        # ===== Table Style =====
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 12), rowheight=28, background="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"))
        style.map("Treeview", background=[('selected', '#343a40')], foreground=[('selected', 'white')])

        # ===== Reservation Table =====
        self.tree = ttk.Treeview(
            self.root,
            columns=("Stay ID", "Name", "Room No", "Adults", "Children", "Check In", "Check Out", "Price"),
            show="headings"
        )
        self.tree.heading("Stay ID", text="Stay ID")
        self.tree.heading("Name", text="Guest Name")
        self.tree.heading("Room No", text="Room No")
        self.tree.heading("Adults", text="Adults")
        self.tree.heading("Children", text="Children")
        self.tree.heading("Check In", text="Check In")
        self.tree.heading("Check Out", text="Check Out")
        self.tree.heading("Price", text="Total Price")

        col_widths = [120, 180, 100, 80, 100, 120, 120, 120]
        for i, col in enumerate(self.tree["columns"]):
            self.tree.column(col, width=col_widths[i], anchor="center")

        self.tree.grid(row=2, column=0, padx=40, pady=10, sticky="nsew")

        # ===== Buttons =====
        action_frame = ctk.CTkFrame(self.root, fg_color=LIGHT)
        action_frame.grid(row=3, column=0, pady=10)
        action_frame.columnconfigure([0,1,2], weight=1)

        ctk.CTkButton(
            action_frame,
            text="🗑 Cancel Reservation",
            fg_color=PRIMARY,
            hover_color="#1a1a1a",
            font=("Segoe UI", 14, "bold"),
            corner_radius=10,
            width=220,
            height=45,
            command=self.cancel_reservation
        ).grid(row=0, column=0, padx=20, pady=10)

        ctk.CTkButton(
            action_frame,
            text="↩ Back to Dashboard",
            fg_color=ACCENT,
            hover_color="#5c636a",
            font=("Segoe UI", 14, "bold"),
            corner_radius=10,
            width=220,
            height=45,
            command=self.back_dashboard
        ).grid(row=0, column=1, padx=20, pady=10)


        ctk.CTkLabel(
            self.root,
            text="© 2025 Jisami’s Hotel Reservation Services",
            text_color=SECONDARY,
            font=("Segoe UI", 12)
        ).grid(row=4, column=0, pady=(0,10))

        # Load all reservations on start
        self.load_reservations()
        self.root.mainloop()

    # ===== Load All Reservations =====
    def load_reservations(self):
        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM reservations")
            data = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())

            for row in data:
                full_name = f"{row['firstName']} {row['lastName']}"
                self.tree.insert("", "end", values=(
                    row["stay_ID"],
                    full_name,
                    row["roomNo"],
                    row["adults"],
                    row["children"],
                    row["checkInDate"],
                    row["checkOutDate"],
                    f"₱{row['totalPrice']:.2f}" if 'totalPrice' in row else "₱0.00"
                ))
        except Exception as e:
            Conf.show_error(f"Error loading reservations: {e}")
        finally:
            conn.close()

    # ===== Search Reservation =====
    def search_reservation(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.load_reservations()
            return

        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT * FROM reservations
                WHERE stay_ID LIKE %s OR roomNo LIKE %s
            """
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            data = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in data:
                full_name = f"{row['firstName']} {row['lastName']}"
                self.tree.insert("", "end", values=(
                    row["stay_ID"],
                    full_name,
                    row["roomNo"],
                    row["adults"],
                    row["children"],
                    row["checkInDate"],
                    row["checkOutDate"],
                    f"₱{row['totalPrice']:.2f}" if 'totalPrice' in row else "₱0.00"
                ))
        except Exception as e:
            Conf.show_error(f"Error searching reservations: {e}")
        finally:
            conn.close()

    # ===== Cancel Reservation =====
    def cancel_reservation(self):
        selected = self.tree.focus()
        if not selected:
            Conf.show_error("Please select a reservation to cancel")
            return

        values = self.tree.item(selected, "values")
        stay_id = values[0]

        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT roomNo FROM reservations WHERE stay_ID=%s", (stay_id,))
            room = cursor.fetchone()
            cursor.execute("DELETE FROM reservations WHERE stay_ID=%s", (stay_id,))
            conn.commit()

            if room:
                cursor.execute("UPDATE rooms SET status='Available' WHERE roomNo=%s", (room[0],))
                conn.commit()

            Conf.show_success(f"Reservation {stay_id} has been cancelled.")
            self.load_reservations()
        except Exception as e:
            Conf.show_error(f"Error cancelling reservation: {e}")
        finally:
            conn.close()


    def back_dashboard(self):
        self.root.destroy()
        from admin_dashboard import AdminDashboard
        AdminDashboard()
