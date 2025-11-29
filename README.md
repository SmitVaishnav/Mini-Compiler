# ⚡ SmitScript (Custom Interpreter)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Completed-orange?style=for-the-badge)

A robust, Turing-complete programming language interpreter built entirely from scratch in Python. 

> **Note:** This project uses **zero** external parsing libraries (like `ply` or `antlr`). Every stage of the compiler pipeline—Lexing, Parsing, and Interpreting—was hand-engineered to understand the core fundamentals of Computer Science.

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Installation & Usage](#-installation--usage)
- [Language Syntax](#-language-syntax)
- [Standard Library](#-standard-library)
- [Future Roadmap](#-future-roadmap)

---

## 🧠 About the Project

I built this language to demystify the "black box" of compilers. It moves beyond simple arithmetic expression evaluators into a fully featured language with memory management, function scopes, and complex data structures.

It features a **Recursive Descent Parser** constructing an **Abstract Syntax Tree (AST)**, which is executed by a custom **Tree-Walk Interpreter**.

---

## ✨ Key Features

* **Primitive Types:** Integers (`123`) and Strings (`"Hello World"`).
* **Data Structures:** Native support for Arrays/Lists (`[1, 2, 3]`) with indexing (`arr[0]`).
* **Variables:** Strong variable binding with `let` and dynamic updates.
* **Control Flow:** Full support for `if/else` conditionals, `while` loops, and C-style `for` loops.
* **Functions:** First-class functions with support for **Recursion** and local scope (stack frames).
* **Comments:** Support for single-line comments using `#`.
* **Standard Library (FFI):** A Foreign Function Interface bridging Python's native `math`, `time`, and `random` libraries into the language.
* **Tooling:** Includes a REPL (Read-Eval-Print Loop) for interactive coding and a CLI for file execution.

---

## 🏗 Architecture

The interpreter follows a classic 3-stage pipeline:

1.  **Lexer (Tokenizer):** * Reads raw source code characters.
    * Outputs a stream of `Token` objects (e.g., `INTEGER`, `ID`, `PLUS`, `DEF`).
    * Handles string parsing and comment skipping.

2.  **Parser:**
    * Uses **Recursive Descent** strategy.
    * Parses the token stream according to defined grammar rules.
    * Handles operator precedence (PEMDAS) and nesting.
    * Outputs an **Abstract Syntax Tree (AST)**.

3.  **Interpreter:**
    * Traverses the AST recursively.
    * Manages the **Runtime Environment** via a stack of Symbol Tables (scopes).
    * Executes logic and handles Python-to-SmitScript type conversions.

---

## 🚀 Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)[SmitVaishnav]/[Mini-Compiler].git
cd [Mini-Compiler]
```

### 2. Run the REPL (Interactive Shell)
Simply run the script without arguments to enter the interactive mode. It supports multi-line input (brace counting).

```Bash
python3 run.py
```

Output:
```Bash
Welcome to the MiniLang REPL! Type 'exit' to quit.
lang> print("Hello World")
Hello World
```

### 3. Run a Script File
Create a file with the .st extension (e.g., demo.st) and run it.

```Bash
python3 run.py demo.smit
```
📝 Language Syntax
Variables & Types
```JavaScript

let x = 10
let name = "Smit"
let list = [1, 2, 3]

# Reassignment
x = x + 5
```
Control Flow
```JavaScript

if (x > 10) {
    print("X is large")
} else {
    print("X is small")
}

let i = 0
while (i < 5) {
    print(i)
    i = i + 1
}

# C-Style For Loops
for (let k = 0; k < 10; k = k + 1) {
    print(k)
}
```
Functions & Recursion
```JavaScript

def add(a, b) {
    return a + b
}

# Recursive Factorial
def factorial(n) {
    if (n < 2) { return 1 }
    return n * factorial(n - 1)
}

print(factorial(5)) # Output: 120
```
