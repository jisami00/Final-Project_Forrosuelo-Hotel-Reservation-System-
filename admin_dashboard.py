import customtkinter as ctk


PRIMARY = "#000000"
ACCENT = "#1c1c1c"
SECONDARY = "#5a5a5a"
LIGHT = "#f2f2f2"
DARK = "#1a1a1a"

class AdminDashboard:
    def __init__(self):

        self.root = ctk.CTk()
        self.root.title("Jisami’s Hotel Reservation Services - Admin Dashboard")
        self.root.geometry("950x650")
        self.root.minsize(850, 600)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure([0, 1, 2, 3, 4], weight=1)

        top_frame = ctk.CTkFrame(self.root, fg_color=PRIMARY, corner_radius=0, height=80)
        top_frame.pack(fill="x")

        ctk.CTkLabel(
            top_frame,
            text="Jisami’s Hotel Reservation Services - Admin Dashboard",
            text_color="white",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        main_frame = ctk.CTkFrame(self.root, fg_color=LIGHT, corner_radius=15)
        main_frame.pack(padx=50, pady=50, fill="both", expand=True)

        ctk.CTkLabel(
            main_frame,
            text="Welcome, Admin!",
            text_color=DARK,
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            main_frame,
            text="Manage hotel reservations, guest check-ins, payments, and service requests efficiently.",
            text_color=SECONDARY,
            font=("Segoe UI", 14)
        ).pack(pady=(0, 30))


        btn_frame = ctk.CTkFrame(main_frame, fg_color="#e6e6e6", corner_radius=15)
        btn_frame.pack(pady=10, padx=20, fill="both", expand=True)
        btn_frame.columnconfigure([0, 1], weight=1)
        btn_frame.rowconfigure([0, 1], weight=1)

        def create_button(text, color, hover, command):
            return ctk.CTkButton(
                btn_frame,
                text=text,
                fg_color=color,
                hover_color=hover,
                font=("Segoe UI", 16, "bold"),
                corner_radius=12,
                height=65,
                width=280,
                command=command
            )

        create_button("🛎 Reservation", "#2e2e2e", "#3d3d3d", self.open_reservation).grid(
            row=0, column=0, padx=25, pady=25, sticky="nsew"
        )

        create_button("🧳 Check-In", "#444444", "#555555", self.open_checkin).grid(
            row=0, column=1, padx=25, pady=25, sticky="nsew"
        )

        create_button("💳 Payment", "#666666", "#757575", self.open_payment).grid(
            row=1, column=0, padx=25, pady=25, sticky="nsew"
        )

        create_button("🧾 Services", "#8c8c8c", "#9c9c9c", self.open_services).grid(
            row=1, column=1, padx=25, pady=25, sticky="nsew"
        )

        footer = ctk.CTkLabel(
            self.root,
            text="© 2025 Jisami’s Hotel Reservation Services | Excellence in Every Stay",
            text_color=SECONDARY,
            font=("Segoe UI", 12)
        )
        footer.pack(pady=(0, 10))

        self.root.mainloop()

    def open_reservation(self):
        self.root.destroy()
        from reservation_window import ReservationWindow
        ReservationWindow()

    def open_checkin(self):
        self.root.destroy()
        from checkin import CheckInWindow
        CheckInWindow()

    def open_payment(self):
        self.root.destroy()
        from payment_window import PaymentWindow
        PaymentWindow()

    def open_services(self):
        self.root.destroy()
        from services_window import ServicesWindow
        ServicesWindow()


if __name__ == "__main__":
    AdminDashboard()
