import customtkinter as ctk
from tkinter import messagebox, ttk
from db_config import connect_db
from Conf import Conf
from payment_window import PaymentWindow


PRIMARY = "#000000"
ACCENT = "#1c1c1c"
SECONDARY = "#5a5a5a"
LIGHT = "#f2f2f2"
DARK = "#1a1a1a"
SUCCESS = "#343a40"


class ServicesWindow:
    def __init__(self, stay_id=None):
        self.stay_id = stay_id
        self.service_data = []
        self.service_vars = []

        # === Window Setup ===
        self.root = ctk.CTk()
        self.root.title("Hotel Services")
        self.root.geometry("850x700")
        self.root.minsize(800, 650)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure([0, 1, 2, 3, 4], weight=1)

        # ===== Header =====
        header = ctk.CTkFrame(self.root, fg_color=PRIMARY, height=70, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="Hotel Services",
            text_color="white",
            font=("Poppins", 26, "bold")
        ).pack(pady=15)


        scroll_frame = ctk.CTkScrollableFrame(
            self.root, fg_color=LIGHT, width=700, height=450
        )
        scroll_frame.pack(pady=20, padx=40, fill="both", expand=True)
        self.load_services(scroll_frame)

        # ===== Stay ID Input (if not passed) =====
        if not self.stay_id:
            id_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=15)
            id_frame.pack(pady=10)
            ctk.CTkLabel(
                id_frame,
                text="Enter Stay ID:",
                text_color=DARK,
                font=("Poppins", 14, "bold")
            ).pack(side="left", padx=10)
            self.stay_entry = ctk.CTkEntry(
                id_frame,
                placeholder_text="e.g. STAY123",
                font=("Poppins", 13),
                width=200
            )
            self.stay_entry.pack(side="left", padx=10)


        btn_frame = ctk.CTkFrame(self.root, fg_color=LIGHT)
        btn_frame.pack(pady=25)
        btn_frame.columnconfigure([0, 1, 2], weight=1)

        def create_button(text, color, hover, command):
            return ctk.CTkButton(
                btn_frame,
                text=text,
                fg_color=color,
                hover_color=hover,
                font=("Poppins", 15, "bold"),
                corner_radius=12,
                height=50,
                width=220,
                command=command
            )

        create_button("✅ Confirm Services", SUCCESS, "#157347", self.save_services)\
            .grid(row=0, column=0, padx=20, pady=10)
        create_button("👁️ View My Services", ACCENT, "#5c636a", self.view_selected_services)\
            .grid(row=0, column=1, padx=20, pady=10)
        create_button("↩️ Back to Dashboard", PRIMARY, ACCENT, self.back_dashboard)\
            .grid(row=0, column=2, padx=20, pady=10)

        # ===== Footer =====
        ctk.CTkLabel(
            self.root,
            text="© 2025 Jisami's Hotel Reservation Services",
            text_color=SECONDARY,
            font=("Poppins", 12)
        ).pack(pady=(0, 10))

        self.root.mainloop()

    # ===== Load Services =====
    def load_services(self, parent_frame):
        essential_services = [
            {'ServiceName': 'Swimming Pool Access', 'Description': 'Unlimited pool access', 'Price': 0.00},
            {'ServiceName': 'Gym Access', 'Description': 'Access to the hotel fitness center', 'Price': 0.00},
            {'ServiceName': 'Conference Room Booking', 'Description': 'Booking for meetings and events', 'Price': 2000.00},
            {'ServiceName': 'Breakfast Buffet', 'Description': 'Daily breakfast buffet for the stay', 'Price': 500.00},
            {'ServiceName': 'Spa Massage', 'Description': 'Relaxing 1-hour full-body massage', 'Price': 1200.00},
            {'ServiceName': 'Airport Pickup', 'Description': 'Private airport pickup service', 'Price': 500.00},
            {'ServiceName': 'Room Service Dinner', 'Description': 'Dinner served in your room', 'Price': 800.00},
            {'ServiceName': 'Laundry Service', 'Description': 'Full laundry service per day', 'Price': 300.00}
        ]

        # Load from DB
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM servicestable WHERE Availability='Available'")
            services = cursor.fetchall()
            if services:
                existing_names = {svc['ServiceName'] for svc in essential_services}
                for svc in services:
                    if svc['ServiceName'] not in existing_names:
                        essential_services.append(svc)
            conn.close()

        self.service_data = essential_services

        # Display services
        for service in essential_services:
            var = ctk.BooleanVar()
            card = ctk.CTkFrame(parent_frame, fg_color="white", corner_radius=12)
            card.pack(fill="x", padx=10, pady=8)
            ctk.CTkCheckBox(
                card,
                text=f"{service['ServiceName']} - ₱{service['Price']:.2f}",
                variable=var,
                font=("Poppins", 14, "bold")
            ).pack(anchor="w", padx=15, pady=(10, 0))
            ctk.CTkLabel(
                card,
                text=service['Description'],
                text_color=SECONDARY,
                font=("Poppins", 12),
                wraplength=600,
                justify="left"
            ).pack(anchor="w", padx=35, pady=(5, 10))
            self.service_vars.append(var)

    # ===== Save Services =====
    def save_services(self):
        conn = connect_db()
        if not conn:
            return

        stay_id = self.stay_id or self.stay_entry.get().strip()
        if not stay_id:
            Conf.show_error("Please enter Stay ID")
            return

        selected = [
            (stay_id, self.service_data[i]['ServiceName'], self.service_data[i]['Price'])
            for i, var in enumerate(self.service_vars) if var.get()
        ]

        if not selected:
            messagebox.showinfo("No Selection", "No services selected")
            return

        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO services (stay_ID, ServiceName, price) VALUES (%s, %s, %s)",
            selected
        )
        conn.commit()
        conn.close()

        Conf.show_success("Selected services have been added successfully!")

        # Open Payment Window after confirming services
        PaymentWindow(stay_id=stay_id)

    # ===== View Selected Services =====
    def view_selected_services(self):
        stay_id = self.stay_id or (self.stay_entry.get().strip() if hasattr(self, 'stay_entry') else None)
        if not stay_id:
            Conf.show_error("Please enter Stay ID first")
            return

        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ServiceName, price FROM services WHERE stay_ID=%s", (stay_id,))
        availed = cursor.fetchall()
        conn.close()

        if not availed:
            messagebox.showinfo("No Services", "No services found for this Stay ID")
            return

        total = sum(item['price'] for item in availed)
        view = ctk.CTkToplevel(self.root)
        view.title(f"Services for Stay ID: {stay_id}")
        view.geometry("550x450")

        ctk.CTkLabel(
            view,
            text=f"Services for Stay ID: {stay_id}",
            font=("Poppins", 18, "bold")
        ).pack(pady=15)

        tree = ttk.Treeview(view, columns=("Service", "Price"), show="headings")
        tree.heading("Service", text="Service Name")
        tree.heading("Price", text="Price (₱)")
        tree.column("Service", width=300)
        tree.column("Price", width=120)
        tree.pack(padx=20, pady=10, fill="both", expand=True)

        for svc in availed:
            tree.insert("", "end", values=(svc['ServiceName'], f"{svc['price']:.2f}"))

        ctk.CTkLabel(
            view,
            text=f"Total Cost: ₱{total:.2f}",
            text_color=DARK,
            font=("Poppins", 14, "bold")
        ).pack(pady=10)

        ctk.CTkButton(
            view,
            text="Close",
            fg_color=PRIMARY,
            hover_color=ACCENT,
            font=("Poppins", 13, "bold"),
            width=150,
            corner_radius=10,
            command=view.destroy
        ).pack(pady=5)


    def back_dashboard(self):
        self.root.destroy()
        from admin_dashboard import AdminDashboard  # delayed import to avoid circular reference
        AdminDashboard()
