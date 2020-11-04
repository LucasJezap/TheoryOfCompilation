import sys
import Mparser
import scanner


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "error.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    try:
        ast = parser.parse(text, lexer=scanner.lexer)
        ast.printTree()
    except Exception as e:
        print(e)