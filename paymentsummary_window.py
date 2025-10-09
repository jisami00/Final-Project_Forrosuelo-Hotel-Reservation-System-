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

class PaymentSummaryWindow:
    def __init__(self, stay_id):
        self.stay_id = stay_id


        self.root = ctk.CTk()
        self.root.title("Payment Summary")
        self.root.geometry("850x700")
        self.root.minsize(800, 650)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure([0,1,2,3,4], weight=1)


        header = ctk.CTkFrame(self.root, fg_color=PRIMARY, height=60, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="🧾 Payment Summary", text_color="white",
                     font=("Segoe UI", 22, "bold")).pack(pady=10)


        content = ctk.CTkFrame(self.root, fg_color=LIGHT, corner_radius=15)
        content.pack(padx=30, pady=20, fill="both", expand=True)
        content.columnconfigure(0, weight=1)


        self.load_summary(content)

        # ===== Footer =====
        ctk.CTkButton(self.root, text="Close", fg_color=PRIMARY, hover_color=ACCENT,
                      font=("Segoe UI", 14, "bold"), corner_radius=10,
                      command=self.root.destroy).pack(pady=10)

        self.root.mainloop()

    def load_summary(self, parent):
        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        try:
            # Guest & Reservation Info
            cursor.execute("""
                SELECT stay_ID, roomNo, firstName, lastName
                FROM reservations
                WHERE stay_ID=%s
            """, (self.stay_id,))
            reservation = cursor.fetchone()
            if not reservation:
                Conf.show_error("Reservation not found for this Stay ID")
                return

            full_name = f"{reservation['firstName']} {reservation['lastName']}"
            room_no = reservation['roomNo']

            ctk.CTkLabel(parent, text=f"Stay ID: {self.stay_id}", font=("Segoe UI", 16, "bold"),
                         text_color=DARK).pack(anchor="w", padx=20, pady=(15,5))
            ctk.CTkLabel(parent, text=f"Guest Name: {full_name}", font=("Segoe UI", 16, "bold"),
                         text_color=DARK).pack(anchor="w", padx=20, pady=5)
            ctk.CTkLabel(parent, text=f"Room Number: {room_no}", font=("Segoe UI", 16, "bold"),
                         text_color=DARK).pack(anchor="w", padx=20, pady=(5,15))

            # Services & Payments
            cursor.execute("""
                SELECT ServiceName, price
                FROM services
                WHERE stay_ID=%s
            """, (self.stay_id,))
            services = cursor.fetchall()

            tree_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
            tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

            style = ttk.Style()
            style.configure("Treeview", font=("Segoe UI", 12), rowheight=28)
            style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"))

            tree = ttk.Treeview(tree_frame, columns=("Service", "Price"), show="headings")
            tree.heading("Service", text="Service Name")
            tree.heading("Price", text="Price (₱)")
            tree.column("Service", width=400, anchor="w")
            tree.column("Price", width=120, anchor="center")
            tree.pack(padx=10, pady=10, fill="both", expand=True)

            total_amount = 0.0
            for svc in services:
                tree.insert("", "end", values=(svc['ServiceName'], f"{svc['price']:.2f}"))
                total_amount += float(svc['price'])

            ctk.CTkLabel(parent, text=f"Total Amount Paid: ₱{total_amount:.2f}",
                         font=("Segoe UI", 16, "bold"), text_color=PRIMARY).pack(pady=10)

        except Exception as e:
            Conf.show_error(f"Error loading summary: {e}")
        finally:
            conn.close()
