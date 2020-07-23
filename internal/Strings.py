"""

	Filename:	strings.py
	Author:		Jessica Turner (highentropystring@gmail.com)
	Date:		28/09/19
	Licence:	GNU GPL V3
	
	 
	A collection of functions for the modification of strings required by multiple programs in the ciphertools suite

"""

import re
from typing import List

StringList = List[str]

alphanumeric_characters = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "

english = { 'monogram-frequencies': [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074 ],
			'bigram-frequencies': [] }

def stringPrepare(string: str, preserveSpacing: bool) -> str: # Strip all non alphabetic characters from a string and convert to upper case
	return re.compile("[^A-Z\s]" if preserveSpacing else "[^A-Z]").sub("", string.upper())

def buildSubStrings(string: str, separation: int) -> StringList: # Build a list of substrings required to analyse the ciphertext
	return [string[i::separation] for i in range(separation)]
