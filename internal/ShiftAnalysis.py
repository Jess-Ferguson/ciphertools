"""

	Filename:	ShiftAnalysis.py
	Author:		Jessica Turner (highentropystring@gmail.com)
	Date:		19/06/20
	Licence:	GNU GPL V3
	
	A collection of analysis functions and pieces of information required by ciphertools programs which implement alphabetic shift algorithms

"""

import re
import string
from itertools import cycle

from .Strings import stringPrepare, buildSubStrings, english

# Alphabetic shift cipher analysis functions

def frequencyAnalysis(string): # Normalised frequency analysis
	freq = [0] * 26

	for c in string:
		freq[ord(c) - ord('A')] += 1

	scale = sum(freq) / 100

	return [f / scale for f in freq]

def shiftScoreCalculator(frequencyAnalysis, shift, letterFrequencies): # Calculates a score for a given shift value
	return sum(abs(frequencyAnalysis[index] - letterFrequencies[(index + shift) % 26]) for index in range(0, 26))

def shiftEstimate(frequencyAnalysis, letterFrequencies): # Calculates the most likely shift value for a substring by comparing weighted scores of different shift values
	bestShift = min((shiftScoreCalculator(frequencyAnalysis, shift, letterFrequencies), shift) for shift in range(1, 27))
	return chr(ord('Z') - bestShift[1] + 1)

# Caesar cipher specific functions

def caesar(string, shift):
	return "".join(chr(((ord(char) + shift - ord('A')) % 26) + ord('A')) for char in string)

# Vigenere specific functions

def guessKey(strippedText, allKeys, letterFrequencies):
	maxLength = 30 if len(strippedText) > 30 else len(strippedText) # Limit how large the key can be and prevent keys from being longer than the ciphertext
	keyList = [
				"".join(shiftEstimate(frequencyAnalysis(subString), letterFrequencies) # For each of these substrings find the most likely shift value and concatenate them together in a string
					for subString in buildSubStrings(strippedText, lengthGuess)) # Build a substring containing every character that is lengthGuess characters appart
				for lengthGuess in range(1, maxLength) # Try and find the most likely key for each possible key length
	]

	if allKeys == True:
		return keyList

	return min((shiftScoreCalculator(frequencyAnalysis(vigenere(strippedText, key, False)), 0, letterFrequencies), key) for key in keyList)[1]

def vigenere(plaintext, key, encrypt):
	alphabet = string.ascii_uppercase

	shift = 1 if encrypt else -1

	return "".join(
		alphabet[(alphabet.index(x) + alphabet.index(y) * shift) % 26]
		for x, y in zip(stringPrepare(plaintext, False), cycle(key))
	) 