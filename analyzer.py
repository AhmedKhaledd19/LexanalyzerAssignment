# Define the token types
KEYWORDS = {'if', 'else', 'while', 'for', 'return', 'int', 'float', 'char'}
OPERATORS = {'+', '-', '*', '/', '=', '==', '>', '<', '>=', '<=', '+=', '-=', '*=', '/='}
DELIMITERS = {'(', ')', '{', '}', '[', ']', ';', ','}
LITERALS = {'true', 'false', 'null'}

# Define token types
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Lexical Analyzer class
class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.current_char = self.code[self.pos] if self.code else None

    def advance(self):
        """Moves the pointer to the next character in the input."""
        self.pos += 1
        if self.pos < len(self.code):
            self.current_char = self.code[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        """Skips over whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def parse_identifier_or_keyword(self):
        """Parses identifiers or keywords."""
        value = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            value += self.current_char
            self.advance()
        if value in KEYWORDS:
            return Token('KEYWORD', value)
        return Token('IDENTIFIER', value)

    def parse_number(self):
        """Parses integers and floats."""
        value = ''
        while self.current_char is not None and self.current_char.isdigit():
            value += self.current_char
            self.advance()
        if self.current_char == '.':
            value += '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                value += self.current_char
                self.advance()
            return Token('FLOAT', value)
        return Token('INTEGER', value)

    def parse_operator(self):
        """Parses operators."""
        value = self.current_char
        if self.current_char == '=' and self.peek() == '=':
            value += self.peek()
            self.advance()
        elif self.current_char in ['+', '-', '*', '/', '<', '>']:
            if self.peek() in ['+', '=', '-', '=']:
                value += self.peek()
                self.advance()
        self.advance()
        return Token('OPERATOR', value)

    def parse_delimiter(self):
        """Parses delimiters (brackets, commas, etc.)."""
        value = self.current_char
        self.advance()
        return Token('DELIMITER', value)

    def parse_literal(self):
        """Parses boolean or null literals."""
        value = ''
        while self.current_char is not None and self.current_char.isalpha():
            value += self.current_char
            self.advance()
        if value in LITERALS:
            return Token('LITERAL', value)
        return None

    def peek(self):
        """Peeks at the next character."""
        if self.pos + 1 < len(self.code):
            return self.code[self.pos + 1]
        return None

    def get_next_token(self):
        """Returns the next token."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha() or self.current_char == '_':
                return self.parse_identifier_or_keyword()
            if self.current_char.isdigit():
                return self.parse_number()
            if self.current_char in OPERATORS:
                return self.parse_operator()
            if self.current_char in DELIMITERS:
                return self.parse_delimiter()
            if self.current_char.isalpha():
                literal_token = self.parse_literal()
                if literal_token:
                    return literal_token
            raise ValueError(f"Invalid character {self.current_char}")
        return Token('EOF', None)

    def tokenize(self):
        """Tokenizes the entire code."""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == 'EOF':
                break
        return tokens

# Example usage:
if __name__ == "__main__":
    code = input("Enter the code to tokenize: ")
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)

