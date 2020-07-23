"""

	Filename:	XORAnalysis.py
	Author:		Jessica Turner (highentropystring@gmail.com)
	Date:		19/06/20
	Licence:	GNU GPL V3
	
	A collection of analysis functions and pieces of information required byciphertools programs which implement XOR-based algorithms
	
"""

from itertools import cycle
from typing import Dict
import string

from .Strings import alphanumeric_characters, buildSubStrings

# XOR analysis functions

def letterRatio(input_string: str) -> float:
	return sum(x in alphanumeric_characters for x in input_string) / len(input_string)

def probablyText(input_string: str) -> float:
	return letterRatio(input_string) > 0.7

# Functions for single-byte key XOR

def repeatingByteXOR(input_string: str, byte: int) -> str:
	return "".join(chr(c ^ byte) for c in input_string)

def repeatingByteXORCrack(input_string: str):
	best = None
	best_valid_chars = 0

	for byte in range(256):
		currentString = repeatingByteXOR(input_string.strip(), byte)
		valid_chars = sum(x in alphanumeric_characters for x in currentString)

		if best == None or valid_chars > best_valid_chars:
			best = { 'message': currentString, 'key': byte }
			best_valid_chars = num_chars

	return best

# Functions for multi-byte key XOR

def multiByteXORCrack(input_string: str, keyLength: int):
	key = "".join(chr(repeatingByteXORCrack(string.strip())['key']) for string in buildSubStrings(input_string, keyLength))
	message = multiByteXOR(input_string, key.encode())

	return { 'message': message, 'key': key }

def multiByteXOR(input_string: str, key: str) -> str:
	return "".join(chr(c ^ byte) for c, byte in zip(input_string, cycle(key)))

# Functions for multi-byte XOR key length prediction

def XORStrings(first: str, second: str) -> bytes:
	return bytes(i ^ j for i, j in zip(first, second)) # Convert two byte strings to their xor product

def hammingDistance(first: str, second: str) -> int:
	return bin(int.from_bytes(XORStrings(first, second), "little")).count("1") # Calculate the bit difference between two strings

def predictKeySize(input_string: str) -> int:
	bestKeyLength = 0
	bestDistance = 10000

	for i in range(6, 40): # Set to a lower bound of 6 because otherwise it always guesses a really short key. Will try and fix in later version.
		distance = 0
		blocks = len(input_string) // i - 1

		distance = sum(
			hamming_distance(
				input_string[i*x     : i*(x+2)-1],
				input_string[i*(x+2) : i*(x+4)-1],
			)
			for x in range(blocks)
		)

		distance /= i * blocks

		if distance < bestDistance:
			bestDistance = distance
			bestKey = i

	return bestKey