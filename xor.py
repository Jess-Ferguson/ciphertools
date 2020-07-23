#!/usr/bin/python3

"""

	Filename:	xor.py
	Author:		Jess Turner
	Date:		15/07/20
	Licence:	GNU GPL V3
	
	Multipurpose XOR Encryption tool, can encrypt and decrypt text using a specified single-byte or multi-byte key or attempt to decrypt an input without a given key by using statistical analysis

	Options:
		--encrypt			Enable encryption mode (Default)
		--decrypt			Enable decryption mode
		--key				Specify the encryption key
		--guess				Attempt to guess the encryption key by statistical analysis
		--single-byte		Enable single-byte XOR mode (Default)
		--multi-byte		Enable multi-byte XOR mode

"""

import argparse
import string
import codecs
import sys
from itertools import cycle

from internal.XORAnalysis import predictKeySize, multiByteXORCrack, multiByteXOR, repeatingByteXOR, repeatingByteXORCrack

def initialise_parser():
	parser = argparse.ArgumentParser(description = "Encrypt, decrypt, or crack a message using the XOR Cipher")

	parser.add_argument("--key", "-k", help = "The encryption key to be used (if relevant)", type = str)
	parser.add_argument("--guess", "-g", help = "Perform statistical analysis to estimate the most likely value of the encryption key", action = "store_true")
	parser.add_argument("--single-byte", "--single", "-s", help = "Enable single-byte key mode", action = "store_true")
	parser.add_argument("--multi-byte", "--multi", "-m", help = "Enable multi-byte key mode", action = "store_true")
	parser.add_argument("--decrypt", "-d", help = "Enable decryption mode", action = "store_true")

	return parser

def main():
	parser = initialise_parser()
	args = parser.parse_args()
	input_string = sys.stdin.read().encode()

	if args.decrypt or args.guess:
		input_string = codecs.decode(input_string, "base-64")

	if args.guess:
		if args.multi_byte:
			print("[+] Selecting multi-byte key mode...", file = sys.stderr)
			print("[+] Predicting key length...", file = sys.stderr) # At this point we have the entire decoded input in memory, all that is left is to crack it

			keyLength = predictKeySize(input_string)

			print(
					f"[-] Got length of {keyLength}...\n"
					"[+] Attempting to crack key...",
					file = sys.stderr
				)

			crack = multiByteXORCrack(input_string, keyLength)
			key = crack['key']
		else:
			print("[+] Selecting single-byte key mode...", file = sys.stderr)
			print("[+] Attempting to crack key...", file = sys.stderr)

			crack = repeatingByteXORCrack(input_string)
			key = chr(crack['key'])

		print("[-] Got key: \"{}\" !\n[+] Decrypting message...".format(key), file = sys.stderr)

		output = crack['message']
	elif args.key != None:
		if len(args.key) > 1 and not args.multi_byte:
			print("[+] Single-byte mode selected but multi-byte key was given. Defaulting to multi-byte mode...", file = sys.stderr)
			args.multi_byte = True

		output = multiByteXOR(input_string, [ord(c) for c in args.key]) if args.multi_byte else repeatingByteXOR(input_string, ord(args.key))
			
	else:
		print("[-] Error: No key given!", file = sys.stderr)
		return

	if not args.decrypt and not args.guess:
		output = codecs.encode(output.encode(), "base-64").decode()

	print(output, end = "")

if __name__ == "__main__":
	main()