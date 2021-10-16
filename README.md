# Basic Python3.10 command line RPN calculator

# Installation

Clone repository and `pip3 install ./rpncalc` to install the calculator.

## Usage
Calling `rpncalc` with no arguments will print a list of commands available to the calculator.  A likely out of date example of the help page is below.

```
No arguments to parse. Displaying help.
Pass integers or numbers to script and apply one or more of the following operators:

Constants: ('pi', 'tau', 'e', 'c', 'h', 'mu0', 'Na', 'kb', 'R', 'G', 'g', 'me', 'mp', 'mn')

Idempotent Operators: ('print',)

Unary Operators: ('sin', 'cos', 'tan', 'acos', 'asin', 'atan', 'int', 'exp', 'expmxsq', 'ln', 'sqrt', 'inv')

Binary Operators: ('+', '-', '*', '/', '//', '^', 'atan2', 'log_base', '=', '>', '>=', '<', '<=')

Reduction Operators: ('sum', 'prod', 'mean', 'max', 'min', 'stdev', 'sem', 'var')

Quote input to avoid shell expansion of special chars such as '*', '>'
```

Incomplete commands will return the contents of the stack, such as `rpncalc 2 2 2 +` will return `[2, 4]`.  
