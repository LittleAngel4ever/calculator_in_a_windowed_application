import tkinter as tk
from tkinter import font
import math, json, os

class Calculator:
    def __init__(self, root, theme_file="theme.json"):
        self.root = root
        self.theme = self.theme(theme_file)

        window = self.theme["window"]
        self.root.title(window["title"])
        self.root.geometry(window["geometry"])
        self.root.resizable(window["resizable"], window["resizable"])
        self.root.configure(bg=self.theme["colors"]["bg"])
        self.geometry_default = window["geometry"]
        self.geometry_expanded = window["geometry_expanded"]

        self.display_font = self.font(self.theme["fonts"]["display"], 34)
        self.button_font  = self.font(self.theme["fonts"]["button"], 20)
        self.mode_font    = self.font(self.theme["fonts"]["mode"], 12)
        self.sci_font     = self.font(self.theme["fonts"]["sci"], 14)

        self.input = ""
        self.display = tk.StringVar(value="0")
        self.motion = None
        self.first_value = None
        self.second_value = False
        self.trigonometry_mode = "DEG"
        self.visible = False
        self.buttons = {}

        self.build()
        self.bind_keys()

    def theme(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def font(self, spec, fallback_size):
        try:
            return font.Font(family=spec["family"], size=spec["size"], weight=spec["weight"])
        except:
            return font.Font(size=fallback_size)

    def add_button(self, parent, text, command, style, row, col, colspan=1, btn_font=None, width=8, height=2):
        colors = self.theme["colors"]
        bg, fg, hover_bg = style
        btn = tk.Button(parent, text=text, font=btn_font or self.button_font,
                        bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
                        borderwidth=0, relief='flat', cursor='hand2',
                        command=command, width=width, height=height)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)
        return btn

    def build(self):
        colors, layout, texts = self.theme["colors"], self.theme["layout"], self.theme["texts"]

        main_container = tk.Frame(self.root, bg=colors['bg'])
        main_container.pack(fill='both', expand=True, padx=layout["padding"], pady=layout["padding"])

        mode_frame = tk.Frame(main_container, bg=colors['bg'])
        mode_frame.pack(fill='x', pady=(0, 15))
        self.mode_label = tk.Label(mode_frame, text=f"{texts['mode_label_prefix']}{self.trigonometry_mode}",
                                   font=self.mode_font, bg=colors['bg'], fg='#888888')
        self.mode_label.pack(side='left')
        tk.Button(mode_frame, text=texts["mode_toggle"], font=self.mode_font,
                  command=self.toggle_trig_mode, bg=colors['toggle_btn'], fg='white',
                  activebackground=colors['toggle_btn_hover'], activeforeground='white',
                  borderwidth=0, relief='flat', cursor='hand2').pack(side='right')

        display_frame = tk.Frame(main_container, bg=colors['display_bg'], height=layout["display_height"])
        display_frame.pack(fill='x', pady=(0, 20))
        tk.Label(display_frame, textvariable=self.display, font=self.display_font,
                 bg=colors['display_bg'], fg=colors['display_fg'], anchor='e').pack(fill='both', expand=True)

        self.sci_toggle_btn = tk.Button(main_container, text=texts["sci_toggle_closed"], font=self.sci_font,
                                        command=self.toggle_sci_panel, bg=colors['sci_btn'], fg='white',
                                        activebackground=colors['sci_btn_hover'], activeforeground='white',
                                        borderwidth=0, relief='flat', cursor='hand2')
        self.sci_toggle_btn.pack(fill='x', pady=(0, 15))

        self.sci_panel = tk.Frame(main_container, bg=colors['bg'], height=layout["sci_panel_height"])
        self.sci_panel.pack_propagate(False)

        self.keyboard_frame = tk.Frame(main_container, bg=colors['bg'])
        self.keyboard_frame.pack(fill='both', expand=True)
        for i in range(4): self.keyboard_frame.grid_columnconfigure(i, weight=1, minsize=layout["keyboard_col_min"])
        for i in range(5): self.keyboard_frame.grid_rowconfigure(i, weight=1, minsize=layout["keyboard_row_min"])

        for row_idx, row in enumerate(self.theme["buttons"]["main"]):
            for col_idx, text in enumerate(row):
                if text == "": continue
                colspan = 2 if text == '=' else 1
                col = col_idx if text != '=' else 2
                if text in ['C','⌫','%']:
                    style = (colors['special_btn'], colors['special_text'], colors['special_btn_hover'])
                elif text in ['/', '*', '-', '+', '=']:
                    style = (colors['op_btn'], colors['op_text'], colors['op_btn_hover'])
                else:
                    style = (colors['num_btn'], colors['num_text'], colors['num_btn_hover'])
                btn = self.add_button(self.keyboard_frame, text, lambda t=text: self.button_click(t),
                                         style, row_idx, col, colspan, width=10 if colspan==2 else 8)
                self.buttons[text] = btn

        self.build_panel()

    def build_panel(self):
        colors = self.theme["colors"]
        sci_container = tk.Frame(self.sci_panel, bg=colors['bg'])
        sci_container.pack(fill='both', expand=True, padx=5, pady=5)
        for i in range(4): sci_container.grid_columnconfigure(i, weight=1)
        for i in range(5): sci_container.grid_rowconfigure(i, weight=1)
        for row_idx, row in enumerate(self.theme["buttons"]["scientific"]):
            for col_idx, text in enumerate(row):
                btn = self.add_button(sci_container, text, lambda t=text: self.sci_button_click(t),
                                         (colors['sci_btn'], colors['sci_text'], colors['sci_btn_hover']),
                                         row_idx, col_idx, btn_font=self.sci_font, width=8, height=1)
                self.buttons[text] = btn

    def toggle_sci_panel(self):
        texts = self.theme["texts"]
        if not self.visible:
            self.sci_panel.pack(fill='x', pady=(0, 10), before=self.keyboard_frame)
            self.sci_toggle_btn.config(text=texts["sci_toggle_open"])
            self.root.geometry(self.geometry_expanded)
        else:
            self.sci_panel.pack_forget()
            self.sci_toggle_btn.config(text=texts["sci_toggle_closed"])
            self.root.geometry(self.geometry_default)
        self.visible = not self.visible

    def toggle_trig_mode(self):
        self.trigonometry_mode = "RAD" if self.trigonometry_mode == "DEG" else "DEG"
        prefix = self.theme["texts"]["mode_label_prefix"]
        self.mode_label.config(text=f"{prefix}{self.trigonometry_mode}")

    def sci_button_click(self, text):
            try:
                if self.input:
                    value = float(self.input)
                else:
                    value = 0
                
                result = None
                if self.trigonometry_mode == "DEG" and text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                    angle_value = math.radians(value)
                else:
                    angle_value = value
                
                if text == 'sin':
                    result = math.sin(angle_value)
                elif text == 'cos':
                    result = math.cos(angle_value)
                elif text == 'tan':
                    result = math.tan(angle_value)
                elif text == 'asin':
                    result = math.asin(value) if -1 <= value <= 1 else None
                    if result is not None and self.trigonometry_mode == "DEG":
                        result = math.degrees(result)
                elif text == 'acos':
                    result = math.acos(value) if -1 <= value <= 1 else None
                    if result is not None and self.trigonometry_mode == "DEG":
                        result = math.degrees(result)
                elif text == 'atan':
                    result = math.atan(value)
                    if self.trigonometry_mode == "DEG":
                        result = math.degrees(result)
                
                elif text == 'π':
                    self.input = str(math.pi)
                    self.update_display()
                    return
                elif text == 'e':
                    self.input = str(math.e)
                    self.update_display()
                    return
                
                elif text == 'log':
                    result = math.log10(value) if value > 0 else None
                elif text == 'ln':
                    result = math.log(value) if value > 0 else None
                elif text == '√':
                    result = math.sqrt(value) if value >= 0 else None
                elif text == 'x²':
                    result = value ** 2
                elif text == 'x³':
                    result = value ** 3
                elif text == '10^x':
                    result = 10 ** value
                elif text == '1/x':
                    result = 1 / value if value != 0 else None
                elif text == 'x!':
                    if value >= 0 and value.is_integer():
                        result = math.factorial(int(value))
                    else:
                        result = math.gamma(value + 1)
                elif text == '|x|':
                    result = abs(value)
                elif text == '(':
                    self.input += '('
                    self.update_display()
                    return
                elif text == ')':
                    self.input += ')'
                    self.update_display()
                    return
                elif text == '^':
                    self.handle_operation('^')
                    return
                
                if result is None:
                    self.display.set("Error")
                    return
                
                if abs(result) < 1e-10:
                    result = 0
                
                if abs(result - round(result, 10)) < 1e-10:
                    result = round(result, 10)
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                
                self.input = str(result)
                self.update_display()
                
            except Exception as e:
                self.display.set("Error")
                self.input = ""

    def button_click(self, text):
        self.highlight_button(text)
        
        if text.isdigit() or text == '.':
            self.handle_number_input(text)
        elif text in ['+', '-', '*', '/', '%', '^']:
            self.handle_operation(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
    
    def handle_number_input(self, num):
        if self.second_value:
            self.input = ""
            self.second_value = False
        
        if num == '.':
            if '.' not in self.input:
                if self.input == "":
                    self.input = "0."
                else:
                    self.input += "."
        else:
            if self.input == "0":
                self.input = num
            else:
                self.input += num
        
        self.update_display()

    def handle_operation(self, op):
        if self.input:
            if self.first_value is not None and not self.second_value:
                self.calculate()
            
            self.first_value = float(self.input)
            self.operation = op
            self.second_value = True
            
            display_op = op
            if op == '*':
                display_op = '×'
            elif op == '/':
                display_op = '÷'
            elif op == '^':
                display_op = '^'
            
            self.display.set(f"{self.input} {display_op}")
    
    def calculate(self):
        if self.first_value is not None and self.operation and self.input:
            try:
                second_number = float(self.input)
                
                if self.operation == '+':
                    result = self.first_value + second_number
                elif self.operation == '-':
                    result = self.first_value - second_number
                elif self.operation == '*':
                    result = self.first_value * second_number
                elif self.operation == '/':
                    if second_number == 0:
                        self.display.set("Error")
                        self.clear()
                        return
                    result = self.first_value / second_number
                elif self.operation == '%':
                    result = self.first_value % second_number
                elif self.operation == '^':
                    result = self.first_value ** second_number
                
                if abs(result) < 1e-10:
                    result = 0
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                
                self.display.set(str(result))
                self.input = str(result)
                self.first_value = None
                self.operation = None
                self.second_value = False
                
            except Exception as e:
                self.display.set("Error")
                self.clear()
    
    def clear(self):
        self.input = ""
        self.display.set("0")
        self.first_value = None
        self.operation = None
        self.second_value = False
    
    def backspace(self):
        if self.input:
            self.input = self.input[:-1]
            if not self.input:
                self.input = "0"
            self.update_display()
    
    def update_display(self):
        if self.input == "":
            self.display.set("0")
        else:
            if len(self.input) > 15:
                try:
                    num = float(self.input)
                    if abs(num) > 1e12 or (abs(num) < 1e-4 and num != 0):
                        self.display.set(f"{num:.4e}")
                    else:
                        self.display.set(f"{num:.8g}")
                except:
                    self.display.set(self.input[:15] + "...")
            else:
                self.display.set(self.input)

    def bind_keys(self):
        for key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.root.bind(key, lambda event, k=key: self.key_press(k))
        
        self.root.bind('+', lambda event: self.key_press('+'))
        self.root.bind('-', lambda event: self.key_press('-'))
        self.root.bind('*', lambda event: self.key_press('*'))
        self.root.bind('/', lambda event: self.key_press('/'))
        
        self.root.bind('.', lambda event: self.key_press('.'))
        self.root.bind('<Return>', lambda event: self.key_press('='))
        self.root.bind('<BackSpace>', lambda event: self.key_press('⌫'))
        self.root.bind('<Delete>', lambda event: self.key_press('C'))
        self.root.bind('<Escape>', lambda event: self.key_press('C'))
        self.root.bind('c', lambda event: self.key_press('C'))
        self.root.bind('C', lambda event: self.key_press('C'))
        self.root.bind('%', lambda event: self.key_press('%'))
        
        self.root.bind('<F2>', lambda event: self.toggle_sci_panel())
    
    def key_press(self, key):
        if key in self.buttons:
            self.highlight_button(key)
        
        if key.isdigit() or key == '.':
            self.handle_number_input(key)
        elif key in ['+', '-', '*', '/', '%']:
            self.handle_operation(key)
        elif key == '=':
            self.calculate()
        elif key == 'C':
            self.clear()
        elif key == '⌫':
            self.backspace()
    
    def highlight_button(self, key):
        if key in self.buttons:
            btn = self.buttons[key]
            original_bg = btn.cget('bg')
            
            if key in ['C', '⌫', '%']:
                highlight_color = self.colors['special_btn_hover']
            elif key in ['+', '-', '*', '/', '=']:
                highlight_color = self.colors['op_btn_hover']
            elif key.isdigit() or key == '.':
                highlight_color = self.colors['num_btn_hover']
            elif key in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'π', 'e', 'log', 'ln', '√', 'x²', 'x³', '10^x', '1/x', 'x!', '(', ')', '|x|', '^']:
                highlight_color = self.colors['sci_btn_hover']
            else:
                return
            
            btn.config(bg=highlight_color)
            self.root.after(100, lambda: btn.config(bg=original_bg))

def main():
    root = tk.Tk()
    app = Calculator(root, theme_file="theme.json")
    root.mainloop()

if __name__ == "__main__":
    main()
