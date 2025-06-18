# Amazon Interview Preparation - Question #150
# Convert Postfix Expression to Infix
#
# Problem Statement:
# Given a postfix expression as a string, convert it into a valid infix expression.
# The expression contains single-letter operands (like a, b, c, ...) and operators (+, -, *, /).
#
# Example:
# Input: "ab+c*"
# Output: "((a+b)*c)"
#
# Rules:
# - Assume the input is a valid postfix expression.
# - The output infix expression should preserve the order of operations with appropriate parentheses.
#
# Write a function: def postfix_to_infix(expression: str) -> str
#
# You can now write your solution below.


def postfix_to_infix(tokens):
    stack = []
    for token in tokens:
        if token in "+-*/":
            b = stack.pop()
            a = stack.pop()
            combined = f"({a}{token}{b})"
            stack.append(combined)
        else:
            stack.append(token)
    return stack[-1]

print(postfix_to_infix("ab+c*"))  # Output: ((a+b)*c)
print(postfix_to_infix("ab+cd+*"))  # Output: ((a+b)*(c+d))
