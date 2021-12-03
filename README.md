# Basic Python3.10 command line RPN calculator

# Installation

Clone repository and `pip3 install ./rpncalc` to install the calculator.

## Usage
Calling `rpncalc` with no arguments will print a list of commands available to the calculator.  A likely out of date example of the help page is below.

```
Displaying help.
Pass integers or numbers to script and apply one or more of the following operators:
Idempotent Operators: ('print', 'print_sv', 'print_store', 'quit', 'exit')
Unary Operators: ('sin', 'cos', 'tan', 'acos', 'asin', 'atan', 'int', 'exp', 'expmxsq', '!', 'ln', 'log10', 'sqrt', '1/x', 'uminus')
Binary Operators: ('+', '-', '*', '/', '//', '^', 'atan2', 'log_base', '=', '>', '>=', '<', '<=', 'choose', 'combo')
Reduction Operators: ('sum', 'prod', 'mean', 'max', 'min', 'stdev', 'sem', 'var')
Linear Algebra Operators ('vec2', 'vec3', 'veca', 'vecn', 'dot', 'cross', 'mat2', 'mat3', 'matsq', 'matmn', 'det', 'inv', 'T', 'e_x', 'e_y', 'e_z', 'hstack', 'vstack', 'repeat', 'reshape', 'normalize', 'norm', 'to_stack')
Stack Operators ('clear', 'swap2', 'reverse', 'pop')
Constants: ('pi', 'tau', 'e', 'c', 'h', 'mu0', 'Na', 'kb', 'R', 'G', 'g', 'm_e', 'm_p', 'm_n')

Use help(cmd) or help_cmd for help on specific operators such as help_matsq

--verbose, -v, to show how the stack is processed
--interactive, -i, for interactive input loop
```

Be wary that many commands involving certain characters must be encapsulated in quotes or your shell will expand them before passing them to the script.  Launching the script with `-iv` for interactive mode can be less hassle.

Incomplete commands will return the contents of the stack, such as `rpncalc 2 2 2 +` will return `[2, 4]`.

### Example: Stored Named Variables
Items can also be stored as named constants by prefixing the desired name with `store_`, to be retrieved by prefixing an `_` later.  These variables are stored in a dictionary and can be accessed until overwritten.  A usage example calculating the vapor pressure of ethanol via Antoine's equation (A 3-parameter fit of 10^(A-B/(C+T)) at T=78.32C is given below.  Units for the fit coefficients are most not SI, and give ye olde mmHg.

`rpncalc -v 8.2042 store_A 1642.9 store_B 230.30 store_C 10 _A _B _C 78.32 + / - ^`
gives output:
```
Stack: [8.2042]
Popping stack into stored value _A
Stack: [1642.9]
Popping stack into stored value _B
Stack: [230.3]
Popping stack into stored value _C
Stack: [10]
Pushing stored value _A to stack
Stack: [10, 8.2042]
Pushing stored value _B to stack
Stack: [10, 8.2042, 1642.9]
Pushing stored value _C to stack
Stack: [10, 8.2042, 1642.9, 230.3, 78.32]
Applying BinaryOperator.addition
Stack: [10, 8.2042, 1642.9, 308.62]
Applying BinaryOperator.division
Stack: [10, 8.2042, 5.323375024301731]
Applying BinaryOperator.subtraction
Stack: [10, 2.8808249756982693]
Applying BinaryOperator.power
Stack: [760.0199208394923]
```

### Example: Matrix Algebra

Example below is linear regression fitting `y=2+x` via inputting `x,y` datapoints and creating the Vandermonde matrix V, and solving for the coefficients of fit via a=(V<sup>T</sup>V)<sup>-1</sup>V<sup>T</sup>y.  This construction fits linear coefficients to the functions are applied in the columns of the matrix, in this case 0th and 1st degree terms of `x` for a line, but coefficients can be fit for any f(x).  

`rpncalc 0 1 2 3 4 veca store_x 2 3 4 5 6 veca store_y _x 0 ^ _x 1 ^ hstack store_V _V T _V dot inv _V T dot _y dot` gives the intercept and slope as:


```
Stack: [array([[2.],
       [1.]])]
```
