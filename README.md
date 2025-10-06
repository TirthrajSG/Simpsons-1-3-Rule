# Simpson's Integration Simulator

**Simpson's Integration Simulator** is a Python GUI application built with **Tkinter**. It allows users to input mathematical functions, calculate definite integrals using Simpson’s 1/3 rule and Simpson's 3/8 rule and visualize both the exact and approximate integral values. The app supports function plotting, expression simplification, and customizable themes.

---

## Features

- Enter mathematical expressions involving `x`.
- Calculate definite integrals using Simpson's 1/3 rule.
- Calculate definite integrals using Simpson's 3/8 rule.
- Plot functions with a clean, customizable interface.
- View simplified expressions in LaTeX format.
- Theme support for different color schemes.
- Interactive buttons for common functions and operations.

---

## Supported Functions

- **Arithmetic:** `+`, `-`, `*`, `/`, `**`
- **Trigonometric:** `sin()`, `cos()`, `tan()`, `csc()`, `sec()`, `cot()`
- **Inverse Trigonometric:** `asin()`, `acos()`, `atan()`, `acsc()`, `asec()`, `acot()`
- **Exponential & Logarithmic:** `e`, `π`, `ln()`, `log()`, `sqrt()`, `root()`
- **Combinatorics:** `nPr()`, `nCr()`, `lcm()`, `gcd()`
- **Calculus:** `diff()`, `limit()`, `integ()`, `Sum()`, `Prod()`

---

## How to use?

-**Step 1:** Enter a function of x in the text box. You can use the buttons on right panel. For more info click `Help` button.

-**Step 2:** Input the values of a, b, n in the text boxes.

-**Step 3:** Simplify the function using the `Simplify` button. These will simplify the integral and plot it.

-**Step 4:** Finally, Evaluate the integral using `Evaluate` button to get actual integral, simpson's 1/3 and 3/8 integral.

-**Change Theme:** Change theme using the `Drop Down` Button on top right corner.

---

## Installation

- Clone the Application:
```bash
git clone https://github.com/TirthrajSG/Simpsons-Integration-Rules.git
```

- Change directory to `Simpsons-Integration-Rules`:
```bash
cd Simpsons-Integration-Rules
```

- Install dependencies:

```bash
pip install -r requirements.txt
```
OR
```bash
pip install pillow matplotlib numpy sympy markdown tkinterweb 
```

- Run the application:
```bash
python .\main.py
```

---