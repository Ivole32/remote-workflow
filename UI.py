import customtkinter
import subprocess

customtkinter.set_widget_scaling(2.5)
customtkinter.set_window_scaling(2.2)

def button_callback():
    subprocess.Popen(["python3", "./UI.py"])
    exit(0)

def switch_event():
    print("switch toggled, current value:", switch_var.get())

app = customtkinter.CTk()
app.geometry("600x500")

button = customtkinter.CTkButton(
    app, text="Reload", command=button_callback,
    width=200, height=50, font=("Arial", 20)
)
button.pack(padx=20, pady=20)

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(padx=20, pady=20, fill="both", expand=True)

tabview.add("Settings")
tabview.add("Home")
tabview.set("Home")

switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(
    master=tabview.tab("Settings"),
    text="SSH File Share",
    command=switch_event,
    variable=switch_var,
    onvalue="on",
    offvalue="off",
    font=("Arial", 18)
)
switch.pack(pady=20)

settings_button = customtkinter.CTkButton(
    master=tabview.tab("Settings"),
    text="Settings Button",
    width=200, height=50,
    font=("Arial", 18)
)
settings_button.pack(padx=20, pady=20)

app.mainloop()