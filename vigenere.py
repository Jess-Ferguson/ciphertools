#!/usr/bin/python3

"""

	Filename:	vigenere.py
	Author:		Jess Turner
	Date:		19/06/20
	Licence:	GNU GPL V3
	
	Multipurpose Vigenere Cipher tool, can encipher and decipher text using a specified key or attempt to decrypt an input without a given key by using statistical analysis

	Options:
		--encrypt			Enable encryption mode (Default)
		--decrypt			Enable decryption mode
		--preserve-spacing	Preserve the spacing of the input in the output
		--key				Specify the encryption key
		--spacing			Specify the output spacing
		--guess				Attempt to guess the encryption key by statistical analysis

"""

import argparse
import string
import sys

from itertools import cycle
from internal.ShiftAnalysis import vigenere, guessKey
from internal.Strings import buildSubStrings, stringPrepare, english

def initialiseParser():
	parser = argparse.ArgumentParser(description = "Encrypt or decrypt a string using the Caesar Cipher")

	parser.add_argument("--encrypt", "--enc", "-e", help = "Enable encryption mode", action = "store_true")
	parser.add_argument("--decrypt", "--dec", "-d", help = "Enable decryption mode", action = "store_true")
	parser.add_argument("--preserve-spacing", "--preserve", "-p", help = "Preserve the spacing from the input text", action = "store_true", dest = "preserveSpacing")
	parser.add_argument("--key", "-k", help = "The encryption key to be used (if relevant)", type = str)
	parser.add_argument("--spacing", "-s", help = "Specify the spacing in the output", type = int)
	parser.add_argument("--guess", "-g", help = "Perform statistical analysis to estimate the most likely value of the encryption key", action = "store_true")
	parser.add_argument("--all", "-a", help = "List all possible keys generated", action = "store_true")

	return parser

def main():
	parser = initialiseParser()
	args = parser.parse_args()
	rawText = stringPrepare(input(""), True)
	strippedText = stringPrepare(rawText, False)

	language = english

	if args.guess:
		print("[+] Attempting to crack key...", file = sys.stderr)
		if args.all:
			for key in list(guessKey(strippedText, True, language['monogram-frequencies'])):
				print(key)

		bestKeyGuess = guessKey(strippedText, False, language['monogram-frequencies'])
		print("[-] Guessed key: {}\n[+] Attempting decryption...".format(bestKeyGuess), file = sys.stderr)
		output = vigenere(strippedText, bestKeyGuess, False)
	elif args.key != None:
		if not args.decrypt and args.encrypt:
			args.encrypt = True

		output = vigenere(strippedText, stringPrepare(args.key, False), args.encrypt)
	else:
		print("[-] Error: No key given!", file = sys.stderr)
		return

	if args.preserveSpacing:
		for x in range(0, len(rawText)):
			if rawText[x].isspace():
				output = output[:x] + rawText[x] + output[x:] # Reinsert the stripped spaces back into the output
	elif args.spacing:
		if args.spacing > 0:
			output = " ".join([output[i:i + args.spacing] for i in range(0, len(output), args.spacing)])

	print(output)

if __name__ == "__main__":
	main()