import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("left", 'ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN'),
    ("left", 'EQ', 'NEQ', 'GT', 'LT', 'LTE', 'GTE'),
    ("left", 'ADD', 'SUB', 'DOT_ADD', 'DOT_SUB'),
    ("left", 'MUL', 'DIV', 'DOT_MUL', 'DOT_DIV'),
    ("right", 'ONES', 'ZEROS', 'EYE'),
    ("left", "'"),
    ("right", ":"),
    ("left", "UMINUS"),

    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
)

def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, "?", p.type, p.value))
    else:
        print("Unexpected end of input")

def p_program(p):
    """
    program : stmt 
            | program stmt
    """

def p_stmt(p):
    """
    stmt : expr ';'
         | print_stmt
         | if_stmt
         | while_stmt
         | for_stmt
         | BREAK ';'
         | CONTINUE ';'
         | RETURN expr ';'
         | ';'
         | '{' '}'
         | '{' stmt_list '}'
    stmt_list : stmt
              | stmt_list stmt
    """

def p_epxr(p):
    """
    expr : ID
         | INTNUM
         | FLOATNUM
         | STR

         | ID ASSIGN expr
         | ID ADD_ASSIGN expr
         | ID SUB_ASSIGN expr
         | ID MUL_ASSIGN expr
         | ID DIV_ASSIGN expr

         | expr '[' list ']' ASSIGN expr
         | expr '[' list ']' ADD_ASSIGN expr
         | expr '[' list ']' SUB_ASSIGN expr
         | expr '[' list ']' MUL_ASSIGN expr
         | expr '[' list ']' DIV_ASSIGN expr

         | expr ADD expr
         | expr SUB expr
         | SUB expr %prec UMINUS
         | expr MUL expr
         | expr DIV expr

         | expr DOT_ADD expr
         | expr DOT_SUB expr
         | expr DOT_MUL expr
         | expr DOT_DIV expr

         | expr GT expr
         | expr LT expr
         | expr GTE expr
         | expr LTE expr
         | expr EQ expr
         | expr NEQ expr

         | EYE '(' expr ')'
         | ONES '(' expr ')'
         | ZEROS '(' expr ')'

         | '[' ']'
         | '[' list ']'

         | expr "'"
    list : expr
         | list ',' expr
    """

def p_if_stmt(p):
    """
    if_stmt : IF '(' expr ')' stmt %prec IFX
            | IF '(' expr ')' stmt ELSE stmt
    """

def p_loop_stmt(p):
    """
    while_stmt : WHILE '(' expr ')' stmt
    range : expr ':' expr
    for_stmt : FOR ID ASSIGN range stmt
    """


def p_print(p):
    """
    print_stmt : PRINT list ';'
    """



parser = yacc.yacc()
