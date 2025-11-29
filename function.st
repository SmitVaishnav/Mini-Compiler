print("--- FUNCTION TEST ---")

def add(a, b) {
    return a + b
}

def factorial(n) {
    if (n < 2) {
        return 1
    }
    return n * factorial(n - 1)
}

let result = add(10, 20)
print("Addition Result: " + result)

let fact = factorial(5)
print("Factorial of 5: " + fact)