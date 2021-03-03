# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
# Convert CS-encoded Coptic text to LaTeX-encoded text
# (for the cbbohairic package)
# -----------------------------------------------------------------------
# CS2LaTeX.py [written for Python 2.x]
# 
# MIT License
#
# Copyright (c) 2021 George Kamel, georgekamel [AT] gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# The Current Maintainer of this Python script is George Kamel.
# Created: 14/11/2008 [Version 1.0]
# Last modified: 03/03/2021 [Version 1.1]
# -----------------------------------------------------------------------

import re
import sys
import os
import argparse


def main():
    print 'CS2LaTeX [Version 1.1]\nCopyright (c) 2021 George Kamel\n'

    print 'This script converts Coptic text encoded in the Coptic Standard (CS),\n' \
          'to the encoding of the \'cbbohairic\' LaTeX package.\n'

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="the path to the file containing the CS-encoded text to be converted")
    parser.add_argument("output_file", help="the path to the file to which to output the converted text")
    args = parser.parse_args()
    input_path = args.input_file
    output_path = args.output_file

    # If user-specified file exists, open it and import the text
    if os.path.isfile(input_path):
        input_file = open(input_path, 'r')
        input_text = input_file.read()
        input_file.close()
        print "Imported input file '" + input_path + "'\n"
    else:
        print "ERROR: Input file '" + input_path + "' not found."
        sys.exit(-1)

    if output_path == "":
        print "ERROR: Output file not specified"
        sys.exit(-1)

    # non-latin CS characters: psi, theta, chi, cheema, ti, soou
    lookup_table = {  # punctuation
        "`": "\\\'", "=": "\\=", "@": ":", "*": "\\Asterisk", "(": "[", ")": "]",

        # lowercase letters
        "h": "h1", "j": "dj", "q": "hj", "s": "y", "v": "p1", "x": "ks",
        "y": "h", "'": "ps", ";": "8", ",": "x", "[": "q", "]": "tj", "^": "\\=6",

        # uppercase letters
        "H": "h1", "J": "dj", "Q": "hj", "S": "y", "V": "p1", "X": "ks",
        "Y": "h", '"': "ps", ":": "8", "<": "x", "{": "q", "}": "tj",

        # other symbols
        "�": "{\\chois}", "�": "{\\martyros}", "�": "=",
        "\\": "ou", "�": "{\\estavros}", "�": "{\\estavros}"
    }

    output_text = ''
    for i in range(len(input_text)):
        char_in = input_text[i]
        char_out = lookup_table.get(char_in, char_in)
        output_text = output_text + char_out

    # Replace all ligatures that succeed an overline (\=)
    # with it's single character equivalent
    output_text = re.sub("\\\=h1", "\=/", output_text)  # hori
    output_text = re.sub("\\\=dj", "\=;", output_text)  # djandja
    output_text = re.sub("\\\=p1", "\=+", output_text)  # phi
    output_text = re.sub("\\\=ks", "\=)", output_text)  # exi
    output_text = re.sub("\\\=ps", "\=#", output_text)  # epsi
    output_text = re.sub("\\\=H1", "\=/", output_text)  # Hori
    output_text = re.sub("\\\=DJ", "\=;", output_text)  # Djandja
    output_text = re.sub("\\\=P1", "\=+", output_text)  # Phi
    output_text = re.sub("\\\=KS", "\=)", output_text)  # Exi
    output_text = re.sub("\\\=PS", "\=#", output_text)  # Epsi
    output_text = re.sub("\\\=81", "\=8", output_text)  # Theta

    # Remove redundant overlines (i.e. \=\= --> \=)
    output_text = re.sub('\\\\\\\=\\\\\\\=', '\\\=', output_text)

    # Remove whitespace following an overline (i.e. '\=  ' -> '\=')
    output_text = re.sub('\\\\\\\= ', '\\\=', output_text)

    # Remove redundant djinkims (i.e. \'\' --> \')
    output_text = re.sub('\\\\\\\'\\\\\\\'', '\\\'', output_text)

    # Remove whitespaces following an djinkim (i.e. '\'  ' -> '\'')
    output_text = re.sub('\\\\\\\' ', '\\\'', output_text)

    # Search for split overlines and replace with continuous ones
    # e.g. I\=l\=h\=m -> I\={lhm}
    # ---
    # Five consecutive overlined letters
    search_overline = re.compile('\\\=\S\\\=\S\\\=\S\\\=\S\\\=\S')
    x = search_overline.search(output_text)

    while x is not None:
        y = x.start()
        output_text = output_text[0:y] + '\\={' + output_text[y + 2] + output_text[y + 5] + output_text[y + 8] + \
                      output_text[y + 11] + output_text[y + 14] + '}' + output_text[y + 15:len(output_text)]
        x = search_overline.search(output_text)

    # Four consecutive overlined letters
    search_overline = re.compile('\\\=\S\\\=\S\\\=\S\\\=\S')
    x = search_overline.search(output_text)

    while x is not None:
        y = x.start()
        output_text = output_text[0:y] + '\\={' + output_text[y + 2] + output_text[y + 5] + output_text[y + 8] + \
                     output_text[y + 11] + '}' + output_text[y + 12:len(output_text)]
        x = search_overline.search(output_text)

    # Three consecutive overlined letters
    search_overline = re.compile('\\\=\S\\\=\S\\\=\S')
    x = search_overline.search(output_text)
    while x is not None:
        y = x.start()
        output_text = output_text[0:y] + '\\={' + output_text[y + 2] + output_text[y + 5] + output_text[
            y + 8] + '}' + output_text[y + 9:len(output_text)]
        x = search_overline.search(output_text)

    # Two consecutive overlined letters
    search_overline = re.compile('\\\=\S\\\=\S')
    x = search_overline.search(output_text)
    while x is not None:
        y = x.start()
        output_text = output_text[0:y] + '\\={' + output_text[y + 2] + output_text[y + 5] + '}' + output_text[
                                                                                              y + 6:len(output_text)]
        x = search_overline.search(output_text)

    # Replace all ligatures that succeed a djinkim (\')
    # with it's single character equivalent
    output_text = re.sub("\\\'h1", "\'/", output_text)  # hori
    output_text = re.sub("\\\'dj", "\';", output_text)  # djandja
    output_text = re.sub("\\\'p1", "\'+", output_text)  # phi
    output_text = re.sub("\\\'ks", "\')", output_text)  # exi
    output_text = re.sub("\\\'ps", "\'#", output_text)  # epsi
    output_text = re.sub("\\\'H1", "\'/", output_text)  # Hori
    output_text = re.sub("\\\'DJ", "\';", output_text)  # Djandja
    output_text = re.sub("\\\'P1", "\'+", output_text)  # Phi
    output_text = re.sub("\\\'KS", "\')", output_text)  # Exi
    output_text = re.sub("\\\'PS", "\'#", output_text)  # Epsi
    output_text = re.sub("\\\'81", "\'8", output_text)  # Theta

    # Other corrections
    output_text = re.sub("\\\={oc}", "{\\chois}", output_text)  # \={oc} -> {\chois}
    output_text = re.sub("\\\={qc}", "{\\chois}", output_text)  # \={qc} -> {\chois}

    # Convert all text to lowercase
    output_text = output_text.lower()

    # Output LaTeX-encoded text ()
    output_file = open(output_path, 'w')
    output_file.write(output_text)
    output_file.close()
    print "Saved LaTeX-encoded text to '" + output_path + "'"


if __name__ == "__main__":
    main()
