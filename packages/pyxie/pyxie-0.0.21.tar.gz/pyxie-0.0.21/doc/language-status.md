## Language Status

Last updated for version: **0.0.17**

### Direct Compilation

Pyxie can now compile (directly) any file that matches pyxie's current subset of
python. For example if the example program below was called demo.pyxie, you could
do this:

    $ pyxie compile demo.pyxie
    $ ./demo

The first line would compile "demo.pyxie" to C++, then compile the C++, rename the
result "demo" and clean up after itself.

Python programs that target arduino can also be compiled directly on the commandline:

    $ pyxie --profile arduino compile tests/progs/arduino-for-blink.pyxie
    $ ls tests/progs/arduino-for-blink.hex
    tests/progs/arduino-for-blink.hex

In order to do this, you need the arduino tool chain installed, along with
commandline tools, but the easiest way of doing this is to do this:

    sudo apt-get install arduino-mk


## Example program that lexes, parses, analyses & compiles

Clearly a single example doesn't tell you everything. This gives you a flavour.

<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b>

<pre>
age = 10
new_age = 10 +1
new_age_too = age + 1
new_age_three = age + new_age_too
foo = "Hello"
bar = "World"
foobar = foo + bar

print 10-1-2,7
print 1+2*3*4-5/7,25
print age, new_age, new_age_too
print foo, bar, foobar

countdown = 2147483647
print "COUNTING DOWN"
while countdown:
    countdown = countdown - 1

print "BLASTOFF"
</pre>
</div>
<div class="column col3_5">
<b>Generated:</b>
<pre>
#include &lt;iostream&gt;
#include &lt;string&gt;

using namespace std;

int main(int argc, char *argv[])
{
    int age;
    string bar;
    int countdown;
    string foo;
    string foobar;
    int new_age;
    int new_age_three;
    int new_age_too;

    age = 10;
    new_age = (10+1);
    new_age_too = (age+1);
    new_age_three = (age+new_age_too);
    foo = "Hello";
    bar = "World";
    foobar = (foo+bar);
    cout &lt;&lt; ((10-1)-2) &lt;&lt; " " &lt;&lt; 7 &lt;&lt; endl;
    cout &lt;&lt; ((1+((2*3)*4))-(5/7)) &lt;&lt; " " &lt;&lt; 25 &lt;&lt; endl;
    cout &lt;&lt; age &lt;&lt; " " &lt;&lt; new_age &lt;&lt; " " &lt;&lt; new_age_too &lt;&lt; endl;
    cout &lt;&lt; foo &lt;&lt; " " &lt;&lt; bar &lt;&lt; " " &lt;&lt; foobar &lt;&lt; endl;
    countdown = 2147483647;
    cout &lt;&lt; "COUNTING DOWN" &lt;&lt; endl;
    while(countdown) {
        countdown = (countdown-1);
    };
    cout &lt;&lt; "BLASTOFF" &lt;&lt; endl;
    return 0;
}
</pre>
</div>
</div>


Supported language features that are not in this example

* Major control structures - in addition to while loops, if/elif/else, conditionals,
  boolean, parenthesised expressions and for statements/etc are all supported. Not
  only that for loops actually support an iterator protocol, not just translation of
  "range" into a simple C style for loop.

Note: for this to compile, this needs simple type inference. We need to be able to
derive the types of foobar and new_age_three. In the case of new_age_three, that
needs to be derived in the context of another variable that has to be derived from
another one.

The same techniques are used to derive types in "for statement" loop iterators.

### Function Calls

Function **calls** are supported. At present they are treated
as having a value type of "None".  They should be treated as statements
not as expressions. However the compiler passes through function calls
to the backend, assuming the backend will understand the function call.

Grammar wise though, they're things in expressions.

### C++ Libraries

Additionally, you can pull C++ libraries in standard locations by simply
incuding them -- for example:

    #include <Arduino.h>

This is ignored by the python parsing because it's a comment, and so I've
chosen to capture such #include lines, and pass them through to the C++ side.
This naturally enables a wide selection of functionality to start making
Pyxie useful.

### Very Nearly Bare Minimum Support

Now supports control structures, key statements

* while (arbitrary expression for control)
* for loops, where the general expression must be an iterable.
 * The only iterable at present is "range". This will get more expressive
* break/continue
* if/ elif / else
* print
* function calls
* assignment

Key expression support:

* Variables have their types inferred for int, bool, char, float, string, hex, binary, octal
* Parenthesised expressions
* Comparisons (>,<,>=,<=, !=,<>, ==)
* Boolean operators: and, or, not

This means we can almost start writing useful programs, but in particular
can start creating simplistic benchmarks for measuring run speed.

## High Level things missing

### Language related

From a high level the key things I view as missing are support for:

* def - function definitions - and therefore implementation of scope
* What happens with mixed types in expressions
* Modulo operator support
* import statements
* yield - generator definitions
* class - class definitions
* object usage - method access, and attribute access

There is obviously more missing, but these are the high level issues with pyxie's
implementation of language at present.

### Profile related

* Linux host profile:
 * Support for output (print) needs to be matched by (raw_)input support
 * Needs to support input/output from files

* Arduino profile:
 * Need to support the following things at minimum:
 * Constants:
  * OUTPUT, INPUT (pinModes)
  * HIGH, LOW (general pin values)
 * functions/etc
  * digitalWrite
  * delayMicroseconds
  * pinMode
  * analogRead
  * millis
 * Hardware devices/libraries etc
  * Servo
  * IOToy
  * prototype microbit

## Grammar Currently Supported

Clearly we're not going to implement the full language spec in one go, so this
documents the current version of the grammar that is supported. Parsing does not
necessarily imply code generation, differences will be noted below.

    program : statements
    statements : statement
               | statement statements

    statement_block : INDENT statements DEDENT

    statement : assignment_statement
              | print_statement
              | general_expression
              | EOL
              | while_statement
              | break_statement
              | continue_statement
              | pass_statement
              | if_statement
              | for_statement

    assignment_statement -> IDENTIFIER ASSIGN general_expression # ASSIGN is currently limited to "="

    while_statement : WHILE general_expression COLON EOL statement_block

    break_statement : BREAK

    pass_statement : PASS

    continue_statement : CONTINUE

    if_statement : IF general_expression COLON EOL statement_block
                 | IF general_expression COLON EOL statement_block extended_if_clauses

    extended_if_clauses : else_clause
                        | elif_clause

    else_clause : ELSE COLON EOL statement_block

    elif_clause : ELIF general_expression COLON EOL statement_block
                | ELIF general_expression COLON EOL statement_block extended_if_clauses

    print_statement : 'print' expr_list # Temporary - to be replaced by python 3 style function

    for_statement | FOR IDENTIFIER IN general_expression COLON EOL statement_block

    expr_list : general_expression
              | general_expression COMMA expr_list

    general_expression : boolean_expression

    boolean_expression : boolean_and_expression
                       | boolean_expression OR boolean_and_expression

    boolean_and_expression : boolean_not_expression
                           | boolean_and_expression AND boolean_not_expression

    boolean_not_expression : relational_expression
                           | NOT boolean_not_expression

    relational_expression : expression
                          | relational_expression COMPARISON_OPERATOR expression

    expression : arith_expression
               | expression '+' arith_expression
               | expression '-' arith_expression
               | expression '**' arith_expression

    arith_expression : negatable_expression_atom
                     | arith_expression '*' negatable_expression_atom
                     | arith_expression '/' negatable_expression_atom


    negatable_expression_atom : "-" negatable_expression_atom 
                              | expression_atom

    expression_atom : value_literal
                    | IDENTIFIER '(' ')' # Function call, with no arguments
                    | IDENTIFIER '(' expr_list ')' # Function call
                    | '(' general_expression ')'

    value_literal : number
                  | STRING
                  | CHARACTER
                  | BOOLEAN
                  | IDENTIFIER

    number : NUMBER
           | FLOAT
           | HEX
           | OCTAL
           | BINARY
           | LONG         (suffice is L)
           | UNSIGNEDLONG (suffice is l)
           | '-' number

Current Lexing rules used by the grammar:

    NUMBER : \d+
    FLOAT : \d+.\d+ # different from normal python, which allows .1 and 1.
    HEX : 0x([abcdef]|\d)+
    OCTAL : 0o\d+
    BINARY : 0b\d+
    STRING - "([^\"]|\.)*" or '([^\']|\.)*' # single/double quote strings, with escaped values
    CHARACTER : c'.' /  c"." # Simplification - can be an escaped character
    BOOLEAN : True|False
    IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*


The lexing supports most aspects of python - much more than this, but the grammar
does not as yet use them, so this summary does not list them.

## Limitations

Most expressions currently rely on the C++ counterparts. As a result not all
combinations which are valid are directly supported yet. Notable ones:

* Combinations of strings with other strings (outlawing /*, etc)
* Combinations of strings with numbers 


## Why a python 2 print statement?

Python 2 has print statement with special notation; python 3's version is
a function call. The reason why this grammar currently has a python-2 style
print statement with special notation is to specifically avoid implementing
general function calls yet. Once those are implemented, special cases - like
implementing print - can be implemented, and this python 2 style print
statement WILL be removed. I expect this will occur around version 0.0.15,
based on current rate of progress.

Keeping it for now also simplifies "yield" later

## Compilation process strategy

The compiler consists of the following parts:

* A lexical analyser. This is a simple parse with 3 modes. These modes are essentially:
  * NORMAL - this is used most of the time and is regular parsing
  * BLOCKS - entered at end of line, and used to check whether to start/finish a BLOCK
  * ENDBLOCKS - this is used to close off 1 or more blocks

* A grammar parser - this constructs an abstract syntax tree for the python code. This
  uses Pynodes - which form a tree. This process does as little as possible beyond
  building the tree - however it aims to throw away as little information as possible.

* Pynodes - these are used to capture information in the abstract tree, and to assist
  with analysis. These are standard tree nodes (now), but can perform custom traversals
  for specific tasks.

* Analysis Phase - WIP. This performs the following tasks:
  * Works down through the AST, DEPTH FIRST, adding context to identifier nodes. This
    is to allow type identification/capture.
    * This idea here is that if you pass into an AST node that represents a syntactic
      scoped namespace - such as a function, class/etc, that we can stack the scopes
      with regard to names, values and especially types

  * Open issues:
    * We need logical values of some kind to be avilable for use in contexts, to be
      referenced by identifiers. Logical values are values that can be assigned or
      read at a specific point in time. In traditional terms this are literally
      represented as expressions, but it's a bit more subtle than that - we want to
      represent expression results.

    * Working down through the AST currently trees the AST as a flat tree - in terms
      of namespaces - a single global one. To determine scoping rules we need to be
      able to differentiate where a tree/subtree starts/finishes in a traversal.
       * Probably requires a custom traversal to be honest

  * The analysis phase decorates the AST with additional data

* Code generation phase:
  * Takes a JSON description from the AST and uses that to create a C-Syntax Tree.
    This syntax tree kinda mirrors the sort of tree that you'd expect to get out
    of the semantic analysis phases of a simplistic C compiler.
  * This is then walked to generate simple C++ code

* Compilation
  * The next step is to take the generated code and compile it. For the moment, this
    operates on the code generated, and compiles it as a linux standalone. This will
    switch over to allowing arduino as a target at some point.

Analysis phase now picks up on the use of a variable before it's definition in code.
This is the start of useful error states and therefore useful error messages!

## Type inference strategy

Create the node tree.

**DONE**

* Traverse down the tree adding a context object to all identifiers. **DONE**

**WIP**

* Then when we do types, we search inside the object and set it inside the object. **DONE**

**TBD**

* When you pass through a class or def, you push the current one onto a stack and refer to it as the parent context **TBD**

* We repeat this until all the types of variables are *known* **TBD** (def/class still TBD)

* If any are unknown we stop type inference. **TBD**

It's simple, but should work and has stopping criteria.

And can build on what we have now

Before we do that though, let's fix the code generation for identifiers, since it's gone screwy!

