import customtkinter as ctk
from tkinter import messagebox, ttk
from db_config import connect_db
from Conf import Conf
from decimal import Decimal

PRIMARY = "#000000"
ACCENT = "#1c1c1c"
SECONDARY = "#5a5a5a"
LIGHT = "#f8f9fa"
DARK = "#1a1a1a"
SUCCESS = "#343a40"

class PaymentWindow:
    def __init__(self, stay_id=None):
        self.stay_id = stay_id
        self.payment_data = []
        self.total_amount = 0.0

        self.root = ctk.CTk()
        self.root.title("Payment Window")
        self.root.geometry("900x750")
        self.root.minsize(850, 650)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

        # ===== Header =====
        header = ctk.CTkFrame(self.root, fg_color=PRIMARY, height=70, corner_radius=0)
        header.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(
            header, text="💳 Payment Window", text_color="white",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=15)

        frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=12)
        frame.grid(row=1, column=0, padx=50, pady=20, sticky="ew")
        frame.columnconfigure([1], weight=1)

        ctk.CTkLabel(
            frame, text="Enter Stay ID:", font=("Segoe UI", 14, "bold"),
            text_color=DARK
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.stay_entry = ctk.CTkEntry(frame, placeholder_text="e.g. STAY123", font=("Segoe UI", 13))
        self.stay_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        if self.stay_id:
            self.stay_entry.insert(0, self.stay_id)

        btn_frame = ctk.CTkFrame(self.root, fg_color=LIGHT)
        btn_frame.grid(row=2, column=0, pady=10)
        btn_frame.columnconfigure([0, 1, 2], weight=1)

        def make_button(text, color, hover, command, emoji=""):
            return ctk.CTkButton(
                btn_frame, text=f"{emoji} {text}", fg_color=color, hover_color=hover,
                font=("Segoe UI", 14, "bold"), corner_radius=10, width=220, height=45,
                command=command
            )

        make_button("📄 Load Payment Details", SUCCESS, "#495057", self.load_payment).grid(row=0, column=0, padx=20, pady=10)
        make_button("💰 Process Payment", PRIMARY, "#1a1a1a", self.process_payment).grid(row=0, column=1, padx=20, pady=10)
        make_button("↩️ Back to Dashboard", ACCENT, "#5c636a", self.back_dashboard).grid(row=0, column=2, padx=20, pady=10)


        summary_card = ctk.CTkFrame(self.root, fg_color="white", corner_radius=15)
        summary_card.grid(row=3, column=0, padx=40, pady=20, sticky="nsew")
        summary_card.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            summary_card, text="🧾 Payment Details",
            font=("Segoe UI", 18, "bold"), text_color=DARK
        ).pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"))

        self.tree = ttk.Treeview(summary_card, columns=("Item", "Price"), show="headings")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Price", text="Price (₱)")
        self.tree.column("Item", width=450, anchor="w")
        self.tree.column("Price", width=120, anchor="center")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        self.total_label = ctk.CTkLabel(
            summary_card, text="Total: ₱0.00",
            font=("Segoe UI", 16, "bold"), text_color=PRIMARY
        )
        self.total_label.pack(pady=10)


        ctk.CTkLabel(
            self.root, text="© 2025 Jisami’s Hotel Reservation Services",
            text_color=SECONDARY, font=("Segoe UI", 12)
        ).grid(row=5, column=0, pady=(0, 10))

        self.root.mainloop()


    def load_payment(self):
        stay_id = self.stay_entry.get().strip()
        if not stay_id:
            Conf.show_error("Please enter Stay ID")
            return

        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        try:
            # Check reservation
            cursor.execute("SELECT * FROM reservations WHERE stay_ID=%s", (stay_id,))
            reservation = cursor.fetchone()
            if not reservation:
                Conf.show_error("Reservation not found for this Stay ID")
                return

            self.payment_data = []
            self.total_amount = 0.0


            room_price = float(reservation.get("TotalPrice", 1000))  # fallback if missing
            self.payment_data.append(("Room Charge", room_price))


            cursor.execute("""
                SELECT s.ServiceName, s.price
                FROM services s
                WHERE s.stay_ID = %s
            """, (stay_id,))
            services = cursor.fetchall()
            for svc in services:
                price = float(svc["price"]) if isinstance(svc["price"], Decimal) else svc["price"]
                self.payment_data.append((svc["ServiceName"], price))


            for i in self.tree.get_children():
                self.tree.delete(i)


            for item, price in self.payment_data:
                self.tree.insert("", "end", values=(item, f"{price:.2f}"))
                self.total_amount += float(price)

            self.total_label.configure(text=f"Total: ₱{self.total_amount:.2f}")

        except Exception as e:
            Conf.show_error(f"Error loading payment details: {e}")
        finally:
            conn.close()

    def process_payment(self):
        stay_id = self.stay_entry.get().strip()
        if not stay_id:
            Conf.show_error("Please enter Stay ID")
            return

        if not self.payment_data:
            Conf.show_error("No payment details loaded")
            return

        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute(
                """ INSERT INTO payments (stay_ID, amountPaid, paymentDate)
                    VALUES (%s, %s, NOW()) """,
                (stay_id, self.total_amount)
            )
            conn.commit()

            Conf.show_success(f"Payment processed successfully!\nTotal Paid: ₱{self.total_amount:.2f}")


            for i in self.tree.get_children():
                self.tree.delete(i)
            self.total_label.configure(text="Total: ₱0.00")
            self.payment_data = []

        except Exception as e:
            Conf.show_error(f"Error processing payment: {e}")
        finally:
            conn.close()

    def back_dashboard(self):
        self.root.destroy()
        from admin_dashboard import AdminDashboard
        AdminDashboard()
