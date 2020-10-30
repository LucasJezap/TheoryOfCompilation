import sys
import scanner

def tokens(input):
    lexer = scanner.lexer  
    lexer.input(text)
    while token := lexer.token():
        yield token


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'example.txt'
    try:
        with open(filename) as file:
            text = file.read()
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    for tok in tokens(text):
        print("(%d): %s(%s)" %(tok.lineno, tok.type, tok.value))