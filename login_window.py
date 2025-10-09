import customtkinter as ctk
from tkinter import messagebox
from admin_dashboard import AdminDashboard
from db_config import connect_db


PRIMARY = "#1C1C1C"
ACCENT = "#2E2E2E"
SECONDARY = "#6C757D"
LIGHT = "#F2F2F2"
DARK = "#000000"

class LoginWindow:
    def __init__(self):
        # === Setup Root Window ===
        self.root = ctk.CTk()
        self.root.title("Jisami’s Hotel Reservation Services - Login")
        self.root.geometry("950x650")
        self.root.minsize(850, 600)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        # ===== Header Bar =====
        header = ctk.CTkFrame(self.root, fg_color=PRIMARY, height=90, corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="🏨 Welcome to Jisami’s Hotel Reservation Services",
            text_color="white",
            font=("Segoe UI", 26, "bold"),
        ).pack(pady=20)

        # ===== Main Frame =====
        main_frame = ctk.CTkFrame(self.root, fg_color=LIGHT, corner_radius=15)
        main_frame.pack(padx=90, pady=70, fill="both", expand=True)

        ctk.CTkLabel(
            main_frame,
            text="Administrator Login",
            text_color=DARK,
            font=("Segoe UI", 22, "bold"),
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            main_frame,
            text="Sign in to access the system dashboard",
            text_color=SECONDARY,
            font=("Segoe UI", 14),
        ).pack(pady=(0, 30))

        # ===== Input Fields =====
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=15)
        form_frame.pack(padx=60, pady=20, fill="x")
        form_frame.columnconfigure(1, weight=1)

        # Username
        ctk.CTkLabel(
            form_frame,
            text="Username:",
            text_color=DARK,
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, padx=10, pady=15, sticky="w")

        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your username",
            font=("Segoe UI", 13)
        )
        self.username_entry.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        # Password
        ctk.CTkLabel(
            form_frame,
            text="Password:",
            text_color=DARK,
            font=("Segoe UI", 14, "bold")
        ).grid(row=1, column=0, padx=10, pady=15, sticky="w")

        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your password",
            show="*",
            font=("Segoe UI", 13)
        )
        self.password_entry.grid(row=1, column=1, padx=10, pady=15, sticky="ew")

        # ===== Buttons =====
        btn_frame = ctk.CTkFrame(main_frame, fg_color=LIGHT)
        btn_frame.pack(pady=30)

        login_btn = ctk.CTkButton(
            btn_frame,
            text="Login",
            font=("Segoe UI", 16, "bold"),
            fg_color=ACCENT,
            hover_color="#495057",
            command=self.login
        )
        login_btn.pack(padx=20, pady=10)

        self.root.mainloop()

    # ===== Login Logic =====
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password")
            return

        # ===== Database Authentication =====
        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            record = cursor.fetchone()
            if record:
                self.root.destroy()
                AdminDashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Login error: {e}")
        finally:
            conn.close()
