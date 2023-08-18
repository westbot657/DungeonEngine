
# Dungeon Scripting language

this is a language that compiles into the json format that the engine can understand


[Tokens](#tokens)  
[Syntax Rules](#syntax-rules)  
[The actually helpful section (eventually maybe)](#documentation)  


## Tokens
```r
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
```r
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


## Documentation

meh, I'll get to this at some point...  


