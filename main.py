# # main.py
# """Main entry point for the MiniLang interpreter."""

# from .lexer import Lexer
# from .parser import Parser
# from .interpreter import Interpreter
# from .errors import LexerError, ParserError


# def main():
#     print("Welcome to the MiniLang! Type 'exit' or press Ctrl+C to quit.")
#     interpreter = Interpreter()

#     while True:
#         try:
#             # 1. Get the first line
#             text = input('lang> ')
            
#             # 2. Check for open braces
#             # If we have more '{' than '}', the block is not finished.
#             open_braces = text.count('{')
#             close_braces = text.count('}')
            
#             while open_braces > close_braces:
#                 # Ask for more input with a different prompt
#                 line = input('...... ')
#                 text += " " + line # Add a space so words don't merge
                
#                 # Update our counts
#                 open_braces += line.count('{')
#                 close_braces += line.count('}')
#         except EOFError:
#             print("\nExiting.")
#             break
#         except KeyboardInterrupt:
#             print("\nExiting.")
#             break

#         if not text:
#             continue
#         if text.strip().lower() == 'exit':
#             print("Exiting calculator.")
#             break

#         try:
#             lexer = Lexer(text)
#             parser = Parser(lexer)
#             ast = parser.parse()
            
#             # --- RESTORED EXECUTION ---
#             result = interpreter.visit(ast)
            
#             # Only print if there is a return value (like from math)
#             if result is not None:
#                 print(result)
        
#         except (LexerError, ParserError) as e:
#             print(f"Syntax Error: {e}")
#         except NameError as e:
#             print(f"Runtime Error: {e}")
#         except Exception as e:
#             print(f"Runtime Error: {e}")


# if __name__ == '__main__':
#     main()


import sys
# We use relative imports because this file is inside the package
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import LexerError, ParserError

def execute(text, interpreter):
    """
    Parses and executes a single block of code.
    """
    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast = parser.parse()
        
        # Determine if we should print the result
        result = interpreter.visit(ast)
        return result
        
    except (LexerError, ParserError) as e:
        print(f"Syntax Error: {e}")
    except NameError as e:
        print(f"Runtime Error: {e}")
    except Exception as e:
        # Catch-all for other errors (like division by zero)
        print(f"Error: {e}")

def repl():
    """
    Run the Interactive Shell (Read-Eval-Print Loop).
    Includes logic for multi-line input using brace counting.
    """
    print("Welcome to the MiniLang REPL! Type 'exit' or press Ctrl+C to quit.")
    interpreter = Interpreter()

    while True:
        try:
            # 1. Get initial input
            text = input('lang> ')
            
            # 2. Brace Counting Logic for Multi-line support
            open_braces = text.count('{')
            close_braces = text.count('}')
            
            # Keep asking for input until braces match
            while open_braces > close_braces:
                line = input('... ')
                text += " " + line
                open_braces += line.count('{')
                close_braces += line.count('}')
            
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not text:
            continue
            
        if text.strip().lower() == 'exit':
            break
            
        # 3. Execute the accumulated text
        result = execute(text, interpreter)
        
        # In REPL mode, we print the result if there is one
        if result is not None:
            print(result)

def run_file(filename):
    """
    Reads a file from the disk and executes it.
    """
    if not filename.endswith('.st'):
        print(f"Error: Invalid file type. Please provide a '.st' file.")
        return
    try:
        with open(filename, 'r') as file:
            text = file.read()
        
        # We create a fresh interpreter for the file
        interpreter = Interpreter()
        execute(text, interpreter)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    """
    Main entry point. Decides whether to run REPL or a file.
    """
    # sys.argv[0] is the script name. 
    # sys.argv[1] is the first argument (filename).
    if len(sys.argv) >= 2:
        run_file(sys.argv[1])
    else:
        repl()


# if __name__ == '__main__':
#     main()
