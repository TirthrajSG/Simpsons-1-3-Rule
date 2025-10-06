from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinterweb import HtmlFrame
from theme import Themes

from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from io import BytesIO
import markdown
import os

import numpy as np
import sympy as sp
from sympy import factorial
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Simpsons 1/3 and 3/8 rule simulator")
        self.master.geometry("700x500")
        self.master.state('zoomed')
        
        self.theme = Themes["Sepia Tone"]

        self.master.configure(bg=self.theme['bg'])
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # self.master.iconbitmap("imgs/icon.ico")

        # Variables
        self.simplified = False
        self.evaluated = False
        self.history = []
        self.frm_master = []
        self.btns_master = []
        self.btns_master_2 = []
        self.entry_master = []
        self.lbl_master = []

        

        # Main Frame <- Master
        self.main_frame = Frame(self.master, bg=self.theme['bg'])
        self.main_frame.pack(side=LEFT,fill=BOTH, expand=True)

        # Right Window Frame <- Master
        self.right_window_border = Frame(self.master, bg=self.theme['btn_bg_2'])
        self.right_window_border.config(width=220)
        self.right_window_border.pack_propagate(False)
        self.right_window_border.pack(side=RIGHT, fill=Y)

        self.right_window = Frame(self.right_window_border, bg=self.theme['bg'])
        self.right_window.pack(side=RIGHT, fill=Y, padx=10, pady=10)

        # Theme OptionMenu <- Right Window Frame <- Master
        self.theme_var = StringVar(value=Themes)
        self.theme_var.set("Sepia Tone")
        self.theme_menu = OptionMenu(self.right_window, self.theme_var, *Themes.keys(), command=self.change_theme)
        self.theme_menu.config(
            font=("Consolas", 14, "bold"),
            bg=self.theme["btn_bg_2"],
            fg=self.theme["fg"],
            activebackground=self.theme["btn_active_bg"],
            activeforeground=self.theme["fg"],
            relief="flat",
            bd=0
        )
        self.theme_menu.pack(fill=X, padx=5, pady=5)

        for key in ["Undo", "Clear", "Simplify","Evaluate"]:
            self.btn = Button(self.right_window,
                                    text=key,
                                    padx=0,
                                    activebackground=self.theme["btn_active_bg"],
                                    activeforeground=self.theme["fg"],
                                    bg=self.theme["btn_bg_2"],
                                    fg=self.theme["fg"],
                                    bd=0,
                                    font=("Consolas", 18, "bold"),
                                    relief="flat",
                                    command=lambda k=key: self.btn_clicked(k)       
                            )
            self.btn.pack(fill=X, padx=5, pady=5)
            self.btns_master_2.append(self.btn)

        # Button Frame <- Right Window Frame <- Master
        self.btn_frame = Frame(self.right_window, bg=self.theme['bg'])
        self.btn_frame.pack(fill=BOTH, expand=1, padx=5,pady=5)
        self.btn_frame.rowconfigure(0, weight=1)
        self.btn_frame.columnconfigure(0, weight=1)

        # Canvas Button <- Button Frame <- Right Window Frame <- Master
        self.btn_canvas = Canvas(self.btn_frame)
        self.btn_canvas.config(
            bg=self.theme['bg'],
            highlightthickness=0
        )
        self.btn_canvas.grid(row=0, column=0, sticky='nsew')
        self.btn_canvas.bind("<Configure>", self.on_canvas_configure)
        

        # Scrollbar for Button Frame <- Button Frame <- Right Window Frame <- Main Frame <- Master
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure(
            "Custom.Vertical.TScrollbar",
            gripcount=0,
            background=self.theme["btn_bg"],      # Color of the thumb
            darkcolor=self.theme["btn_bg_2"],       # Color of the border around the thumb
            lightcolor=self.theme["btn_bg_2"],      # Color of the border around the thumb
            troughcolor=self.theme["bg"],   # Color of the trough
            bordercolor=self.theme["btn_bg_2"],
            arrowcolor=self.theme["fg"]
        )
        self.style.map(
            "Custom.Vertical.TScrollbar",
            background=[("active", self.theme["btn_bg"]),      # Thumb color when hovered
                        ("!active", self.theme["btn_bg"])],    # Thumb color normal
            darkcolor=[("active", self.theme["btn_bg_2"]), ("!active", self.theme["btn_bg_2"])],
            lightcolor=[("active", self.theme["btn_bg_2"]), ("!active", self.theme["btn_bg_2"])],
            bordercolor=[("active", self.theme["btn_bg_2"]), ("!active", self.theme["btn_bg_2"])],
            arrowcolor=[("active", self.theme["fg"]), ("!active", self.theme["fg"])]
        )
        self.scroll_btn_canvas = ttk.Scrollbar(self.btn_frame, style="Custom.Vertical.TScrollbar", orient="vertical", command=self.btn_canvas.yview)
        self.scroll_btn_canvas.grid(row=0, column=1, sticky='ns')

        self.btn_canvas.configure(yscrollcommand=self.scroll_btn_canvas.set)
        
        # Scrollable Button Frame < -Canvas Button <- Button Frame <- Right Window Frame <- Main Frame <- Master
        self.scrl_btn_frame = Frame(self.btn_canvas, bg=self.theme['bg'])
        self.scrl_btn_frame_id = self.btn_canvas.create_window((0, 0), window=self.scrl_btn_frame, anchor="nw")

        
        self.scrl_btn_frame.bind("<Configure>", self.on_frame_configure)
        self.scrl_btn_frame.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.scrl_btn_frame.bind("<Leave>", lambda e: self._unbind_mousewheel())

        self.button_layout=[
            'x', 'e', 'π',
            'a**2', 'a**b', 'sqrt()', 'root()', 'ln()', 'log()',
            'sin()', 'cos()', 'tan()', 'csc()', 'sec()','cot()',
            'asin()', 'acos()', 'atan()', 'acsc()', 'asec()','acot()',
            'lcm()', 'gcd()', 'abs()', 'ceil()', 'floor()','round()',
            'sign()', 'Sum()', 'Prod()', 'diff()', 'limit()', 'integ()',
        ]
        self.add_buttons()

        self.title = Frame(self.main_frame, bg=self.theme["btn_bg_2"])
        self.title.pack(fill=X)

        self.title_lbl = Label(self.title, text="Simpsons 1/3 and 3/8 rule simulator"
                               , bg=self.theme["btn_bg_2"], fg=self.theme["fg"],font=("Consolas", 25, "bold"))
        self.title_lbl.pack()

        self.exp_frame = Frame(self.main_frame, bg=self.theme["bg"], height=100)
        self.exp_frame.pack(fill=X, padx=10, pady=10)

        self.exp_lbl = Label(self.exp_frame, text="Expression f(x):",bg=self.theme["bg"],
                            fg=self.theme["fg"],
                            font=("Consolas", 20)     
                        )
        self.exp_lbl.pack(side=LEFT, padx=5, pady=5)

        self.expression = Entry(self.exp_frame, 
                               bg=self.theme["entry_bg"],
                               fg=self.theme["entry_fg"],
                               font=("Consolas", 23),
                            )
        self.expression.pack(side=LEFT,expan=True, fill=X, padx=5, pady=5)

        self.abn_frame = Frame(self.main_frame, bg=self.theme["bg"])
        self.abn_frame.pack(fill=X, padx=10, pady=10)
        
        self.a_lbl = Label(self.abn_frame, text="Integrate f(x) from x = ",bg=self.theme["bg"],
                            fg=self.theme["fg"],
                            font=("Consolas", 20)     
                        )
        self.a_lbl.pack(side=LEFT, padx=5, pady=5)

        self.a_val = StringVar()
        self.a_val.set("-10")
        self.a = Entry(self.abn_frame, textvariable=self.a_val,
                               bg=self.theme["entry_bg"],
                               fg=self.theme["entry_fg"],
                               font=("Consolas", 23),
                               justify='center',
                               width=6
                            )
        self.a.pack(side=LEFT, padx=5, pady=5)

        self.b_lbl = Label(self.abn_frame, text=" to x = ",bg=self.theme["bg"],
                            fg=self.theme["fg"],
                            font=("Consolas", 20)     
                        )
        self.b_lbl.pack(side=LEFT, padx=5, pady=5)

        self.b_val = StringVar()
        self.b_val.set("10")
        self.b = Entry(self.abn_frame, textvariable=self.b_val,
                               bg=self.theme["entry_bg"],
                               fg=self.theme["entry_fg"],
                               font=("Consolas", 23),
                               justify='center',
                               width=6
                            )
        self.b.pack(side=LEFT, padx=5, pady=5)

        self.n_lbl = Label(self.abn_frame, text=" in n = ",bg=self.theme["bg"],
                            fg=self.theme["fg"],
                            font=("Consolas", 20)     
                        )
        self.n_lbl.pack(side=LEFT, padx=5, pady=5)

        self.n_val = StringVar()
        self.n_val.set("4")
        self.n = Entry(self.abn_frame, textvariable=self.n_val,
                               bg=self.theme["entry_bg"],
                               fg=self.theme["entry_fg"],
                               font=("Consolas", 23),
                               justify='center',
                               width=6
                            )
        self.n.pack(side=LEFT, padx=5, pady=5)
        
        self.nn_lbl = Label(self.abn_frame, text=" intervals.",bg=self.theme["bg"],
                            fg=self.theme["fg"],
                            font=("Consolas", 20)     
                        )
        self.nn_lbl.pack(side=LEFT, padx=5, pady=5)

        self.plot_grid = Frame(self.main_frame, bg=self.theme["bg"])
        self.plot_grid.pack(fill=BOTH, expand=TRUE)

        self.plot_grid.rowconfigure(0, weight=1)
        self.plot_grid.columnconfigure(0, weight=1)
        self.plot_grid.columnconfigure(1, weight=1)

        self.plot_frame = Frame(self.plot_grid, bg=self.theme["btn_bg_2"])
        self.plot_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.plot1 = Label(self.plot_frame, text="Plot of ∫f(x)dx", font=("Consolas", 15)
                          ,bg=self.theme["bg"], fg=self.theme["fg"])
        self.plot1.pack(fill=X, padx=3, pady=(3,0))

        self.plot = Label(self.plot_frame, font=("Consolas", 25)
                          ,bg=self.theme["bg"], fg=self.theme["fg"])
        self.plot.pack(fill=BOTH, expand=True, padx=3, pady=3)
        # self.plot.pack_propagate(False)

        self.sol_frm = Frame(self.plot_grid, bg=self.theme["btn_bg_2"])
        self.sol_frm.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        # self.sol_frm.pack_propagate(False)

        
        self.actual_lbl1 = Label(self.sol_frm, text="Actual Value of Integral", 
                                wraplength=300,font=("Consolas", 15), bg=self.theme["bg"],
                                  fg=self.theme["fg"])
        self.actual_lbl1.pack(fill=X,padx=3, pady=(3,0))

        self.actual_lbl = Label(self.sol_frm, 
                                wraplength=300,font=("Consolas", 25), bg=self.theme["bg"],
                                  fg=self.theme["fg"])
        self.actual_lbl.pack(fill=BOTH,expand=1,padx=3, pady=3)
        self.simpsons_lbl1 = Label(self.sol_frm, text="Simpson's 1/3 Value of Integral", 
                                  wraplength=350,font=("Consolas", 15), bg=self.theme["bg"],
                                  fg=self.theme["fg"])
        self.simpsons_lbl1.pack(fill=X,padx=3, pady=0)

        self.simpsons_lbl = Label(self.sol_frm, 
                                  wraplength=300,font=("Consolas", 25), bg=self.theme["bg"],
                                  fg=self.theme["fg"])
        self.simpsons_lbl.pack(fill=BOTH,expand=1,padx=3, pady=3)

        self.simplify_lbl1 = Label(self.sol_frm, text="Simpson's 3/8 Value of Integral", 
                                  wraplength=350,font=("Consolas", 15), bg=self.theme["bg"],
                                  fg=self.theme["fg"])
        self.simplify_lbl1.pack(fill=X,padx=3, pady=0)

        self.simplify_lbl = Label(self.sol_frm, 
                                  wraplength=300,font=("Consolas", 25), bg=self.theme["bg"],
                                  fg=self.theme["fg"])
        self.simplify_lbl.pack(fill=BOTH,expand=1,padx=3, pady=3)



        self.entry_master += [self.expression, self.a,self.b, self.n] + [self.plot]
        self.lbl_master += [self.exp_lbl, self.a_lbl, self.simplify_lbl,self.actual_lbl,self.simpsons_lbl,
                            self.b_lbl, self.n_lbl, self.nn_lbl, self.plot, self.plot1,
                            self.simplify_lbl1,self.actual_lbl1,self.simpsons_lbl1] 
        self.frm_master += [self.master,self.main_frame,self.exp_frame,self.plot_grid,
                            self.abn_frame,self.right_window, self.btn_frame,
                            self.btn_canvas,self.scrl_btn_frame]


    def change_theme_widgets(self):
        if self.evaluated: self.eval_expr()
        if self.simplified: self.simp_expr()
        for frm in self.frm_master:
            frm.configure(bg=self.theme['bg'])
        
        self.title.config(bg=self.theme['btn_bg_2'])
        self.plot_frame.config(bg=self.theme['btn_bg_2'])
        self.sol_frm.config(bg=self.theme['btn_bg_2'])
        self.right_window_border.config(bg=self.theme['btn_bg_2'])

        self.theme_menu.config(
            font=("Consolas", 14, "bold"),
            bg=self.theme["btn_bg_2"],
            fg=self.theme["fg"],
            activebackground=self.theme["btn_active_bg"],
            activeforeground=self.theme["fg"]
        
        )

        for ent in self.entry_master:
            ent.config(
                bg=self.theme["entry_bg"],
                fg=self.theme["entry_fg"],
            )

        for btn in self.btns_master:
            btn.config(
                activebackground=self.theme["btn_active_bg"],
                activeforeground=self.theme["fg"],
                bg=self.theme["btn_bg"],
                fg=self.theme["fg"],
                font=("Consolas", 14, "bold"),
            )
        for btn in self.btns_master_2:
            btn.config(
                activebackground=self.theme["btn_active_bg"],
                activeforeground=self.theme["fg"],
                bg=self.theme["btn_bg_2"],
                fg=self.theme["fg"],
                font=("Consolas", 18, "bold"),
            )

        self.title_lbl.config(bg=self.theme['btn_bg_2'], fg=self.theme["fg"])
        for lbl in self.lbl_master:
            lbl.config(bg=self.theme['bg'], fg=self.theme["fg"])
        
        self.style.configure(
            "Custom.Vertical.TScrollbar",
            gripcount=0,
            background=self.theme["btn_bg"],      # Color of the thumb
            darkcolor=self.theme["btn_bg_2"],       # Color of the border around the thumb
            lightcolor=self.theme["btn_bg_2"],      # Color of the border around the thumb
            troughcolor=self.theme["bg"],   # Color of the trough
            bordercolor=self.theme["btn_bg_2"],
            arrowcolor=self.theme["fg"]
        )
        self.style.map(
            "Custom.Vertical.TScrollbar",
            background=[("active", self.theme["btn_bg"]),      # Thumb color when hovered
                        ("!active", self.theme["btn_bg"])],    # Thumb color normal
            darkcolor=[("active", self.theme["btn_bg_2"]), ("!active", self.theme["btn_bg_2"])],
            lightcolor=[("active", self.theme["btn_bg_2"]), ("!active", self.theme["btn_bg_2"])],
            bordercolor=[("active", self.theme["btn_bg_2"]), ("!active", self.theme["btn_bg_2"])],
            arrowcolor=[("active", self.theme["fg"]), ("!active", self.theme["fg"])]
        )
        self.scroll_btn_canvas.config(style="Custom.Vertical.TScrollbar")
    
    def change_theme(self, theme_name):
        self.theme = Themes[theme_name]
        self.change_theme_widgets()

    def add_buttons(self):
        for key in self.button_layout:
            btn = Button(
                self.scrl_btn_frame,
                text=key,
                padx=0,
                activebackground=self.theme["btn_active_bg"],
                activeforeground=self.theme["fg"],
                bg=self.theme["btn_bg"],
                fg=self.theme["fg"],
                bd=0,
                font=("Consolas", 14, "bold"),
                relief="flat",
                command=lambda k=key: self.btn_clicked(k)
            )
            btn.pack(fill='x', expand=True, pady=3, padx=5)
            self.bind_mousewheel(btn)
            self.btns_master.append(btn)

    def on_frame_configure(self, event):
        self.btn_canvas.configure(scrollregion=self.btn_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
         self.btn_canvas.itemconfig(self.scrl_btn_frame_id, width=event.width)

    def _bind_mousewheel(self):
        self.btn_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self):
        self.btn_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.btn_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def bind_mousewheel(self, widget):
        widget.bind("<Enter>", lambda e: self.btn_canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        widget.bind("<Leave>", lambda e: self.btn_canvas.unbind_all("<MouseWheel>"))

    def undo(self): pass
    def simp_expr(self): 
        expr_str = f"integrate({self.expression.get()},x)"
        try:
            transformations = standard_transformations + (implicit_multiplication_application,)
            local_dict = {
                'ceil': sp.ceiling,
                'nPr': self.nPr,
                'nCr':sp.binomial,
                'e': sp.E,           
                'π': sp.pi,
                'sin': sp.sin,
                'cos': sp.cos,
                'tan': sp.tan,
                'cot': sp.cot,
                'sec': sp.sec,
                'csc': sp.csc,
                'ln': sp.ln,
                'sqrt': sp.sqrt
            }
            self.expr = parse_expr(expr_str, transformations=transformations, local_dict=local_dict)
            self.expr = sp.sympify(self.expr)

            if not self.expr.free_symbols:
                self.expr = self.expr.evalf()

            latex_str = f"$\\text{{Plot of }} \\int_{{a}}^{{b}}f(x) = {sp.latex(self.expr)} + c$"
            
            fig, ax = plt.subplots()
            ax.text(0.5,0.5, latex_str, fontsize=15, ha='center', va='center', color=self.theme["fg"])
            ax.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            buf = BytesIO()
            plt.savefig(buf, format='png',transparent=True, dpi=100, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            buf.seek(0)

            latex_img = Image.open(buf)
            latex_img = latex_img.crop(latex_img.getbbox())
            photo = ImageTk.PhotoImage(latex_img)
            self.plot1.config(text="", image=photo)
            self.plot1.image = photo

        except Exception as e:
            self.expr = ""
            messagebox.showerror("Error", f"Invalid function:\n{e}")
        
        try:
            a, b = float(self.a_val.get()), float(self.b_val.get())
            nn = 500
            if not hasattr(self, 'expr'):
                return
            expr = self.expr
            x = sp.symbols('x')
            
            variable = expr.free_symbols
            
            fig, ax = plt.subplots(facecolor=self.theme["plot_bg"])
            ax.set_facecolor(self.theme["plot_bg"])
            
            if not variable: # Constant
                X = np.linspace(a, b, nn)
                Y = [float(expr)] * nn
                ax.plot(X, Y, color=self.theme["accent_color"])
            
            elif variable=={x}: # 1D plot
                f = sp.lambdify(x, expr, 'numpy')
                X = np.linspace(a, b, nn)
                Y = f(X)
                ax.plot(X, Y, color=self.theme["accent_color"])
            else:
                messagebox.showinfo("Info", "Plotting only supported for expressions with x or x and y.")
                plt.close(fig)
                return

            # --- Style the plot axes and labels ---
            ax.set_xlabel('x')
            ax.tick_params(axis='x', colors=self.theme["fg"])
            ax.tick_params(axis='y', colors=self.theme["fg"])
            ax.xaxis.label.set_color(self.theme["fg"])
            ax.yaxis.label.set_color(self.theme["fg"])
            ax.title.set_color(self.theme["fg"])
            ax.spines['bottom'].set_color(self.theme["fg"])
            ax.spines['top'].set_color(self.theme["fg"])
            ax.spines['left'].set_color(self.theme["fg"])
            ax.spines['right'].set_color(self.theme["fg"])
            ax.grid(True, color=self.theme["btn_bg"], linestyle='--', linewidth=0.5)


            buf2 = BytesIO()
            plt.savefig(buf2, format='png', facecolor=fig.get_facecolor(), dpi=100, bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)
            buf2.seek(0)
            
            img = Image.open(buf2)
            photo = ImageTk.PhotoImage(img)
            self.plot.config(text="",image=photo)
            self.plot.image = photo
            self.simplified = True
        except Exception as e:
            messagebox.showerror("Plotting Error", f"An error occurred while plotting:\n{e}")

    def eval_expr(self): 
        if not hasattr(self, "expr"): messagebox.showerror("Simplify", f"Simplify the function first:") ;return
        try: self.simp_expr() 
        except Exception as e: return
        try:
            transformations = standard_transformations + (implicit_multiplication_application,)
            local_dict = {
                'ceil': sp.ceiling,
                'nPr': self.nPr,
                'nCr':sp.binomial,
                'e': sp.E,           
                'π': sp.pi,
                'sin': sp.sin,
                'cos': sp.cos,
                'tan': sp.tan,
                'cot': sp.cot,
                'sec': sp.sec,
                'csc': sp.csc,
                'ln': sp.ln,
                'sqrt': sp.sqrt
            }
            a = float(self.a_val.get())
            b = float(self.b_val.get())
            expr = self.expr
            expr_str = f"integrate({expr}, (x, {a}, {b}))"
            new_expr = parse_expr(expr_str, transformations=transformations, local_dict=local_dict)
            ACTUAL = new_expr.evalf()
            latex_str = f"$\\int_{{{round(a,2):.2f}}}^{{{round(b,2):.2f}}} f(x) = {round(ACTUAL,2):.2f}$"

            fig, ax = plt.subplots()
            ax.text(0.5,0.5, latex_str, fontsize=15, ha='center', va='center', color=self.theme["fg"])
            ax.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            buf = BytesIO()
            plt.savefig(buf, format='png',transparent=True, dpi=100, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            buf.seek(0)

            latex_img = Image.open(buf)
            latex_img = latex_img.crop(latex_img.getbbox())
            photo = ImageTk.PhotoImage(latex_img)
            self.actual_lbl.config(text="", image=photo)
            self.actual_lbl.image = photo

            SIMPSONS1 = self.simpsons1()
            latex_str = f"$\\int_{{{round(a,2):.2f}}}^{{{round(b,2):.2f}}} f(x) \\approx {round(SIMPSONS1,2):.2f}$"

            fig, ax = plt.subplots()
            ax.text(0.5,0.5, latex_str, fontsize=15, ha='center', va='center', color=self.theme["fg"])
            ax.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            buf = BytesIO()
            plt.savefig(buf, format='png',transparent=True, dpi=100, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            buf.seek(0)

            latex_img = Image.open(buf)
            latex_img = latex_img.crop(latex_img.getbbox())
            photo = ImageTk.PhotoImage(latex_img)
            self.simpsons_lbl.config(text="", image=photo)
            self.simpsons_lbl.image = photo

            SIMPSONS3 = self.simpsons3()
            latex_str = f"$\\int_{{{round(a,2):.2f}}}^{{{round(b,2):.2f}}} f(x) \\approx {round(SIMPSONS3,2):.2f}$"

            fig, ax = plt.subplots()
            ax.text(0.5,0.5, latex_str, fontsize=15, ha='center', va='center', color=self.theme["fg"])
            ax.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            buf = BytesIO()
            plt.savefig(buf, format='png',transparent=True, dpi=100, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            buf.seek(0)

            latex_img = Image.open(buf)
            latex_img = latex_img.crop(latex_img.getbbox())
            photo = ImageTk.PhotoImage(latex_img)
            self.simplify_lbl.config(text="", image=photo)
            self.simplify_lbl.image = photo

            self.evaluated = True



        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while solving:\n{e}")

    def simpsons3(self):
        n = int(self.n_val.get())
        a_val = float(self.a_val.get())
        b_val = float(self.b_val.get())

        # Simpson's 3/8 rule requires n to be a multiple of 3
        if n % 3 != 0:
            n += 3 - (n % 3)
            self.n_val.set(str(n))
        # Simpson's 1/3 rule requires n to be even
        if n % 2 == 1:
            self.n_val.set(str(n+1))
            n += 1

        x = sp.symbols('x')
        expr = self.expr

        def y(val):
            return expr.subs(x, val).evalf()

        h = (b_val - a_val) / n
        sum_ = y(a_val) + y(b_val)

        for i in range(1, n):
            xi = a_val + i * h
            # Coefficients: 3 for non-multiples of 3, 2 for multiples of 3
            weight = 3 if i % 3 != 0 else 2
            sum_ += weight * y(xi)

        integral = (3 * h / 8) * sum_
        return integral

    
    def simpsons1(self):
        n = int(self.n_val.get())
        a_val = float(self.a_val.get())
        b_val = float(self.b_val.get())

        # Simpson's 3/8 rule requires n to be a multiple of 3
        if n % 3 != 0:
            n += 3 - (n % 3)
            self.n_val.set(str(n))
        # Simpson's 1/3 rule requires n to be even
        if n % 2 == 1:
            self.n_val.set(str(n+1))
            n += 1

        x = sp.symbols('x')
        expr = self.expr

        def y(val):
            return expr.subs(x, val).evalf()

        h = (b_val - a_val) / n
        sum_ = y(a_val) + y(b_val)

        for i in range(1, n):
            xi = a_val + i*h
            weight = 4 if i % 2 == 1 else 2
            sum_ += weight * y(xi)

        integral = (h/3) * sum_
        return integral

    def nPr(self, n, r):
        return factorial(n) / factorial(n - r)
    
    def clear(self):
        self.history.append(self.expression.get())
        self.expression.delete(0, END)

        self.plot.config(image="")   
        self.plot1.config(image="")   
        self.plot1.config(text="Plot of ∫f(x)dx")   
        self.actual_lbl.config(image="")   
        self.simplify_lbl.config(image="")   
        self.simpsons_lbl.config(image="")

        self.evaluated = False
        self.simplified = False

    def btn_clicked(self, k):
        if k == "Evaluate": self.eval_expr();return
        elif k == "Simplify": self.simp_expr();return
        elif k == "Undo": self.undo(); return
        elif k == "Clear": self.clear(); return
        
        i = 1
        add = k
        if k not in ("<--", "Clear"):
            self.history.append(self.expression.get())

        if k == "a**2": add="**2"
        elif k == "a**b": add="**"
        elif k == "log()": add="log(a, b)"; i=4
        elif k == "root()": add="root(, n)"; i=4
        elif k == "nCr()": add="nCr(n, r)"; i=4
        elif k == "nPr()": add="nPr(n, r)"; i=4
        elif k == "lcm()": add="lcm(a, b)"; i=4
        elif k == "gcd()": add="gcd(a, b)"; i=4
        elif k == "Sum()": add = "Sum(f(i), (i, a, b))"; i = 12
        elif k == "Prod()": add="Product(f(i), (i, a, b))"; i=12
        elif k == "diff()": add="diff(f(x), x)"; i=4
        elif k == "limit()": add = "limit(f(x), x, a)";i=7
        elif k == "integ()": add="integrate(f(x), (x, a, b))"; i=12

        
        self.expression.insert(INSERT, add)
        if "(" in k and k.endswith(")"): 
            pos = self.expression.index(INSERT)
            if pos > 0: self.expression.icursor(pos-i)

if __name__ == "__main__":
    root = Tk()
    app =App(root)
    root.mainloop()
