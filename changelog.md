
# Alpha-6 Update

## Changes
- Updated Scripting Language



### Scripting Language
---

The scripting language has been updated to:
- give error messages instead of failing to compile or partially compiling
- give you a summary of your code when compiled
- allow better and cleaner syntax

#### Compilation Summary
- Gives you a list of variables and where (or why) they are defined
- Lists whenever a variable is assigned or referenced, useful for ensuring you are using the variables you actually intended to use

#### Syntax and feature updates

- macros and macro functions
  - can be used to write repetitive code faster
  - function macros are basically just functions that can't have code updated live (normal functions can be modified by code)
- shorthand functions
  - common functions can be written easier. ie: `output()` vs `[engine:player/message]()`
- string joining
  - written as `expr_1`..`expr_2`..`expr_n`::`seperator`
  - `..` indicates to join strings
  - `::` indicates the seperator (defaults to space)
- list/dict accessing
  - written as `<var>['key']` or `<var>[0]` (index starts at 0)
- error messages
  - compiling code with syntax errors will now tell you what/where an error is (error position may be wrong if it is expecting a closing parenthesis/bracket/brace)




