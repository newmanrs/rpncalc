# Basic Python3.10 command line RPN calculator

# Installation

Clone repository and `pip3 install ./rpncalc` to install the calculator.

## Usage
Calling `rpncalc` with no arguments will print a list of commands available to the calculator.  A likely out of date example of the help page is below.

```
Reverse Polish Calculator on input argument strings.  An example `rpncalc 1 2 +`
  should push 3 to the stack.  The available operators are:
 BinaryOperators:
  +, -, *, /, //, ^, atan2, log_base, =, >, >=, <, <=, choose, combo, %, divmod
 UnaryOperators:
  sin, cos, tan, acos, asin, atan, int, exp, expmxsq, !, ln, log10, sqrt, 1/x,
  uminus
 IdempotentOperators:
  print, print_sv, print_store, print_state, quit, exit
 ReductionOperators:
  sum, prod, mean, max, min, stdev, sem, var
 LinearAlgebraOperators:
  vec2, vec3, veca, vecn, dot, cross, mat2, mat3, matsq, matmn, det, inv, T,
  e_x, e_y, e_z, hstack, vstack, reshape, normalize, norm, to_stack
 Constants:
  true, false, pi, tau, e, c, h, mu0, Na, kb, R, G, g, m_e, m_p, m_n
 StateOperators:
  clear, clear_storage, swap2, reverse, pop, save, load, repeatn
 RandomOperators:
  rand, coin, normal, d2, d4, d6, d8, d10, d12, d20, d100
 HistoryOperators:
  history, get_history

Use help(cmd) or help_cmd for detailed help on specific operators such as
  help_matsq

Flags:
 --verbose, -v. Print how the stack is processed
 --interactive, -i. Launch interactive input loop
 --load, -l.  Load from specified snapshot file
 --debug. Set breakpoints after expression evalution
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

## Design

This was built as an experiment of using python emums with match statements for python3.10.  Input strings are cast to callable enum classes, and then processed via a stack. Perhaps not wholly wise to implement an RPN calculator using these tools (see the `__new__` override in the `ActionEnum` class), as well as the potentially overcomplicated creation of the cli help.  Adding a bash-like history and interactive modes for the calculator were surprisingly simple.
