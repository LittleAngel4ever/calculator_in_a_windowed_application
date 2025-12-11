import customtkinter as ctk
import math

ctk.set_appearance_mode("system") 
ctk.set_default_color_theme("theme.json") # Style Mercedes Formula 1 Team

app = ctk.CTk()
app.title("Калькулятор")
app.geometry("465x465")

entry = ctk.CTkEntry(app, width=380, height=50, font=("Arial", 20))
entry.pack(pady=10)

def open_popup():
    popup = ctk.CTkToplevel(app)
    popup.geometry("250x150")
    popup.title("Инструкция к n_sqrt")
    label = ctk.CTkLabel(popup, text="Сначала число, потом корень.")
    label.pack(pady=10)
    close_button = ctk.CTkButton(popup, text="Закрыть", command=popup.destroy)
    close_button.pack(pady=5)
    popup.after(3000, popup.destroy)

def n_sqrt(x, n):
    return math.pow(x, 1/n)

def calculate():
    try:
        expr = entry.get()
        result = eval(expr, {**math.__dict__, "n_sqrt": n_sqrt})
        entry.delete(0, "end")
        entry.insert(0, str(result))
    except:
        entry.delete(0, "end")
        entry.insert(0, "Ошибка")

def press(key):
    if key == "=":
        calculate()
    elif key == "C":
        entry.delete(0, "end")
    elif key == "^":
        entry.insert("end", "**")
    elif key == "√":
        entry.insert("end", "sqrt(")
    elif key == "ⁿ√":
        open_popup()
        entry.insert("end", "n_sqrt(")
    else:
        entry.insert("end", key)

frame = ctk.CTkFrame(app)
frame.pack(pady=20)

buttons = [
    "sin","cos","tan","log","√","ⁿ√",
    "(",")","^","pi","e",
    "7","8","9","/","C",
    "4","5","6","*","-",
    "1","2","3","+","%",
    "0",".",",","="
]

row, col = 0, 0
for b in buttons:
    btn = ctk.CTkButton(frame, text=b, width=70, height=50,
                        command=lambda x=b: press(x))
    btn.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 4:
        col = 0
        row += 1

app.mainloop()
