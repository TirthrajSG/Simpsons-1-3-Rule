# Help - Simpsons 1/3 and 3/8 Rule Simulator

Welcome to the **Simpsons 1/3 and 3/8 Rule Simulator**! This tool allows you to compute definite integrals using **Simpson's 1/3 rule**, **Simpson's 3/8 rule**, and also shows the **actual integral value**.

---

## 1. Entering a Function

- Use the **Expression f(x)** field to enter a mathematical function of `x`.
- Supported operations and functions:
  - Basic arithmetic: `+`, `-`, `*`, `/`, `**` (power)
  - Constants: `e`, `π`
  - Functions: `sin()`, `cos()`, `tan()`, `csc()`, `sec()`, `cot()`, `asin()`, `acos()`, `atan()`, `acsc()`, `asec()`, `acot()`, `ln()`, `log()`, `sqrt()`, `root()`, `abs()`
  - Calculus: `diff()`, `limit()`, `Sum()`, `Prod()`, `integ()`

---

## 2. Functions Syntax:
  - **Trignometric Functions:** 
    - `sin()`-> `sin(x)`
    - `asin()`-> `asin(x)`
  - **Calculus Functions:**
    - `diff()` -> `diff(f(x), x)`: derivative of f(x) wrt x
    - `limit()` -> `limit(f(x), x, a)`: limit of f(x) at x=a
    - `Sum()` -> `Sum(f(i), (i, a, b))`: Summation of f(i) where i = {a,....,b}
    - `Prod()` -> `Product(f(i), (i, a, b))`: Product of f(i) where i = {a,....,b}
    - `integ()` -> `integrate(f(x), (x, a, b))`: Integrate f(x) wrt x from x=a to x=b
    - `integ()` -> `integrate(f(x), x)`: Indefinite Integrate of f(x) wrt x

### Examples:

| Input          | Description |
|----------------|-------------|
| `x**2 + 3*x`   | Polynomial function |
| `sin(x)`       | Sine function |
| `ln(x)`        | Natural logarithm (x > 0) |
| `sqrt(x)`      | Square root (x ≥ 0) |
| `diff(x**3, x)`| Derivative of x³ |

---

## 3. Integration Settings

- **x = a to x = b**: Define the interval of integration.
- **n intervals**: Number of subintervals for Simpson’s rules.
  - For **1/3 rule**, `n` must be even.
  - For **3/8 rule**, `n` must be a multiple of 3.
  - If your input does not satisfy these conditions, the simulator automatically adjusts `n`.

---

## 4. Buttons Overview

- **Evaluate**: Computes the integral using Simpson's 1/3, 3/8 rules, and shows the actual value.
- **Simplify**: Parses the expression and shows a preview plot of the function.
- **Undo**: Reverts the last change in the expression field.
- **Clear**: Clears the expression and all results.
- **Help**: Opens this help window.

- **Function Buttons**: Click to quickly insert functions like `sin()`, `cos()`, `ln()`, `nCr()`, `Sum()`, etc.

---

## 5. Plotting

- The **Plot of f(x)** section shows:
  - Function preview when simplified.
  - Shaded area under the curve for better visualization.
- Only expressions with variable `x` can be plotted. Constants will show a horizontal line.

---

## 6. Examples

### 1. Simple Polynomial
- Function: `x**2`
- Interval: `0 to 5`
- n = 4
- Click **Simplify** → see plot
- Click **Evaluate** → see Simpson's 1/3, 3/8, and actual integral

### 2. Trigonometric Function
- Function: `sin(x)`
- Interval: `0 to π`
- n = 6
- Click **Simplify** → see plot
- Click **Evaluate** → compare numerical results with actual value

### 3. Logarithmic Function
- Function: `ln(x)`
- Interval: `1 to 5`
- n = 4
- Click **Simplify** → see plot
- Click **Evaluate** → results

---

## 7. Notes & Tips

- If the function is undefined for some values (like `sqrt(-1)`), Simpson's rules treat it as 0 for numerical evaluation.
- Always **simplify** the function before evaluating.
- Use the **theme menu** to change UI themes for better visibility.
- Results are rounded to **2 decimal places** for readability.
- For advanced functions like `Sum()` or `Prod()`, make sure to follow the syntax:  
  `Sum(f(i), (i, a, b))` or `Prod(f(i), (i, a, b))`

---

## 8. Troubleshooting

- **Error: Invalid function** → Check syntax or supported functions.
- **Plot not displayed** → Ensure the expression has variable `x`.
- **NaN values in integral** → Some input values are out of domain; adjust the interval or function.

---

Thank you for using the **Simpsons 1/3 and 3/8 Rule Simulator**!  

