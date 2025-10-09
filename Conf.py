import customtkinter as ctk


PRIMARY = "#212529"
SUCCESS = "#198754"
ERROR = "#dc3545"
ACCENT = "#343a40"

class Conf:
    @staticmethod
    def show_success(message):

        popup = ctk.CTkToplevel()
        popup.title("Success")
        popup.geometry("400x150")
        popup.resizable(False, False)
        popup.configure(fg_color=PRIMARY)

        ctk.CTkLabel(popup, text="✅ Success!", font=("Poppins", 16, "bold"), text_color=SUCCESS).pack(pady=(20, 10))
        ctk.CTkLabel(popup, text=message, font=("Poppins", 13), text_color="white", wraplength=350, justify="center").pack(pady=(0, 15))
        ctk.CTkButton(popup, text="OK", fg_color=SUCCESS, hover_color="#157347", font=("Poppins", 13, "bold"),
                      width=120, corner_radius=10, command=popup.destroy).pack()
        popup.grab_set()  # Make the popup modal

    @staticmethod
    def show_error(message):

        popup = ctk.CTkToplevel()
        popup.title("Error")
        popup.geometry("400x150")
        popup.resizable(False, False)
        popup.configure(fg_color=PRIMARY)

        ctk.CTkLabel(popup, text="Error!", font=("Poppins", 16, "bold"), text_color=ERROR).pack(pady=(20, 10))
        ctk.CTkLabel(popup, text=message, font=("Poppins", 13), text_color="white", wraplength=350, justify="center").pack(pady=(0, 15))
        ctk.CTkButton(popup, text="OK", fg_color=ERROR, hover_color="#a71d2a", font=("Poppins", 13, "bold"),
                      width=120, corner_radius=10, command=popup.destroy).pack()
        popup.grab_set()
