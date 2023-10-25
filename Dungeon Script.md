
# Dungeon Scripting language

this is a language that compiles into the json format that the engine can understand


[Tokens](#tokens)  
[Syntax Rules](#syntax-rules)  
[The actually helpful section (eventually maybe)](#documentation)  


## Tokens
```rust
comments             : "//..."
functions            : "[namespace:category/function]"
variables            : "<local_variable>"
                     | "<#environment_variable>"
                     | "<%constant_value>"
                     | "<variable.with.attributes>"
macros               | "$macro_name"
comparison operators : "a == b"
                     | "a != b"
                     | "a >> b"
                     | "a << b"
                     | "a <= b"
                     | "a >= b"
                     | "not a"
                     | "a or b"
                     | "a and b"
math operators       : "a + b"
                     | "a - b"
                     | "a * b"
                     | "a / b"
                     | "min(a, b[, ...])"
                     | "max(a, b[, ...])"
keywords             : "return [a]"
                     | "break"
                     | "if"
                     | "elif"
                     | "else"
boolean              : "true"
                     | "false"
numbers              : "n"
                     | "n.n"
                     | ".n"
```

## Syntax rules
```rust
atom : VARIABLE '=' expression
     | VARIABLE
     | '-' atom
     | '(' expression ')'
     | NUMBER
     | BOOLEAN
     | STRING
     | table
     | WORD
     | scope
     | function_call

expression : comp
           | MACRO '=' expression
           | MACRO
           | PASS

table : '%' '[' comma_expressions ']'
      | '%' '{' table_contents '}'

scope : '{' expressions '}'

function_call : FUNCTION parameters scope
              | FUNCTION parameters tag_list
              | FUNCTION parameters
              | FUNCTION

comp : NOT comp
     | arith LT arith
     | arith LE arith
     | arith GT arith
     | arith GE arith
     | arith EE arith
     | arith NE arith
     | comp AND comp
     | comp OR comp
     | arith

comma_expressions : expression ',' comma_expressions
                  | expression ','
                  | expression

table_contents : STRING ':' expression ',' table_contents
               | NUMBER ':' expression ',' table_contents
               | STRING ':' expression ','
               | NUMBER ':' expression ','
               | STRING ':' expression
               | NUMBER ':' expression

expressions : statement expressions
            | statement

parameters : '(' param_element ')'
           | '(' ')'

tag_list : tag '#' scope tag_list
         | tag '#' scope

arith : atom '+' atom
      | atom '-' atom
      | atom '*' atom
      | atom '/' atom
      | atom

statement : BREAK
          | expression
          | if_condition
          | RETURN expression
          | RETURN


param_element : expression ',' param_element
              | expression ',' param_element_pos
              | expression ','
              | expression

tag : TAG expression

param_element_pos : WORD '=' expression ',' param_element_pos
                  | WORD '=' expression ','
                  | WORD '=' expression

if_condition : IF '(' expression ')' scope elif_branch
             | IF '(' expression ')' scope else_branch
             | IF '(' expression ')' scope

elif_branch : ELSEIF '(' expression ')' scope elif_branch
            | ELSEIF '(' expression ')' scope else_branch
            | ELSEIF '(' expression ')' scope

else_branch : ELSE scope

```

## New Syntax Rules
```rust
statements : statement statements
           | statement
           | <none>

statement : BREAK
          | RETURN expression
          | RETURN
          | PASS
          | if_statement
          | while_loop
          | for_loop
          | expression

expression : comp
           | macro

if_statement : IF '(' expression ')' scope elif_branch
             | IF '(' expression ')' scope else_branch
             | IF '(' expression ')' scope

while_loop : WHILE '(' expression ')' scope

for_loop : FOR variable ',' variable IN expression scope
         | FOR variable IN expression scope

scope : '{' statements '}'

elif_branch : ELSEIF '(' expression ')' scope elif_branch
            | ELSEIF '(' expression ')' scope else_branch
            | ELSEIF '(' expression ')' scope

else_branch : ELSE scope

comp : NOT comp
     | arith LT arith
     | arith LE arith
     | arith GT arith
     | arith GE arith
     | arith EE arith
     | arith NE arith
     | comp AND comp
     | comp OR comp
     | arith

macro : MACRO '(' macro_args ')' '=' macro_scope
      | MACRO '(' comma_expressions ')'
      | MACRO '=' expression
      | MACRO

arith : atom '+' atom
      | atom '-' atom
      | atom '*' atom
      | atom '/' atom
      | atom

macro_args : MACRO ',' macro_args
           | MACRO

macro_scope : '{' macro_statements '}'

comma_expressions : expression ',' comma_expressions
                  | expression ','
                  | expression

atom : VARIABLE '=' expression
     | VARIABLE
     | '-' atom
     | '(' expression ')'
     | NUMBER
     | BOOLEAN
     | STRING
     | table
     | WORD
     | scope
     | function_call

table : '%' '[' comma_expressions ']'
      | '%' '{' table_contents '}'

function_call : FUNCTION parameters scope
              | FUNCTION parameters tag_list
              | FUNCTION parameters
              | FUNCTION

table_contents : expression ':' expression ',' table_contents
               | expression ':' expression ','
               | expression ':' expression

parameters : '(' param_element ')'
           | '(' ')'

tag_list : tag '#' scope tag_list
         | tag '#' scope

param_element : expression ',' param_element_pos
              | expression ',' param_element
              | expression ','
              | expression

tag : TAG expression

param_element_pos : WORD '=' expression ',' param_element_pos
                  | WORD '=' expression ','
                  | WORD '=' expression

```




## Documentation

meh, I'll get to this at some point...  


functions:
```json

[engine:player/message]("...") // this compiles to a function call, passing "..." as a parameter
// Compiles to:
// {
//     "function": "engine:player/message",
//     "message": "..."
// }


[engine:combat/next_turn] // this compiles to a function call with no parameters passed
// Compiles to:
// {
//     "function": "engine:combat/next_turn"
// }


[engine:text/match](<#text>) // some functions support a branching syntax for better readability.
@pattern: "(1|one)" # { // depending on the function, multiple branches may be called
    pass
}
@pattern: "(2|two)" # {
    pass
}
// Compiles to:
// {
//     "function": "engine:text/match",
//     "text": {"#ref": "#text"},
//     "matches": [
//         {
//             "pattern": "(1|one)",
//             "run": {} // 'pass' compiles to nothing
//         },
//         {
//             "pattern": (2|two),
//             "run": {}
//         }
//     ]
// }



```



