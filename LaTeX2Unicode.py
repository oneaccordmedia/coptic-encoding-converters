import os
import argparse
from unicodedata import normalize

conversion_table = {
    'A': 'Ⲁ',                                       'a': 'ⲁ',
    'B': 'Ⲃ',                                       'b': 'ⲃ',
    'C': 'Ⲥ',                                       'c': 'ⲥ',
    'D': 'Ⲇ',                                       'd': 'ⲇ',
    'E': 'Ⲉ',                                       'e': 'ⲉ',
    'F': 'Ϥ',                                       'f': 'ϥ',
    'G': 'Ⲅ',                                       'g': 'ⲅ',
    'H': 'Ⲏ',                                       'h': 'ⲏ',
    'I': 'Ⲓ',                                       'i': 'ⲓ',
    'J': 'Ϧ', 'HJ': 'Ϧ', 'Hj': 'Ϧ',                 'j': 'ϧ', 'hj': 'ϧ',
    'K': 'Ⲕ',                                       'k': 'ⲕ',
    'L': 'Ⲗ',                                       'l': 'ⲗ',
    'M': 'Ⲙ',                                       'm': 'ⲙ',
    'N': 'Ⲛ',                                       'n': 'ⲛ',
    'O': 'Ⲟ',                                       'o': 'ⲟ',
    'P': 'Ⲡ',                                       'p': 'ⲡ',
    'Q': 'Ϭ',                                       'q': 'ϭ',
    'R': 'Ⲣ',                                       'r': 'ⲣ',
    'T': 'Ⲧ',                                       't': 'ⲧ',
    'U': 'Ⲩ',                                       'u': 'ⲩ',
    'W': 'Ⲱ',                                      'w': 'ⲱ',
    'X': 'Ⲭ',                                       'x': 'ⲭ',
    'Y': 'Ϣ',                                       'y': 'ϣ',
    'Z': 'Ⲍ',                                       'z': 'ⲍ',
    '(': 'Ⲑ', '81': 'Ⲑ',                            '8': 'ⲑ',
    '*': 'Ⲝ', 'KS': 'Ⲝ', 'Ks': 'Ⲝ',                 ')': 'ⲝ', 'ks': 'ⲝ',
    ',': 'Ⲫ', 'P1': 'Ⲫ',                            '+': 'ⲫ', 'p1': 'ⲫ',
    '$': 'Ⲯ', 'PS': 'Ⲯ', 'Ps': 'Ⲯ',                 '#': 'ⲯ', 'ps': 'ⲯ',
    '<': 'Ϫ', 'DJ': 'Ϫ', 'Dj': 'Ϫ', 'D1': 'Ϫ',      ';': 'ϫ', 'dj': 'ϫ', 'd1': 'ϫ',
    '4': 'Ϯ', 'TJ': 'Ϯ', 'Tj': 'Ϯ',                 '3': 'ϯ', 'tj': 'ϯ',
    '0': 'Ϩ', 'H1': 'Ϩ',                            '/': 'ϩ', 'h1': 'ϩ',
    '61': 'Ⲋ',                                      '6': 'ⲋ',
    ']': ')',                                       '[': '(',
    '.': '.',                                       '\\Asterisk': '*',
    '=': '',                                        '-': '-',
    '\\chois': '⳪' + u'\u0305',                    '9': '⳪',
    '\\martyros': '⳥',                              '\\estavros': '⳧',
    '\\longcross': '',                              '\\shortcross': '',
    '\\varlongcross': '',                           '\\varshortcross': '',
    ' ': ' ',                                       ':': ':',
    '\\\\': '\\\\'
}

backslash_symbols = ['\\', 'chois', 'Asterisk', 'martyros', 'estavros', 'longcross', 'shortcross', 'varlongcross', 'varshortcross']

def process_line(input_str):
    """
        Takes line of input file, written in LaTeX/ASCII-encoded Coptic, and converts
        the characters to their 
    """
    i = 0
    result = ""
    insert_djinkim = False
    abbreviation = False
    char_builder = ""
    while True:
        if i >= len(input_str):
            return result
        if input_str[i:i+2] == '\\\'':  # Deal with djinkims first, insert djinkim after next character detection
            insert_djinkim = True
            i += 2
            continue
        elif input_str[i:i+3] == '\\={':  # Abbreviation start, record characters
            abbreviation = True
            i += 3
            continue
        elif input_str[i] == '}':  # Abbreviation end, add combining overlines
            abbreviation = False
            char_builder = u'\u0305'.join(char_builder)
            char_builder += u'\u0305'
            i += 1
        elif input_str[i] == '\\':  # Process symbols prefixed with backslashes
            for symbol in backslash_symbols:
                if input_str[i+1:i+len(symbol)+1] == symbol:
                    char_builder += conversion_table['\\'+symbol]
                    i += len(symbol) + 1
                    break
            else:
                raise Exception(f"LaTeX command? - {input_str[i:]}")
        elif (
            (input_str[i] in ['H', 'h', 'D', 'd', 'T', 't']           and input_str[i+1] == 'j') or
            (input_str[i] in ['H', 'D', 'T']                          and input_str[i+1] == 'J') or
            (input_str[i] in ['8', 'P', 'p', 'D', 'd', 'H', 'h', '6'] and input_str[i+1] == '1') or
            (input_str[i] in ['K', 'P']                               and input_str[i+1] == 'S') or
            (input_str[i] in ['K', 'P', 'k', 'p']                     and input_str[i+1] == 's')
        ):
            char_builder += conversion_table[input_str[i:i+2]]
            i += 2
        elif input_str[i] in conversion_table:
            char_builder += conversion_table[input_str[i]]
            i += 1
        else:
            raise Exception(f"Unidentified character! - {input_str[i:]}")
        if insert_djinkim:
            char_builder += u'\u0300'
            insert_djinkim = False
        if not abbreviation:
            result += char_builder
            char_builder = ""

if __name__ == '__main__':
    # First, process input and output filename arguments
    parser = argparse.ArgumentParser(description='Process LaTeX-formatted Coptic into Unicode-formatted Coptic')
    parser.add_argument('input', metavar='input', type=str, help='input filename')
    parser.add_argument('output', metavar='output', type=str, help='output filename')
    args = parser.parse_args()

    # Open input and output files
    input_file = open(args.input, 'r+')
    output_file = open(args.output, 'w+', encoding="utf-8")

    # Read through the input file line-by-line, process each line
    for line in input_file:
        line = line.rstrip()
        result = process_line(line)
        output_file.write(result + "\n")
