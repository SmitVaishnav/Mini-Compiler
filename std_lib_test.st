print("--- STANDARD LIBRARY TEST ---")

# 1. Input and String conversion
let name = input("What is your name? ")
print("Hello, " + name)

# 2. Length check
let length = len(name)
print("Your name has " + length + " letters.")

# 3. Random Number Game
print("I am picking a number between 0 and 10...")
let lucky = int(random() * 10)

let guess = int(input("Guess the number: "))

if (guess == lucky) {
    print("WOW! You guessed it!")
} else {
    print("Sorry, the number was " + lucky)
}

# 4. Timing code execution
print("Calculating something heavy...")
let start = time()

let sum = 0
for (let i = 0; i < 10000; i = i + 1) {
    let sum = sum + 1
}

let end = time()
let duration = end - start
print("That took " + duration + " seconds.")