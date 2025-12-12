import tkinter as tk
from tkinter import font
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x650")
        self.root.configure(bg='#121212')
        self.root.resizable(False, False)
        
        self.colors = {
            'bg': '#000000',              
            'display_bg': '#1c1c1c',    
            'display_fg': '#ffffff',      
            'num_btn': '#2e2e2e',        
            'num_btn_hover': '#3d3d3d',   
            'num_text': '#ffffff',       
            'op_btn': '#00d2be',         
            'op_btn_hover': '#33e6d4',   
            'op_text': '#000000',         
            'special_btn': '#a6a6a6',     
            'special_btn_hover': '#c0c0c0',
            'special_text': '#000000',
            'sci_btn': '#00d2be',         
            'sci_btn_hover': '#33e6d4',
            'sci_text': '#000000',
            'toggle_btn': '#444444',      
            'toggle_btn_hover': '#666666',
            'shadow': '#000000'
        }
        
        self.current_input = ""
        self.result_var = tk.StringVar(value="0")
        self.operation = None
        self.first_number = None
        self.second_number = False
        self.trig_mode = "DEG"
        self.panel_visible = False
        
        try:
            self.display_font = font.Font(family="Segoe UI", size=34, weight="normal")
            self.button_font = font.Font(family="Segoe UI", size=20, weight="normal")
            self.mode_font = font.Font(family="Segoe UI", size=12, weight="normal")
            self.sci_font = font.Font(family="Segoe UI", size=14, weight="normal")
        except:
            self.display_font = font.Font(size=34, weight="normal")
            self.button_font = font.Font(size=20, weight="normal")
            self.mode_font = font.Font(size=12, weight="normal")
            self.sci_font = font.Font(size=14, weight="normal")
        
        self.build()
        self.bind_keys()
    
    def create_button(self, parent, text, command, bg, fg, hover_bg, row, col, colspan=1, btn_font=None, width=8, height=2):
        if btn_font is None:
            btn_font = self.button_font
        
        btn = tk.Button(
            parent,
            text=text,
            font=btn_font,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            command=command,
            padx=10,
            pady=10,
            width=width,
            height=height
        )
        
        def on_enter(e):
            btn['bg'] = hover_bg
        
        def on_leave(e):
            btn['bg'] = bg
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        btn.grid(
            row=row,
            column=col,
            columnspan=colspan,
            sticky="nsew",
            padx=3,
            pady=3,
            ipadx=5,
            ipady=5
        )
        return btn
    
    def build(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        mode_frame = tk.Frame(main_container, bg=self.colors['bg'])
        mode_frame.pack(fill='x', pady=(0, 15))
        
        self.mode_label = tk.Label(
            mode_frame,
            text=f"Mode: {self.trig_mode}",
            font=self.mode_font,
            bg=self.colors['bg'],
            fg='#888888'
        )
        self.mode_label.pack(side='left')
        
        mode_btn = tk.Button(
            mode_frame,
            text="DEG/RAD",
            font=self.mode_font,
            command=self.toggle_mode,
            bg=self.colors['toggle_btn'],
            fg='white',
            activebackground=self.colors['toggle_btn_hover'],
            activeforeground='white',
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        )
        mode_btn.pack(side='right')
        
        display = tk.Frame(
            main_container,
            bg=self.colors['display_bg'],
            height=100
        )
        display.pack(fill='x', pady=(0, 20))
        
        display = tk.Label(
            display,
            textvariable=self.result_var,
            font=self.display_font,
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            anchor='e',
            padx=20,
            pady=25
        )
        display.pack(fill='both', expand=True)
        
        switch_frame = tk.Frame(main_container, bg=self.colors['bg'])
        switch_frame.pack(fill='x', pady=(0, 15))
        
        self.switch_btn = tk.Button(
            switch_frame,
            text="▼ Scientific Functions",
            font=self.sci_font,
            command=self.switch_panel,
            bg=self.colors['sci_btn'],
            fg='white',
            activebackground=self.colors['sci_btn_hover'],
            activeforeground='white',
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            pady=10
        )
        self.switch_btn.pack(fill='x')
        
        self.panel = tk.Frame(main_container, bg=self.colors['bg'], height=250)
        self.panel.pack_propagate(False) 

        self.keyboard = tk.Frame(main_container, bg=self.colors['bg'])
        self.keyboard.pack(fill='both', expand=True)
        
        for i in range(4):
            self.keyboard.grid_columnconfigure(i, weight=1, minsize=80)
        for i in range(5):
            self.keyboard.grid_rowconfigure(i, weight=1, minsize=70)
        
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', ''] 
        ]
        
        self.buttons_dict = {}
        
        for row_index, row in enumerate(buttons):
            for column_index, text in enumerate(row):
                if text == '':  
                    continue
                    
                colspan = 2 if text == '=' else 1
                col = column_index if text != '=' else 2  
                
                if text in ['C', '⌫', '%']:
                    bg = self.colors['special_btn']
                    fg = self.colors['special_text']
                    hover_bg = self.colors['special_btn_hover']
                elif text in ['/', '*', '-', '+', '=']:
                    bg = self.colors['op_btn']
                    fg = self.colors['op_text']
                    hover_bg = self.colors['op_btn_hover']
                else:
                    bg = self.colors['num_btn']
                    fg = self.colors['num_text']
                    hover_bg = self.colors['num_btn_hover']
                
                btn = self.create_button(
                    self.keyboard,
                    text,
                    lambda t=text: self.button_click(t),
                    bg,
                    fg,
                    hover_bg,
                    row_index,
                    col,
                    colspan,
                    width=10 if colspan == 2 else 8
                )
                
                self.buttons_dict[text] = btn
        
        self.build_panel()
    
    def build_panel(self):
        container = tk.Frame(self.panel, bg=self.colors['bg'])
        container.pack(fill='both', expand=True, padx=5, pady=5)
        
        for i in range(4):
            container.grid_columnconfigure(i, weight=1)
        for i in range(5):
            container.grid_rowconfigure(i, weight=1)
        
        sci_buttons = [
            ['sin', 'cos', 'tan', 'π'],
            ['asin', 'acos', 'atan', 'e'],
            ['log', 'ln', '√', 'x²'],
            ['x³', '10^x', '1/x', 'x!'],
            ['(', ')', '|x|', '^']
        ]
        
        for row_idx, row in enumerate(sci_buttons):
            for col_idx, text in enumerate(row):
                btn = tk.Button(
                    container,
                    text=text,
                    font=self.sci_font,
                    bg=self.colors['sci_btn'],
                    fg=self.colors['sci_text'],
                    activebackground=self.colors['sci_btn_hover'],
                    activeforeground=self.colors['sci_text'],
                    borderwidth=0,
                    relief='flat',
                    cursor='hand2',
                    command=lambda t=text: self.button_click(t),
                    padx=5,
                    pady=10
                )
                
                def on_enter(e, b=btn, h=self.colors['sci_btn_hover']):
                    b['bg'] = h
                
                def on_leave(e, b=btn, bg=self.colors['sci_btn']):
                    b['bg'] = bg
                
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
                
                btn.grid(
                    row=row_idx,
                    column=col_idx,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )
                
                self.buttons_dict[text] = btn
    
    def switch_panel(self):
        if not self.panel_visible:
            self.panel.pack(fill='x', pady=(0, 10), before=self.keyboard)
            self.switch_btn.config(text="▲ Engineer Functions")
            self.root.geometry("400x900")
        else:
            self.panel.pack_forget()
            self.switch_btn.config(text="▼ Engineer Functions")
            self.root.geometry("400x650")
        
        self.panel_visible = not self.panel_visible
    
    def toggle_mode(self):
        self.trig_mode = "RAD" if self.trig_mode == "DEG" else "DEG"
        self.mode_label.config(text=f"Mode: {self.trig_mode}")
    
    def button_click(self, text):
        try:
            if self.current_input:
                value = float(self.current_input)
            else:
                value = 0
            
            result = None
            
            if self.trig_mode == "DEG" and text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                geometry_value = math.radians(value)
            else:
                geometry_value = value
            
            if text == 'sin':
                result = math.sin(geometry_value)
            elif text == 'cos':
                result = math.cos(geometry_value)
            elif text == 'tan':
                result = math.tan(geometry_value)
            elif text == 'asin':
                result = math.asin(value) if -1 <= value <= 1 else None
                if result is not None and self.trig_mode == "DEG":
                    result = math.degrees(result)
            elif text == 'acos':
                result = math.acos(value) if -1 <= value <= 1 else None
                if result is not None and self.trig_mode == "DEG":
                    result = math.degrees(result)
            elif text == 'atan':
                result = math.atan(value)
                if self.trig_mode == "DEG":
                    result = math.degrees(result)
            
            elif text == 'π':
                self.current_input = str(math.pi)
                self.update()
                return
            elif text == 'e':
                self.current_input = str(math.e)
                self.update()
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
                self.current_input += '('
                self.update()
                return
            elif text == ')':
                self.current_input += ')'
                self.update()
                return
            elif text == '^':
                self.handle_operation('^')
                return
            
            if result is None:
                self.result_var.set("Error")
                return
            
            if abs(result) < 1e-10:
                result = 0
            
            if abs(result - round(result, 10)) < 1e-10:
                result = round(result, 10)
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            self.current_input = str(result)
            self.update()
            
        except Exception as exception:
            self.result_var.set("Error")
            self.current_input = ""
    
    def button_click(self, text):
        self.highlight_button(text)
        
        if text.isdigit() or text == '.':
            self.handle_input(text)
        elif text in ['+', '-', '*', '/', '%', '^']:
            self.handle_operation(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
    
    def handle_input(self, num):
        if self.second_number:
            self.current_input = ""
            self.second_number = False
        
        if num == '.':
            if '.' not in self.current_input:
                if self.current_input == "":
                    self.current_input = "0."
                else:
                    self.current_input += "."
        else:
            if self.current_input == "0":
                self.current_input = num
            else:
                self.current_input += num
        
        self.update()
    
    def handle_operation(self, operation):
        if self.current_input:
            if self.first_number is not None and not self.second_number:
                self.calculate()
            
            self.first_number = float(self.current_input)
            self.operation = operation
            self.second_number = True
            
            display_operation = operation
            if operation == '*':
                display_operation = '×'
            elif operation == '/':
                display_operation = '÷'
            elif operation == '^':
                display_operation = '^'
            
            self.result_var.set(f"{self.current_input} {display_operation}")
    
    def calculate(self):
        if self.first_number is not None and self.operation and self.current_input:
            try:
                second_number = float(self.current_input)
                
                if self.operation == '+':
                    result = self.first_number + second_number
                elif self.operation == '-':
                    result = self.first_number - second_number
                elif self.operation == '*':
                    result = self.first_number * second_number
                elif self.operation == '/':
                    if second_number == 0:
                        self.result_var.set("Error")
                        self.clear()
                        return
                    result = self.first_number / second_number
                elif self.operation == '%':
                    result = self.first_number % second_number
                elif self.operation == '^':
                    result = self.first_number ** second_number
                
                if abs(result) < 1e-10:
                    result = 0
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                
                self.result_var.set(str(result))
                self.current_input = str(result)
                self.first_number = None
                self.operation = None
                self.second_number = False
                
            except Exception as e:
                self.result_var.set("Error")
                self.clear()
    
    def clear(self):
        self.current_input = ""
        self.result_var.set("0")
        self.first_number = None
        self.operation = None
        self.second_number = False
    
    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = "0"
            self.update()
    
    def update(self):
        if self.current_input == "":
            self.result_var.set("0")
        else:
            if len(self.current_input) > 15:
                try:
                    num = float(self.current_input)
                    if abs(num) > 1e12 or (abs(num) < 1e-4 and num != 0):
                        self.result_var.set(f"{num:.4e}")
                    else:
                        self.result_var.set(f"{num:.8g}")
                except:
                    self.result_var.set(self.current_input[:15] + "...")
            else:
                self.result_var.set(self.current_input)
    
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
        
        self.root.bind('<F2>', lambda event: self.switch_panel())
    
    def key_press(self, key):
        if key in self.buttons_dict:
            self.highlight_button(key)
        
        if key.isdigit() or key == '.':
            self.handle_input(key)
        elif key in ['+', '-', '*', '/', '%']:
            self.handle_operation(key)
        elif key == '=':
            self.calculate()
        elif key == 'C':
            self.clear()
        elif key == '⌫':
            self.backspace()
    
    def highlight_button(self, key):
        if key in self.buttons_dict:
            btn = self.buttons_dict[key]
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
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()