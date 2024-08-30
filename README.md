# AST Manipulation - J-Dees
## 1. Project completion

I was able to implement the two required operations, additive identity and multiplicative identity. I also implemented the multiply by zero operation. For my testing framework, I decided not to use unittest, but rather made my own testbench that would navigate the files and run test cases similarly to unittest. Functionally, the operations succesfully manipulate the AST appropriately, the only test case that some operations fail is when a level 1 tree is not fully reduced. To fix this in the simplify_binops function, I called everything twice. Despite its inefficiency, this succeded in fully reducing all AST test cases that I produced.

## 2. Things I learned from this assignment

I felt the scope of this project was pretty complex, fortunately we were given two weeks to work on it. I was coming into this term with some minor knowledge of Python, but I have never built anything of this scope, so I feel like this project is a great way of familiarizing students with Python. This project is also great file io experience. Previously, I had only ever worked on single file io programs. I feel more comfortable with walking file directories now than I did before starting the assignment. This project is my first step into mastering Python as a scripting language, so thank you for assigning it to us.

## 3. Difficulty and Bug Descriptions

Walking the tree took me some time, my community college did not cover binary trees in our data structures course (it was the last chapter so I think Hancock usually skips it due to time constraints). I was still able to logically recurse through it and create an implementation from that, but the implementation was not perfect because some operations got stuck reducing to a level 1 tree. All the bugs I encountered were eventually fixed, I spent a lot of time with the VS Code Python debugger and it managed to help me fix a lot of errors in the operation and test framework code. I made a couple of attempts to restart my function code from scratch, but in the end I kept coming back to my solution and got it to work for the most part.
