
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "expressionsleft+-left*/leftLTLEGTGEEENEleftANDORAND BOOLEAN BREAK CONTINUE EE ELSE ELSEIF FUNCTION GE GT IF LE LT MACRO MAX MIN NE NOT NUMBER OR PASS POW RETURN STRING TAG VARIABLE WHILE WORDexpression : PASSexpression : MACRO '=' expression\n                  | MACROatom : VARIABLE '=' expression\n            | VARIABLEelse_branch : ELSE scopeelif_branch : ELSEIF '(' expression ')' scope elif_branch\n                   | ELSEIF '(' expression ')' scope else_branch\n                   | ELSEIF '(' expression ')' scopeif_condition : IF '(' expression ')' scope elif_branch\n                    | IF '(' expression ')' scope else_branch\n                    | IF '(' expression ')' scopewhile_loop : WHILE '(' expression ')' scopefunction_call : FUNCTION parameters scope\n                     | FUNCTION parameters tag_list\n                     | FUNCTION parameters\n                     | FUNCTIONtag : TAG expressiontag_list : tag '#' scope tag_list\n                | tag '#' scopescope : '{' expressions '}'\n             | '{' '}'expressions : statement expressions\n                   | statement\n                   | parameters : '(' param_element ')'\n                  | '(' ')'param_element_pos : WORD '=' expression ',' param_element_pos\n                         | WORD '=' expression ','\n                         | WORD '=' expressionparam_element : expression ',' param_element\n                     | expression ',' param_element_pos\n                     | expression ','\n                     | expressionstatement : BREAKstatement : expression\n                 | if_condition\n                 | while_loopatom : function_callcomp : NOT comp\n            | arith LT arith\n            | arith LE arith\n            | arith GT arith\n            | arith GE arith\n            | arith EE arith\n            | arith NE arith\n            | comp AND comp\n            | comp OR comp\n            | aritharith : atom '+' atom\n             | atom '-' atom\n             | atom '*' atom\n             | atom '/' atom\n             | atom '%' atom\n             | atom '&' atom\n             | atom '|' atom\n             | atom '^' atom\n             | atom POW atom\n             | atomatom : '-' atomcomma_expressions : expression ',' comma_expressions\n                         | expression ','\n                         | expressionarith : MIN '(' comma_expressions ')'\n             | MAX '(' comma_expressions ')'atom : '(' expression ')'statement : RETURN expression\n                 | RETURNtable_contents : STRING ':' expression ',' table_contents\n                      | NUMBER ':' expression ',' table_contents\n                      | STRING ':' expression ','\n                      | NUMBER ':' expression ','\n                      | STRING ':' expression\n                      | NUMBER ':' expressiontable : '%' '[' comma_expressions ']'\n             | '%' '{' table_contents '}'atom : NUMBER\n            | BOOLEAN\n            | STRING\n            | table\n            | WORD\n            | scopeexpression : comp"
    
_lr_action_items = {'$end':([0,1,2,3,4,5,6,7,8,9,10,13,16,17,22,23,24,25,26,27,28,29,31,32,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,115,116,120,124,125,130,133,142,143,144,],[-25,0,-24,-35,-36,-37,-38,-68,-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,-23,-67,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-12,-13,-20,-10,-11,-19,-6,-9,-7,-8,]),'BREAK':([0,2,3,4,5,6,7,8,9,10,13,16,17,22,23,24,25,26,27,28,29,30,32,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,115,116,120,124,125,130,133,142,143,144,],[3,3,-35,-36,-37,-38,-68,-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,3,-67,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-12,-13,-20,-10,-11,-19,-6,-9,-7,-8,]),'RETURN':([0,2,3,4,5,6,7,8,9,10,13,16,17,22,23,24,25,26,27,28,29,30,32,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,115,116,120,124,125,130,133,142,143,144,],[7,7,-35,-36,-37,-38,-68,-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,7,-67,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-12,-13,-20,-10,-11,-19,-6,-9,-7,-8,]),'PASS':([0,2,3,4,5,6,7,8,9,10,12,13,16,17,22,23,24,25,26,27,28,29,30,32,33,36,38,39,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,142,143,144,],[8,8,-35,-36,-37,-38,8,-1,-3,-83,8,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,8,-67,8,8,8,-40,-60,8,8,8,8,-16,8,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,8,-27,-21,-75,8,-76,8,8,-64,-65,-26,8,-12,-13,-20,-10,-11,-19,8,8,-6,-9,-7,-8,]),'MACRO':([0,2,3,4,5,6,7,8,9,10,12,13,16,17,22,23,24,25,26,27,28,29,30,32,33,36,38,39,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,142,143,144,],[9,9,-35,-36,-37,-38,9,-1,-3,-83,9,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,9,-67,9,9,9,-40,-60,9,9,9,9,-16,9,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,9,-27,-21,-75,9,-76,9,9,-64,-65,-26,9,-12,-13,-20,-10,-11,-19,9,9,-6,-9,-7,-8,]),'IF':([0,2,3,4,5,6,7,8,9,10,13,16,17,22,23,24,25,26,27,28,29,30,32,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,115,116,120,124,125,130,133,142,143,144,],[11,11,-35,-36,-37,-38,-68,-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,11,-67,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-12,-13,-20,-10,-11,-19,-6,-9,-7,-8,]),'WHILE':([0,2,3,4,5,6,7,8,9,10,13,16,17,22,23,24,25,26,27,28,29,30,32,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,115,116,120,124,125,130,133,142,143,144,],[14,14,-35,-36,-37,-38,-68,-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,14,-67,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-12,-13,-20,-10,-11,-19,-6,-9,-7,-8,]),'NOT':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,142,143,144,],[15,15,-35,-36,-37,-38,15,-1,-3,-83,15,-82,15,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,15,-67,15,15,15,15,15,-40,-60,15,15,15,15,-16,15,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,15,-27,-21,-75,15,-76,15,15,-64,-65,-26,15,-12,-13,-20,-10,-11,-19,15,15,-6,-9,-7,-8,]),'MIN':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,142,143,144,],[20,20,-35,-36,-37,-38,20,-1,-3,-83,20,-82,20,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,20,-67,20,20,20,20,20,-40,20,20,20,20,20,20,-60,20,20,20,20,-16,20,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,20,-27,-21,-75,20,-76,20,20,-64,-65,-26,20,-12,-13,-20,-10,-11,-19,20,20,-6,-9,-7,-8,]),'MAX':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,142,143,144,],[21,21,-35,-36,-37,-38,21,-1,-3,-83,21,-82,21,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,21,-67,21,21,21,21,21,-40,21,21,21,21,21,21,-60,21,21,21,21,-16,21,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,21,-27,-21,-75,21,-76,21,21,-64,-65,-26,21,-12,-13,-20,-10,-11,-19,21,21,-6,-9,-7,-8,]),'VARIABLE':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,142,143,144,],[22,22,-35,-36,-37,-38,22,-1,-3,-83,22,-82,22,-49,-59,22,-5,-39,-77,-78,-79,-80,-81,-17,22,-67,22,22,22,22,22,-40,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,-60,22,22,22,22,-16,22,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,22,-27,-21,-75,22,-76,22,22,-64,-65,-26,22,-12,-13,-20,-10,-11,-19,22,22,-6,-9,-7,-8,]),'-':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,123,124,125,130,131,132,133,142,143,144,],[18,18,-35,-36,-37,-38,18,-1,-3,-83,18,-82,18,-49,47,18,-5,-39,-77,-78,-79,-80,-81,-17,18,-67,18,18,18,18,18,-40,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,-60,18,18,18,18,-16,18,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,18,-27,-21,-75,18,-76,18,18,-64,-65,-26,18,-12,-13,-20,-81,-10,-11,-19,18,18,-6,-9,-7,-8,]),'(':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,126,130,131,132,133,142,143,144,],[12,12,-35,-36,-37,-38,12,-1,-3,-83,36,12,-82,38,12,-49,-59,12,58,59,-5,-39,-77,-78,-79,-80,-81,62,12,-67,12,12,12,12,12,-40,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,-60,12,12,12,12,-16,12,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,12,-27,-21,-75,12,-76,12,12,-64,-65,-26,12,-12,-13,-20,-10,-11,132,-19,12,12,-6,-9,-7,-8,]),'NUMBER':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,128,129,130,131,132,133,142,143,144,],[24,24,-35,-36,-37,-38,24,-1,-3,-83,24,-82,24,-49,-59,24,-5,-39,-77,-78,-79,-80,-81,-17,24,-67,24,24,24,24,24,-40,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,-60,24,90,24,24,24,-16,24,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,24,-27,-21,-75,24,-76,24,24,-64,-65,-26,24,-12,-13,-20,-10,-11,90,90,-19,24,24,-6,-9,-7,-8,]),'BOOLEAN':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,142,143,144,],[25,25,-35,-36,-37,-38,25,-1,-3,-83,25,-82,25,-49,-59,25,-5,-39,-77,-78,-79,-80,-81,-17,25,-67,25,25,25,25,25,-40,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,-60,25,25,25,25,-16,25,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,25,-27,-21,-75,25,-76,25,25,-64,-65,-26,25,-12,-13,-20,-10,-11,-19,25,25,-6,-9,-7,-8,]),'STRING':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,128,129,130,131,132,133,142,143,144,],[26,26,-35,-36,-37,-38,26,-1,-3,-83,26,-82,26,-49,-59,26,-5,-39,-77,-78,-79,-80,-81,-17,26,-67,26,26,26,26,26,-40,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,-60,26,89,26,26,26,-16,26,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,26,-27,-21,-75,26,-76,26,26,-64,-65,-26,26,-12,-13,-20,-10,-11,89,89,-19,26,26,-6,-9,-7,-8,]),'WORD':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,138,142,143,144,],[28,28,-35,-36,-37,-38,28,-1,-3,-83,28,-82,28,-49,-59,28,-5,-39,-77,-78,-79,-80,-81,-17,28,-67,28,28,28,28,28,-40,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,-60,28,28,28,28,-16,28,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,28,-27,-21,-75,28,-76,28,28,-64,-65,-26,123,-12,-13,-20,-10,-11,-19,28,28,-6,140,-9,-7,-8,]),'FUNCTION':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,124,125,130,131,132,133,142,143,144,],[29,29,-35,-36,-37,-38,29,-1,-3,-83,29,-82,29,-49,-59,29,-5,-39,-77,-78,-79,-80,-81,-17,29,-67,29,29,29,29,29,-40,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,-60,29,29,29,29,-16,29,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,29,-27,-21,-75,29,-76,29,29,-64,-65,-26,29,-12,-13,-20,-10,-11,-19,29,29,-6,-9,-7,-8,]),'%':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,104,105,106,107,108,109,110,113,114,115,116,120,123,124,125,130,131,132,133,142,143,144,],[19,19,-35,-36,-37,-38,19,-1,-3,-83,19,-82,19,-49,50,19,-5,-39,-77,-78,-79,-80,-81,-17,19,-67,19,19,19,19,19,-40,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,-60,19,19,19,19,-16,19,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,19,-27,-21,-75,19,-76,19,19,-64,-65,-26,19,-12,-13,-20,-81,-10,-11,-19,19,19,-6,-9,-7,-8,]),'{':([0,2,3,4,5,6,7,8,9,10,12,13,15,16,17,18,19,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,97,99,101,102,103,104,105,106,107,108,109,110,111,113,114,115,116,120,124,125,127,130,131,132,133,139,142,143,144,],[30,30,-35,-36,-37,-38,30,-1,-3,-83,30,-82,30,-49,-59,30,57,-5,-39,-77,-78,-79,-80,-81,-17,30,-67,30,30,30,30,30,-40,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,-60,30,30,30,30,30,30,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,30,-27,-21,30,30,-75,30,-76,30,30,-64,-65,30,-26,30,-12,-13,-20,-10,-11,30,-19,30,30,-6,30,-9,-7,-8,]),'}':([2,3,4,5,6,7,8,9,10,13,16,17,22,23,24,25,26,27,28,29,30,31,32,39,55,61,63,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,88,93,94,95,99,101,104,106,109,110,113,115,116,118,119,120,124,125,128,129,130,133,134,135,142,143,144,],[-24,-35,-36,-37,-38,-68,-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,64,-23,-67,-40,-60,-16,101,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,106,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-12,-13,-73,-74,-20,-10,-11,-71,-72,-19,-6,-69,-70,-9,-7,-8,]),')':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,37,39,55,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,87,91,92,93,94,95,98,99,100,101,104,105,106,109,110,113,114,117,120,121,122,123,130,136,137,138,141,],[-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,69,-40,-60,-16,99,-22,-2,-47,-48,102,-66,103,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-63,109,110,-4,-14,-15,113,-27,-34,-21,-75,-62,-76,-64,-65,-26,-33,-61,-20,-31,-32,-81,-19,-30,139,-29,-28,]),'AND':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,34,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,34,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'OR':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,35,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,35,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),',':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,87,93,94,95,99,100,101,104,106,109,110,113,118,119,120,123,130,136,],[-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,105,-4,-14,-15,-27,114,-21,-75,-76,-64,-65,-26,128,129,-20,-81,-19,138,]),']':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,93,94,95,99,101,104,105,106,109,110,113,117,120,130,],[-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,104,-63,-4,-14,-15,-27,-21,-75,-62,-76,-64,-65,-26,-61,-20,-19,]),'+':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,-49,46,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'*':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,-49,48,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'/':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,-49,49,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'&':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,-49,51,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'|':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,-49,52,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'^':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,-49,53,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'POW':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,-49,54,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'LT':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,40,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'LE':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,41,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'GT':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,42,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'GE':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,43,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'EE':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,44,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'NE':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,99,101,104,106,109,110,113,120,123,130,],[-1,-3,-83,-82,45,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,-27,-21,-75,-76,-64,-65,-26,-20,-81,-19,]),'#':([8,9,10,13,16,17,22,23,24,25,26,27,28,29,39,55,61,64,65,66,67,69,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,93,94,95,96,99,101,104,106,109,110,112,113,120,130,],[-1,-3,-83,-82,-49,-59,-5,-39,-77,-78,-79,-80,-81,-17,-40,-60,-16,-22,-2,-47,-48,-66,-41,-42,-43,-44,-45,-46,-50,-51,-52,-53,-54,-55,-56,-57,-58,-4,-14,-15,111,-27,-21,-75,-76,-64,-65,-18,-26,-20,-19,]),'=':([9,22,123,140,],[33,60,131,131,]),'[':([19,],[56,]),'TAG':([61,64,99,101,113,120,],[97,-22,-27,-21,-26,97,]),'ELSEIF':([64,101,115,142,],[-22,-21,126,126,]),'ELSE':([64,101,115,142,],[-22,-21,127,127,]),':':([89,90,],[107,108,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expressions':([0,2,30,],[1,31,63,]),'statement':([0,2,30,],[2,2,2,]),'expression':([0,2,7,12,30,33,36,38,56,58,59,60,62,97,105,107,108,114,131,132,],[4,4,32,37,4,65,68,70,87,87,87,93,100,112,87,118,119,100,136,137,]),'if_condition':([0,2,30,],[5,5,5,]),'while_loop':([0,2,30,],[6,6,6,]),'comp':([0,2,7,12,15,30,33,34,35,36,38,56,58,59,60,62,97,105,107,108,114,131,132,],[10,10,10,10,39,10,10,66,67,10,10,10,10,10,10,10,10,10,10,10,10,10,10,]),'scope':([0,2,7,12,15,18,30,33,34,35,36,38,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,58,59,60,61,62,97,102,103,105,107,108,111,114,127,131,132,139,],[13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,94,13,13,115,116,13,13,13,120,13,133,13,13,142,]),'arith':([0,2,7,12,15,30,33,34,35,36,38,40,41,42,43,44,45,56,58,59,60,62,97,105,107,108,114,131,132,],[16,16,16,16,16,16,16,16,16,16,16,71,72,73,74,75,76,16,16,16,16,16,16,16,16,16,16,16,16,]),'atom':([0,2,7,12,15,18,30,33,34,35,36,38,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,58,59,60,62,97,105,107,108,114,131,132,],[17,17,17,17,17,55,17,17,17,17,17,17,17,17,17,17,17,17,77,78,79,80,81,82,83,84,85,17,17,17,17,17,17,17,17,17,17,17,17,]),'function_call':([0,2,7,12,15,18,30,33,34,35,36,38,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,58,59,60,62,97,105,107,108,114,131,132,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'table':([0,2,7,12,15,18,30,33,34,35,36,38,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,58,59,60,62,97,105,107,108,114,131,132,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'parameters':([29,],[61,]),'comma_expressions':([56,58,59,105,],[86,91,92,117,]),'table_contents':([57,128,129,],[88,134,135,]),'tag_list':([61,120,],[95,130,]),'tag':([61,120,],[96,96,]),'param_element':([62,114,],[98,121,]),'param_element_pos':([114,138,],[122,141,]),'elif_branch':([115,142,],[124,143,]),'else_branch':([115,142,],[125,144,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expressions","S'",1,None,None,None),
  ('expression -> PASS','expression',1,'p_pass','EngineScript.py',174),
  ('expression -> MACRO = expression','expression',3,'p_macro_statement','EngineScript.py',178),
  ('expression -> MACRO','expression',1,'p_macro_statement','EngineScript.py',179),
  ('atom -> VARIABLE = expression','atom',3,'p_statement_assign','EngineScript.py',190),
  ('atom -> VARIABLE','atom',1,'p_statement_assign','EngineScript.py',191),
  ('else_branch -> ELSE scope','else_branch',2,'p_else_branch','EngineScript.py',205),
  ('elif_branch -> ELSEIF ( expression ) scope elif_branch','elif_branch',6,'p_elif_branch','EngineScript.py',211),
  ('elif_branch -> ELSEIF ( expression ) scope else_branch','elif_branch',6,'p_elif_branch','EngineScript.py',212),
  ('elif_branch -> ELSEIF ( expression ) scope','elif_branch',5,'p_elif_branch','EngineScript.py',213),
  ('if_condition -> IF ( expression ) scope elif_branch','if_condition',6,'p_if_statement','EngineScript.py',225),
  ('if_condition -> IF ( expression ) scope else_branch','if_condition',6,'p_if_statement','EngineScript.py',226),
  ('if_condition -> IF ( expression ) scope','if_condition',5,'p_if_statement','EngineScript.py',227),
  ('while_loop -> WHILE ( expression ) scope','while_loop',5,'p_while_loop','EngineScript.py',237),
  ('function_call -> FUNCTION parameters scope','function_call',3,'p_function_call','EngineScript.py',246),
  ('function_call -> FUNCTION parameters tag_list','function_call',3,'p_function_call','EngineScript.py',247),
  ('function_call -> FUNCTION parameters','function_call',2,'p_function_call','EngineScript.py',248),
  ('function_call -> FUNCTION','function_call',1,'p_function_call','EngineScript.py',249),
  ('tag -> TAG expression','tag',2,'p_tag','EngineScript.py',439),
  ('tag_list -> tag # scope tag_list','tag_list',4,'p_tag_list','EngineScript.py',446),
  ('tag_list -> tag # scope','tag_list',3,'p_tag_list','EngineScript.py',447),
  ('scope -> { expressions }','scope',3,'p_scope','EngineScript.py',461),
  ('scope -> { }','scope',2,'p_scope','EngineScript.py',462),
  ('expressions -> statement expressions','expressions',2,'p_statements','EngineScript.py',469),
  ('expressions -> statement','expressions',1,'p_statements','EngineScript.py',470),
  ('expressions -> <empty>','expressions',0,'p_statements','EngineScript.py',471),
  ('parameters -> ( param_element )','parameters',3,'p_parameters','EngineScript.py',496),
  ('parameters -> ( )','parameters',2,'p_parameters','EngineScript.py',497),
  ('param_element_pos -> WORD = expression , param_element_pos','param_element_pos',5,'p_param_element2','EngineScript.py',504),
  ('param_element_pos -> WORD = expression ,','param_element_pos',4,'p_param_element2','EngineScript.py',505),
  ('param_element_pos -> WORD = expression','param_element_pos',3,'p_param_element2','EngineScript.py',506),
  ('param_element -> expression , param_element','param_element',3,'p_param_element','EngineScript.py',517),
  ('param_element -> expression , param_element_pos','param_element',3,'p_param_element','EngineScript.py',518),
  ('param_element -> expression ,','param_element',2,'p_param_element','EngineScript.py',519),
  ('param_element -> expression','param_element',1,'p_param_element','EngineScript.py',520),
  ('statement -> BREAK','statement',1,'p_statement_break','EngineScript.py',531),
  ('statement -> expression','statement',1,'p_statement_expr','EngineScript.py',535),
  ('statement -> if_condition','statement',1,'p_statement_expr','EngineScript.py',536),
  ('statement -> while_loop','statement',1,'p_statement_expr','EngineScript.py',537),
  ('atom -> function_call','atom',1,'p_expression_function_call','EngineScript.py',541),
  ('comp -> NOT comp','comp',2,'p_comp_expression','EngineScript.py',545),
  ('comp -> arith LT arith','comp',3,'p_comp_expression','EngineScript.py',546),
  ('comp -> arith LE arith','comp',3,'p_comp_expression','EngineScript.py',547),
  ('comp -> arith GT arith','comp',3,'p_comp_expression','EngineScript.py',548),
  ('comp -> arith GE arith','comp',3,'p_comp_expression','EngineScript.py',549),
  ('comp -> arith EE arith','comp',3,'p_comp_expression','EngineScript.py',550),
  ('comp -> arith NE arith','comp',3,'p_comp_expression','EngineScript.py',551),
  ('comp -> comp AND comp','comp',3,'p_comp_expression','EngineScript.py',552),
  ('comp -> comp OR comp','comp',3,'p_comp_expression','EngineScript.py',553),
  ('comp -> arith','comp',1,'p_comp_expression','EngineScript.py',554),
  ('arith -> atom + atom','arith',3,'p_expression_binop','EngineScript.py',603),
  ('arith -> atom - atom','arith',3,'p_expression_binop','EngineScript.py',604),
  ('arith -> atom * atom','arith',3,'p_expression_binop','EngineScript.py',605),
  ('arith -> atom / atom','arith',3,'p_expression_binop','EngineScript.py',606),
  ('arith -> atom % atom','arith',3,'p_expression_binop','EngineScript.py',607),
  ('arith -> atom & atom','arith',3,'p_expression_binop','EngineScript.py',608),
  ('arith -> atom | atom','arith',3,'p_expression_binop','EngineScript.py',609),
  ('arith -> atom ^ atom','arith',3,'p_expression_binop','EngineScript.py',610),
  ('arith -> atom POW atom','arith',3,'p_expression_binop','EngineScript.py',611),
  ('arith -> atom','arith',1,'p_expression_binop','EngineScript.py',612),
  ('atom -> - atom','atom',2,'p_expression_uminus','EngineScript.py',653),
  ('comma_expressions -> expression , comma_expressions','comma_expressions',3,'p_comma_sep_expressions','EngineScript.py',664),
  ('comma_expressions -> expression ,','comma_expressions',2,'p_comma_sep_expressions','EngineScript.py',665),
  ('comma_expressions -> expression','comma_expressions',1,'p_comma_sep_expressions','EngineScript.py',666),
  ('arith -> MIN ( comma_expressions )','arith',4,'p_expression_min','EngineScript.py',673),
  ('arith -> MAX ( comma_expressions )','arith',4,'p_expression_min','EngineScript.py',674),
  ('atom -> ( expression )','atom',3,'p_expression_group','EngineScript.py',686),
  ('statement -> RETURN expression','statement',2,'p_expression_return','EngineScript.py',690),
  ('statement -> RETURN','statement',1,'p_expression_return','EngineScript.py',691),
  ('table_contents -> STRING : expression , table_contents','table_contents',5,'p_table_contents','EngineScript.py',698),
  ('table_contents -> NUMBER : expression , table_contents','table_contents',5,'p_table_contents','EngineScript.py',699),
  ('table_contents -> STRING : expression ,','table_contents',4,'p_table_contents','EngineScript.py',700),
  ('table_contents -> NUMBER : expression ,','table_contents',4,'p_table_contents','EngineScript.py',701),
  ('table_contents -> STRING : expression','table_contents',3,'p_table_contents','EngineScript.py',702),
  ('table_contents -> NUMBER : expression','table_contents',3,'p_table_contents','EngineScript.py',703),
  ('table -> % [ comma_expressions ]','table',4,'p_table','EngineScript.py',715),
  ('table -> % { table_contents }','table',4,'p_table','EngineScript.py',716),
  ('atom -> NUMBER','atom',1,'p_expression_other','EngineScript.py',731),
  ('atom -> BOOLEAN','atom',1,'p_expression_other','EngineScript.py',732),
  ('atom -> STRING','atom',1,'p_expression_other','EngineScript.py',733),
  ('atom -> table','atom',1,'p_expression_other','EngineScript.py',734),
  ('atom -> WORD','atom',1,'p_expression_other','EngineScript.py',735),
  ('atom -> scope','atom',1,'p_expression_other','EngineScript.py',736),
  ('expression -> comp','expression',1,'p_expression_comp','EngineScript.py',743),
]
