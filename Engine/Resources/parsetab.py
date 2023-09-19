
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "expressionsleft+-left*/leftLTLEGTGEEENEleftANDORAND BOOLEAN BREAK CONTINUE EE ELSE ELSEIF FUNCTION GE GT IF LE LT MACRO MAX MIN NE NOT NUMBER OR PASS RETURN STRING TAG VARIABLE WORDexpression : PASSexpression : MACRO '=' expression\n                  | MACROatom : VARIABLE '=' expression\n            | VARIABLEelse_branch : ELSE scopeelif_branch : ELSEIF '(' expression ')' scope elif_branch\n                   | ELSEIF '(' expression ')' scope else_branch\n                   | ELSEIF '(' expression ')' scopeif_condition : IF '(' expression ')' scope elif_branch\n                    | IF '(' expression ')' scope else_branch\n                    | IF '(' expression ')' scopefunction_call : FUNCTION parameters scope\n                     | FUNCTION parameters tag_list\n                     | FUNCTION parameters\n                     | FUNCTIONtag : TAG expressiontag_list : tag '#' scope tag_list\n                | tag '#' scopescope : '{' expressions '}'expressions : statement expressions\n                   | statementparameters : '(' param_element ')'\n                  | '(' ')'param_element_pos : WORD '=' expression ',' param_element_pos\n                         | WORD '=' expression ','\n                         | WORD '=' expressionparam_element : expression ',' param_element\n                     | expression ',' param_element_pos\n                     | expression ','\n                     | expressionstatement : BREAKstatement : expression\n                 | if_conditionatom : function_callcomp : NOT comp\n            | arith LT arith\n            | arith LE arith\n            | arith GT arith\n            | arith GE arith\n            | arith EE arith\n            | arith NE arith\n            | comp AND comp\n            | comp OR comp\n            | aritharith : atom '+' atom\n             | atom '-' atom\n             | atom '*' atom\n             | atom '/' atom\n             | atom '%' atom\n             | atom '&' atom\n             | atom '|' atom\n             | atom '^' atom\n             | atomatom : '-' atomcomma_expressions : expression ',' comma_expressions\n                         | expression ','\n                         | expressionarith : MIN '(' comma_expressions ')'\n             | MAX '(' comma_expressions ')'atom : '(' expression ')'statement : RETURN expression\n                 | RETURNtable_contents : STRING ':' expression ',' table_contents\n                      | NUMBER ':' expression ',' table_contents\n                      | STRING ':' expression ','\n                      | NUMBER ':' expression ','\n                      | STRING ':' expression\n                      | NUMBER ':' expressiontable : '%' '[' comma_expressions ']'\n             | '%' '{' table_contents '}'atom : NUMBER\n            | BOOLEAN\n            | STRING\n            | table\n            | WORD\n            | scopeexpression : comp"
    
_lr_action_items = {'BREAK':([0,2,3,4,5,6,7,8,9,12,14,15,20,21,22,23,24,25,26,27,28,30,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,107,111,115,116,121,124,133,134,135,],[3,3,-32,-33,-34,-63,-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,3,-62,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-12,-19,-10,-11,-18,-6,-9,-7,-8,]),'RETURN':([0,2,3,4,5,6,7,8,9,12,14,15,20,21,22,23,24,25,26,27,28,30,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,107,111,115,116,121,124,133,134,135,],[6,6,-32,-33,-34,-63,-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,6,-62,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-12,-19,-10,-11,-18,-6,-9,-7,-8,]),'PASS':([0,2,3,4,5,6,7,8,9,11,12,14,15,20,21,22,23,24,25,26,27,28,30,31,34,36,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,133,134,135,],[7,7,-32,-33,-34,7,-1,-3,-78,7,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,7,-62,7,7,-36,-55,7,7,7,7,-15,7,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,7,-24,-20,-70,7,-71,7,7,-59,-60,-23,7,-12,-19,-10,-11,-18,7,7,-6,-9,-7,-8,]),'MACRO':([0,2,3,4,5,6,7,8,9,11,12,14,15,20,21,22,23,24,25,26,27,28,30,31,34,36,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,133,134,135,],[8,8,-32,-33,-34,8,-1,-3,-78,8,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,8,-62,8,8,-36,-55,8,8,8,8,-15,8,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,8,-24,-20,-70,8,-71,8,8,-59,-60,-23,8,-12,-19,-10,-11,-18,8,8,-6,-9,-7,-8,]),'IF':([0,2,3,4,5,6,7,8,9,12,14,15,20,21,22,23,24,25,26,27,28,30,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,107,111,115,116,121,124,133,134,135,],[10,10,-32,-33,-34,-63,-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,10,-62,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-12,-19,-10,-11,-18,-6,-9,-7,-8,]),'NOT':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,133,134,135,],[13,13,-32,-33,-34,13,-1,-3,-78,13,-77,13,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,13,-62,13,13,13,13,-36,-55,13,13,13,13,-15,13,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,13,-24,-20,-70,13,-71,13,13,-59,-60,-23,13,-12,-19,-10,-11,-18,13,13,-6,-9,-7,-8,]),'MIN':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,133,134,135,],[18,18,-32,-33,-34,18,-1,-3,-78,18,-77,18,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,18,-62,18,18,18,18,-36,18,18,18,18,18,18,-55,18,18,18,18,-15,18,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,18,-24,-20,-70,18,-71,18,18,-59,-60,-23,18,-12,-19,-10,-11,-18,18,18,-6,-9,-7,-8,]),'MAX':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,133,134,135,],[19,19,-32,-33,-34,19,-1,-3,-78,19,-77,19,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,19,-62,19,19,19,19,-36,19,19,19,19,19,19,-55,19,19,19,19,-15,19,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,19,-24,-20,-70,19,-71,19,19,-59,-60,-23,19,-12,-19,-10,-11,-18,19,19,-6,-9,-7,-8,]),'VARIABLE':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,133,134,135,],[20,20,-32,-33,-34,20,-1,-3,-78,20,-77,20,-45,-54,20,-5,-35,-72,-73,-74,-75,-76,-16,20,-62,20,20,20,20,-36,20,20,20,20,20,20,20,20,20,20,20,20,20,20,-55,20,20,20,20,-15,20,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,20,-24,-20,-70,20,-71,20,20,-59,-60,-23,20,-12,-19,-10,-11,-18,20,20,-6,-9,-7,-8,]),'-':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,114,115,116,121,122,123,124,133,134,135,],[16,16,-32,-33,-34,16,-1,-3,-78,16,-77,16,-45,44,16,-5,-35,-72,-73,-74,-75,-76,-16,16,-62,16,16,16,16,-36,16,16,16,16,16,16,16,16,16,16,16,16,16,16,-55,16,16,16,16,-15,16,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,16,-24,-20,-70,16,-71,16,16,-59,-60,-23,16,-12,-19,-76,-10,-11,-18,16,16,-6,-9,-7,-8,]),'(':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,117,121,122,123,124,133,134,135,],[11,11,-32,-33,-34,11,-1,-3,-78,34,11,-77,11,-45,-54,11,54,55,-5,-35,-72,-73,-74,-75,-76,58,11,-62,11,11,11,11,-36,11,11,11,11,11,11,11,11,11,11,11,11,11,11,-55,11,11,11,11,-15,11,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,11,-24,-20,-70,11,-71,11,11,-59,-60,-23,11,-12,-19,-10,-11,123,-18,11,11,-6,-9,-7,-8,]),'NUMBER':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,119,120,121,122,123,124,133,134,135,],[22,22,-32,-33,-34,22,-1,-3,-78,22,-77,22,-45,-54,22,-5,-35,-72,-73,-74,-75,-76,-16,22,-62,22,22,22,22,-36,22,22,22,22,22,22,22,22,22,22,22,22,22,22,-55,22,83,22,22,22,-15,22,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,22,-24,-20,-70,22,-71,22,22,-59,-60,-23,22,-12,-19,-10,-11,83,83,-18,22,22,-6,-9,-7,-8,]),'BOOLEAN':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,133,134,135,],[23,23,-32,-33,-34,23,-1,-3,-78,23,-77,23,-45,-54,23,-5,-35,-72,-73,-74,-75,-76,-16,23,-62,23,23,23,23,-36,23,23,23,23,23,23,23,23,23,23,23,23,23,23,-55,23,23,23,23,-15,23,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,23,-24,-20,-70,23,-71,23,23,-59,-60,-23,23,-12,-19,-10,-11,-18,23,23,-6,-9,-7,-8,]),'STRING':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,119,120,121,122,123,124,133,134,135,],[24,24,-32,-33,-34,24,-1,-3,-78,24,-77,24,-45,-54,24,-5,-35,-72,-73,-74,-75,-76,-16,24,-62,24,24,24,24,-36,24,24,24,24,24,24,24,24,24,24,24,24,24,24,-55,24,82,24,24,24,-15,24,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,24,-24,-20,-70,24,-71,24,24,-59,-60,-23,24,-12,-19,-10,-11,82,82,-18,24,24,-6,-9,-7,-8,]),'WORD':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,129,133,134,135,],[26,26,-32,-33,-34,26,-1,-3,-78,26,-77,26,-45,-54,26,-5,-35,-72,-73,-74,-75,-76,-16,26,-62,26,26,26,26,-36,26,26,26,26,26,26,26,26,26,26,26,26,26,26,-55,26,26,26,26,-15,26,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,26,-24,-20,-70,26,-71,26,26,-59,-60,-23,114,-12,-19,-10,-11,-18,26,26,-6,131,-9,-7,-8,]),'FUNCTION':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,115,116,121,122,123,124,133,134,135,],[27,27,-32,-33,-34,27,-1,-3,-78,27,-77,27,-45,-54,27,-5,-35,-72,-73,-74,-75,-76,-16,27,-62,27,27,27,27,-36,27,27,27,27,27,27,27,27,27,27,27,27,27,27,-55,27,27,27,27,-15,27,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,27,-24,-20,-70,27,-71,27,27,-59,-60,-23,27,-12,-19,-10,-11,-18,27,27,-6,-9,-7,-8,]),'%':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,96,97,98,99,100,101,102,105,106,107,111,114,115,116,121,122,123,124,133,134,135,],[17,17,-32,-33,-34,17,-1,-3,-78,17,-77,17,-45,47,17,-5,-35,-72,-73,-74,-75,-76,-16,17,-62,17,17,17,17,-36,17,17,17,17,17,17,17,17,17,17,17,17,17,17,-55,17,17,17,17,-15,17,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,17,-24,-20,-70,17,-71,17,17,-59,-60,-23,17,-12,-19,-76,-10,-11,-18,17,17,-6,-9,-7,-8,]),'{':([0,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,20,21,22,23,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,58,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,90,92,94,95,96,97,98,99,100,101,102,103,105,106,107,111,115,116,118,121,122,123,124,130,133,134,135,],[28,28,-32,-33,-34,28,-1,-3,-78,28,-77,28,-45,-54,28,53,-5,-35,-72,-73,-74,-75,-76,-16,28,-62,28,28,28,28,-36,28,28,28,28,28,28,28,28,28,28,28,28,28,28,-55,28,28,28,28,28,28,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,28,-24,-20,28,-70,28,-71,28,28,-59,-60,28,-23,28,-12,-19,-10,-11,28,-18,28,28,-6,28,-9,-7,-8,]),'$end':([1,2,3,4,5,6,7,8,9,12,14,15,20,21,22,23,24,25,26,27,29,30,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,107,111,115,116,121,124,133,134,135,],[0,-22,-32,-33,-34,-63,-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,-21,-62,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-12,-19,-10,-11,-18,-6,-9,-7,-8,]),'}':([2,3,4,5,6,7,8,9,12,14,15,20,21,22,23,24,25,26,27,29,30,36,51,57,59,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,81,86,87,88,92,94,96,98,101,102,105,107,109,110,111,115,116,119,120,121,124,125,126,133,134,135,],[-22,-32,-33,-34,-63,-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,-21,-62,-36,-55,-15,94,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,98,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-12,-68,-69,-19,-10,-11,-66,-67,-18,-6,-64,-65,-9,-7,-8,]),')':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,35,36,51,57,58,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,80,84,85,86,87,88,91,92,93,94,96,97,98,101,102,105,106,108,111,112,113,114,121,127,128,129,132,],[-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,64,-36,-55,-15,92,-2,-43,-44,95,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-58,101,102,-4,-13,-14,105,-24,-31,-20,-70,-57,-71,-59,-60,-23,-30,-56,-19,-28,-29,-76,-18,-27,130,-26,-25,]),'AND':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,32,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,32,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'OR':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,33,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,33,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),',':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,80,86,87,88,92,93,94,96,98,101,102,105,109,110,111,114,121,127,],[-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,97,-4,-13,-14,-24,106,-20,-70,-71,-59,-60,-23,119,120,-19,-76,-18,129,]),']':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,86,87,88,92,94,96,97,98,101,102,105,108,111,121,],[-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,96,-58,-4,-13,-14,-24,-20,-70,-57,-71,-59,-60,-23,-56,-19,-18,]),'+':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,-45,43,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'*':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,-45,45,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'/':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,-45,46,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'&':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,-45,48,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'|':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,-45,49,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'^':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,-45,50,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'LT':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,37,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'LE':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,38,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'GT':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,39,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'GE':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,40,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'EE':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,41,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'NE':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,92,94,96,98,101,102,105,111,114,121,],[-1,-3,-78,-77,42,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,-24,-20,-70,-71,-59,-60,-23,-19,-76,-18,]),'#':([7,8,9,12,14,15,20,21,22,23,24,25,26,27,36,51,57,60,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,86,87,88,89,92,94,96,98,101,102,104,105,111,121,],[-1,-3,-78,-77,-45,-54,-5,-35,-72,-73,-74,-75,-76,-16,-36,-55,-15,-2,-43,-44,-61,-37,-38,-39,-40,-41,-42,-46,-47,-48,-49,-50,-51,-52,-53,-4,-13,-14,103,-24,-20,-70,-71,-59,-60,-17,-23,-19,-18,]),'=':([8,20,114,131,],[31,56,122,122,]),'[':([17,],[52,]),'TAG':([57,92,94,105,111,],[90,-24,-20,-23,90,]),':':([82,83,],[99,100,]),'ELSEIF':([94,107,133,],[-20,117,117,]),'ELSE':([94,107,133,],[-20,118,118,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expressions':([0,2,28,],[1,29,59,]),'statement':([0,2,28,],[2,2,2,]),'expression':([0,2,6,11,28,31,34,52,54,55,56,58,90,97,99,100,106,122,123,],[4,4,30,35,4,60,63,80,80,80,86,93,104,80,109,110,93,127,128,]),'if_condition':([0,2,28,],[5,5,5,]),'comp':([0,2,6,11,13,28,31,32,33,34,52,54,55,56,58,90,97,99,100,106,122,123,],[9,9,9,9,36,9,9,61,62,9,9,9,9,9,9,9,9,9,9,9,9,9,]),'scope':([0,2,6,11,13,16,28,31,32,33,34,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,54,55,56,57,58,90,95,97,99,100,103,106,118,122,123,130,],[12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,87,12,12,107,12,12,12,111,12,124,12,12,133,]),'arith':([0,2,6,11,13,28,31,32,33,34,37,38,39,40,41,42,52,54,55,56,58,90,97,99,100,106,122,123,],[14,14,14,14,14,14,14,14,14,14,65,66,67,68,69,70,14,14,14,14,14,14,14,14,14,14,14,14,]),'atom':([0,2,6,11,13,16,28,31,32,33,34,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,54,55,56,58,90,97,99,100,106,122,123,],[15,15,15,15,15,51,15,15,15,15,15,15,15,15,15,15,15,71,72,73,74,75,76,77,78,15,15,15,15,15,15,15,15,15,15,15,15,]),'function_call':([0,2,6,11,13,16,28,31,32,33,34,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,54,55,56,58,90,97,99,100,106,122,123,],[21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'table':([0,2,6,11,13,16,28,31,32,33,34,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,54,55,56,58,90,97,99,100,106,122,123,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'parameters':([27,],[57,]),'comma_expressions':([52,54,55,97,],[79,84,85,108,]),'table_contents':([53,119,120,],[81,125,126,]),'tag_list':([57,111,],[88,121,]),'tag':([57,111,],[89,89,]),'param_element':([58,106,],[91,112,]),'param_element_pos':([106,129,],[113,132,]),'elif_branch':([107,133,],[115,134,]),'else_branch':([107,133,],[116,135,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expressions","S'",1,None,None,None),
  ('expression -> PASS','expression',1,'p_pass','EngineScript.py',168),
  ('expression -> MACRO = expression','expression',3,'p_macro_statement','EngineScript.py',172),
  ('expression -> MACRO','expression',1,'p_macro_statement','EngineScript.py',173),
  ('atom -> VARIABLE = expression','atom',3,'p_statement_assign','EngineScript.py',184),
  ('atom -> VARIABLE','atom',1,'p_statement_assign','EngineScript.py',185),
  ('else_branch -> ELSE scope','else_branch',2,'p_else_branch','EngineScript.py',197),
  ('elif_branch -> ELSEIF ( expression ) scope elif_branch','elif_branch',6,'p_elif_branch','EngineScript.py',203),
  ('elif_branch -> ELSEIF ( expression ) scope else_branch','elif_branch',6,'p_elif_branch','EngineScript.py',204),
  ('elif_branch -> ELSEIF ( expression ) scope','elif_branch',5,'p_elif_branch','EngineScript.py',205),
  ('if_condition -> IF ( expression ) scope elif_branch','if_condition',6,'p_if_statement','EngineScript.py',217),
  ('if_condition -> IF ( expression ) scope else_branch','if_condition',6,'p_if_statement','EngineScript.py',218),
  ('if_condition -> IF ( expression ) scope','if_condition',5,'p_if_statement','EngineScript.py',219),
  ('function_call -> FUNCTION parameters scope','function_call',3,'p_function_call','EngineScript.py',229),
  ('function_call -> FUNCTION parameters tag_list','function_call',3,'p_function_call','EngineScript.py',230),
  ('function_call -> FUNCTION parameters','function_call',2,'p_function_call','EngineScript.py',231),
  ('function_call -> FUNCTION','function_call',1,'p_function_call','EngineScript.py',232),
  ('tag -> TAG expression','tag',2,'p_tag','EngineScript.py',422),
  ('tag_list -> tag # scope tag_list','tag_list',4,'p_tag_list','EngineScript.py',429),
  ('tag_list -> tag # scope','tag_list',3,'p_tag_list','EngineScript.py',430),
  ('scope -> { expressions }','scope',3,'p_scope','EngineScript.py',444),
  ('expressions -> statement expressions','expressions',2,'p_statements','EngineScript.py',448),
  ('expressions -> statement','expressions',1,'p_statements','EngineScript.py',449),
  ('parameters -> ( param_element )','parameters',3,'p_parameters','EngineScript.py',472),
  ('parameters -> ( )','parameters',2,'p_parameters','EngineScript.py',473),
  ('param_element_pos -> WORD = expression , param_element_pos','param_element_pos',5,'p_param_element2','EngineScript.py',480),
  ('param_element_pos -> WORD = expression ,','param_element_pos',4,'p_param_element2','EngineScript.py',481),
  ('param_element_pos -> WORD = expression','param_element_pos',3,'p_param_element2','EngineScript.py',482),
  ('param_element -> expression , param_element','param_element',3,'p_param_element','EngineScript.py',493),
  ('param_element -> expression , param_element_pos','param_element',3,'p_param_element','EngineScript.py',494),
  ('param_element -> expression ,','param_element',2,'p_param_element','EngineScript.py',495),
  ('param_element -> expression','param_element',1,'p_param_element','EngineScript.py',496),
  ('statement -> BREAK','statement',1,'p_statement_break','EngineScript.py',507),
  ('statement -> expression','statement',1,'p_statement_expr','EngineScript.py',511),
  ('statement -> if_condition','statement',1,'p_statement_expr','EngineScript.py',512),
  ('atom -> function_call','atom',1,'p_expression_function_call','EngineScript.py',516),
  ('comp -> NOT comp','comp',2,'p_comp_expression','EngineScript.py',520),
  ('comp -> arith LT arith','comp',3,'p_comp_expression','EngineScript.py',521),
  ('comp -> arith LE arith','comp',3,'p_comp_expression','EngineScript.py',522),
  ('comp -> arith GT arith','comp',3,'p_comp_expression','EngineScript.py',523),
  ('comp -> arith GE arith','comp',3,'p_comp_expression','EngineScript.py',524),
  ('comp -> arith EE arith','comp',3,'p_comp_expression','EngineScript.py',525),
  ('comp -> arith NE arith','comp',3,'p_comp_expression','EngineScript.py',526),
  ('comp -> comp AND comp','comp',3,'p_comp_expression','EngineScript.py',527),
  ('comp -> comp OR comp','comp',3,'p_comp_expression','EngineScript.py',528),
  ('comp -> arith','comp',1,'p_comp_expression','EngineScript.py',529),
  ('arith -> atom + atom','arith',3,'p_expression_binop','EngineScript.py',578),
  ('arith -> atom - atom','arith',3,'p_expression_binop','EngineScript.py',579),
  ('arith -> atom * atom','arith',3,'p_expression_binop','EngineScript.py',580),
  ('arith -> atom / atom','arith',3,'p_expression_binop','EngineScript.py',581),
  ('arith -> atom % atom','arith',3,'p_expression_binop','EngineScript.py',582),
  ('arith -> atom & atom','arith',3,'p_expression_binop','EngineScript.py',583),
  ('arith -> atom | atom','arith',3,'p_expression_binop','EngineScript.py',584),
  ('arith -> atom ^ atom','arith',3,'p_expression_binop','EngineScript.py',585),
  ('arith -> atom','arith',1,'p_expression_binop','EngineScript.py',586),
  ('atom -> - atom','atom',2,'p_expression_uminus','EngineScript.py',625),
  ('comma_expressions -> expression , comma_expressions','comma_expressions',3,'p_comma_sep_expressions','EngineScript.py',636),
  ('comma_expressions -> expression ,','comma_expressions',2,'p_comma_sep_expressions','EngineScript.py',637),
  ('comma_expressions -> expression','comma_expressions',1,'p_comma_sep_expressions','EngineScript.py',638),
  ('arith -> MIN ( comma_expressions )','arith',4,'p_expression_min','EngineScript.py',645),
  ('arith -> MAX ( comma_expressions )','arith',4,'p_expression_min','EngineScript.py',646),
  ('atom -> ( expression )','atom',3,'p_expression_group','EngineScript.py',658),
  ('statement -> RETURN expression','statement',2,'p_expression_return','EngineScript.py',662),
  ('statement -> RETURN','statement',1,'p_expression_return','EngineScript.py',663),
  ('table_contents -> STRING : expression , table_contents','table_contents',5,'p_table_contents','EngineScript.py',670),
  ('table_contents -> NUMBER : expression , table_contents','table_contents',5,'p_table_contents','EngineScript.py',671),
  ('table_contents -> STRING : expression ,','table_contents',4,'p_table_contents','EngineScript.py',672),
  ('table_contents -> NUMBER : expression ,','table_contents',4,'p_table_contents','EngineScript.py',673),
  ('table_contents -> STRING : expression','table_contents',3,'p_table_contents','EngineScript.py',674),
  ('table_contents -> NUMBER : expression','table_contents',3,'p_table_contents','EngineScript.py',675),
  ('table -> % [ comma_expressions ]','table',4,'p_table','EngineScript.py',687),
  ('table -> % { table_contents }','table',4,'p_table','EngineScript.py',688),
  ('atom -> NUMBER','atom',1,'p_expression_other','EngineScript.py',703),
  ('atom -> BOOLEAN','atom',1,'p_expression_other','EngineScript.py',704),
  ('atom -> STRING','atom',1,'p_expression_other','EngineScript.py',705),
  ('atom -> table','atom',1,'p_expression_other','EngineScript.py',706),
  ('atom -> WORD','atom',1,'p_expression_other','EngineScript.py',707),
  ('atom -> scope','atom',1,'p_expression_other','EngineScript.py',708),
  ('expression -> comp','expression',1,'p_expression_comp','EngineScript.py',715),
]
