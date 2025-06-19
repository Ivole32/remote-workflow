from logger import Logger
import customtkinter as ctk

logger = Logger()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("500x400")
app.title("Remote Workflows")

textbox = ctk.CTkTextbox(app, width=500, height=300)
textbox.pack(padx=20, pady=20)

textbox.insert("0.0", "In development")

textbox.configure(state="disabled")

if __name__ == "__main__":
    app.mainloop()