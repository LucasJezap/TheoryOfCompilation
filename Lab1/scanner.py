import ply.lex as lex

literals = "()[]{},;:'"

keywords = {
    keyword: keyword.upper()
    for keyword in [
        'if', 'else', 'for', 'while', 'break', 'continue',
        'return', 'eye', 'zeros', 'ones', 'print'
    ]
}

operators = {
    f"{lexem_prefix}{lexem}{lexem_postfix}": f"{token_prefix}{token}{token_postfix}"
    for lexem, token in (
        ('+', 'ADD'), ('-', 'SUB'),
        ('*', 'MUL'), ('/', 'DIV')
    )
    for lexem_prefix, token_prefix, lexem_postfix, token_postfix in (
        (''         , ''          , ''           , ''            ),
        ('.'        , 'DOT_'      , ''           , ''            ),
        (''         , ''          , '='          , '_ASSIGN'     )
    )
}

tokens = (
    'ID',  # identyfikatory

    'INTNUM',  # liczby całkowite
    'FLOATNUM',  # liczby zmiennoprzecinkowe
    'STR',  # string

    'ASSIGN',
    'GT', 'LT', 'GTE', 'LTE', 'NEQ', 'EQ',  # operatory relacyjne

    'BRACKETS',  # nawiasy

    'RANGE',  # : operator zakresu
    'TRANSPOSE',  # ' transpozycja
    'COLON', 'SEMICOLON',  # przecinek i średnik

    *keywords.values(),
    *operators.values()
)


def t_BINOP(t):
    r"[-+*/]=|\.?[-+*/]"
    t.type = operators[t.value]
    return t


t_ASSIGN = r"="
t_NEQ = r"!="
t_EQ = r"=="

t_GT = r"<"
t_LT = r">"
t_GTE = r"<="
t_LTE = r">="


def t_ID(t):
    r"[a-zA-Z_]\w*"
    t.type = keywords[t.value] if t.value in keywords else 'ID'
    return t


def t_FLOATNUM(t):
    r"(?:\d+\.\d*|\.\d+)(?:[eE]-?\d+)?|\d+[eE]-?\d+"
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_STR(t):
    r'".*?"'
    t.value = t.value[1:-1]
    return t


t_ignore = ' \t'
t_ignore_COMMENT = r'[#].*'


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()