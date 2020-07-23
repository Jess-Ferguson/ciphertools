#!/usr/bin/python3

"""

	Filename:	caesar.py
	Author:		Jess Turner
	Date:		19/06/20
	Licence:	GNU GPL V3

	Multipurpose Caesar Cipher tool, an encipher and decipher text using a specified shift value, or can attempt to decrypt an input without a given shift by using statistical analysis

	Options:
		--bruteforce - attempt to bruteforce the shift value
		--encrypt - enable encryption mode
		--decrypt - enable decryption mode
		--preserve-spacing - preserve the spacing of the input in the output
		--shift - specify the shift value
		--spacing - specify the output spacing
		--guess - attempt to guess the shift value by statistical analysis
		
"""

import argparse
import string
import sys
import re

from internal.ShiftAnalysis import shiftEstimate, frequencyAnalysis, caesar
from internal.Strings import stringPrepare, english

def initialiseParser():
	parser = argparse.ArgumentParser(description = "Encrypt or decrypt a string using the Caesar Cipher")

	parser.add_argument("--bruteforce", "--brute", "-b", help = "Try every single possible shift value and allow the user to manually analyse the output", action = "store_true")
	parser.add_argument("--encrypt", "--enc", "-e", help = "Enable encryption mode", action = "store_true")
	parser.add_argument("--decrypt", "--dec", "-d", help = "Enable decryption mode", action = "store_true")
	parser.add_argument("--preserve-spacing", "--preserve", "-p", help = "Preserve the spacing from the input text", action = "store_true", dest = "preserveSpacing")
	parser.add_argument("--shift", "-s", help = "Specify the shift value for the cipher", type = int, choices = range(1, 26))
	parser.add_argument("--spacing", "-x", help = "Specify the spacing in output", type = int)
	parser.add_argument("--guess", "-g", help = "Perform statistical analysis to estimate the most likely shift value", action = "store_true")

	return parser

def main():
	parser = initialiseParser()
	args = parser.parse_args()
	rawText = stringPrepare(input(""), True)
	strippedText = stringPrepare(rawText, False)
	shift = 13;

	if args.bruteforce:
		bruteforce = True
	else:
		bruteforce = False
		if args.shift:
			shift = args.shift
		elif not args.guess:
			print("[+] No shift value given, defaulting to ROT13 mode...")

	if args.decrypt:
		shift = -shift

	if args.guess:
		shiftGuess = ord(shiftEstimate(frequencyAnalysis(strippedText), english["monogram-frequencies"])) - ord('A')
		print("[-] Best shift value guess: {} ({})\n[+] Attempting decryption...".format(shiftGuess, shiftGuess))
		output = caesar(strippedText, -shiftGuess)
	elif bruteforce:
		for shift in range(1, 27):
			print("{}: {}".format(shift, caesar(strippedText, -shift)))
		return
	else:
		output = caesar(strippedText, shift)

	if args.preserveSpacing:
		for x in range(0, len(rawText)):
			if rawText[x].isspace():
				output = output[:x] + rawText[x] + output[x:] # Reinsert the stripped spaces back into the output
	elif args.spacing:
		if args.spacing > 0:
			output = " ".join([output[i:i + args.spacing] for i in range(0, len(output), args.spacing)])

	print(output)

	return

if __name__ == "__main__":
	main()