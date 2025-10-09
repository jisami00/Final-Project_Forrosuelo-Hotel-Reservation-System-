import customtkinter as ctk
from tkinter import messagebox
from db_config import connect_db
from Conf import Conf
from admin_dashboard import AdminDashboard


PRIMARY = "#1C1C1C"
ACCENT = "#2E2E2E"
SECONDARY = "#6C757D"
LIGHT = "#F2F2F2"
SUCCESS = "#198754"


class CheckInWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Jisami’s Hotel - Guest Check-In/Check-Out")
        self.root.geometry("900x700")
        self.root.minsize(850, 650)
        ctk.set_appearance_mode("light")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure([0,1,2,3], weight=1)


        header = ctk.CTkFrame(self.root, fg_color=PRIMARY, height=70, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="🏨 Guest Check-In / Check-Out",
            text_color="white",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=15)


        main_frame = ctk.CTkFrame(self.root, fg_color=LIGHT, corner_radius=15)
        main_frame.pack(padx=50, pady=20, fill="both", expand=True)

        # Stay ID Input
        ctk.CTkLabel(main_frame, text="Enter Stay ID:", font=("Segoe UI", 14, "bold"), text_color=PRIMARY).pack(pady=(20,5))
        self.stay_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Stay ID",
            font=("Segoe UI", 15),
            width=300,     # wider input
            height=40      # taller input
        )
        self.stay_entry.pack(pady=(0,20))

        # Guest Info Display
        self.info_label = ctk.CTkLabel(main_frame, text="", text_color=PRIMARY, font=("Segoe UI", 14), justify="left")
        self.info_label.pack(pady=(10,20))

        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color=LIGHT)
        btn_frame.pack(pady=20)
        btn_frame.columnconfigure([0,1,2], weight=1)

        def create_button(text, color, hover, command):
            return ctk.CTkButton(btn_frame, text=text, fg_color=color, hover_color=hover,
                                 font=("Segoe UI", 15, "bold"), corner_radius=10, height=50, width=180, command=command)

        create_button("🔍 Show Guest Info", ACCENT, "#495057", self.show_guest_info).grid(row=0, column=0, padx=10, pady=10)
        create_button("✅ Check-In Guest", SUCCESS, "#157347", self.check_in_guest).grid(row=0, column=1, padx=10, pady=10)
        create_button("🛎 Check-Out Guest", ACCENT, "#8c8c8c", self.check_out_guest).grid(row=0, column=2, padx=10, pady=10)
        create_button("⬅ Back to Dashboard", ACCENT, "#495057", self.back_dashboard).grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Footer
        ctk.CTkLabel(self.root, text="© 2025 Jisami’s Hotel Reservation System", text_color=SECONDARY, font=("Segoe UI", 12)).pack(pady=(0,10))

        self.root.mainloop()

    # ===== Show Guest Info =====
    def show_guest_info(self):
        stay_id = self.stay_entry.get().strip()
        if not stay_id:
            Conf.show_error("Please enter Stay ID")
            return

        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM reservations WHERE stay_ID=%s", (stay_id,))
            record = cursor.fetchone()
            if not record:
                Conf.show_error("No reservation found with that Stay ID.")
                return

            status = record.get("status", "Not Checked-In")
            self.info_label.configure(text=f"""
Guest Name: {record['firstName']} {record.get('middleName','')} {record['lastName']}
Check-In: {record['checkInDate']}
Check-Out: {record['checkOutDate']}
Status: {status}
""")
        except Exception as e:
            Conf.show_error(f"Error fetching guest info: {e}")
        finally:
            conn.close()

    # ===== Check-In Guest =====
    def check_in_guest(self):
        self.update_status("Checked-In", "Guest successfully checked in!")

    # ===== Check-Out Guest =====
    def check_out_guest(self):
        self.update_status("Checked-Out", "Guest successfully checked out!")

    # ===== General Status Update =====
    def update_status(self, new_status, success_msg):
        stay_id = self.stay_entry.get().strip()
        if not stay_id:
            Conf.show_error("Please enter Stay ID")
            return

        conn = connect_db()
        if not conn:
            return
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT status FROM reservations WHERE stay_ID=%s", (stay_id,))
            record = cursor.fetchone()
            if not record:
                Conf.show_error("No reservation found with that Stay ID.")
                return

            if record["status"] == new_status:
                Conf.show_error(f"Guest is already {new_status}.")
                return

            if messagebox.askyesno("Confirm Action", f"Are you sure you want to mark this guest as {new_status}?"):
                cursor.execute("UPDATE reservations SET status=%s WHERE stay_ID=%s", (new_status, stay_id))
                conn.commit()
                Conf.show_success(success_msg)
                self.show_guest_info()
        except Exception as e:
            Conf.show_error(f"Error updating status: {e}")
        finally:
            conn.close()


    def back_dashboard(self):
        self.root.destroy()
        AdminDashboard()
