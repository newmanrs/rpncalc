# Basic Python3.10 command line RPN calculator

# Installation

Clone repository and `pip3 install ./rpncalc` to install the calculator.

## Usage
Calling `rpncalc` with no arguments will print a list of commands available to the calculator.  A likely out of date example of the help page is below.

```
Displaying help.
Pass integers or numbers to script and apply one or more of the following operators:
Idempotent Operators: ('print', 'print_sv', 'print_store', 'quit')
Unary Operators: ('sin', 'cos', 'tan', 'acos', 'asin', 'atan', 'int', 'exp', 'expmxsq', '!', 'ln', 'sqrt', '1/x', 'uminus')
Binary Operators: ('+', '-', '*', '/', '//', '^', 'atan2', 'log_base', '=', '>', '>=', '<', '<=', 'choose', 'combo')
Reduction Operators: ('sum', 'prod', 'mean', 'max', 'min', 'stdev', 'sem', 'var')
Linear Algebra Operators ('vec2', 'vec3', 'veca', 'vecn', 'dot', 'cross', 'mat2', 'mat3', 'matsq', 'matmn', 'det', 'inv', 'T', 'e_x', 'e_y', 'e_z', 'hstack', 'vstack', 'repeat', 'reshape', 'normalize', 'norm', 'to_stack')
Stack Operators ('clear', 'swap2', 'reverse', 'pop')
Constants: ('pi', 'tau', 'e', 'c', 'h', 'mu0', 'Na', 'kb', 'R', 'G', 'g', 'me', 'mp', 'mn')

Use help(cmd) or help_cmd for help on specific operators such as help_matsq

--verbose, -v, to show how the stack is processed
--interactive, -i, for interactive input loop
Stack: []
```

Be wary that many commands involving certain characters must be encapsulated in quotes or your shell will expand them before passing them to the script.  Launching the script with `-iv` for interactive mode can be less hassle.

Incomplete commands will return the contents of the stack, such as `rpncalc 2 2 2 +` will return `[2, 4]`.

Some rudimentary vector support is provided.
`rpncalc -v 2 1 1 1 2 1 1 3 3 matsq inv 13 11 19 vec3 dot`
should give output as:
```
Stack: [2, 1, 1, 1, 2, 1, 1, 3, 3]
Applying LinearAlgebraOperator.to_matsq
Stack: [array([[2, 1, 1],
       [1, 2, 1],
       [1, 3, 3]])]
Applying LinearAlgebraOperator.inverse
Stack: [array([[ 0.6,  0. , -0.2],
       [-0.4,  1. , -0.2],
       [ 0.2, -1. ,  0.6]]), 13, 11, 19]
Applying LinearAlgebraOperator.to_vec3
Stack: [array([[ 0.6,  0. , -0.2],
       [-0.4,  1. , -0.2],
       [ 0.2, -1. ,  0.6]]), array([13, 11, 19])]
Applying LinearAlgebraOperator.dotproduct
Stack: [array([4., 2., 3.])]
```

