# built-in
import os
import math
import itertools

# scipy suite
# import numpy as np
# import sympy
# from scipy import integrate

# custom
from to_words import to_words
from error import error
from word_types import *


# everything after a sentence in the same paragraph can access variables from that sentence
# indented paragraphs seperated by a line break are out of scope of eachother
# non-indented blocks are in the global scope
# only normal sentences are allowed, no questions
# a variable at the beginning of the sentence that is capitalized stays capitalized,
#	however if there is no variable with that capital name it will be lowercased
# add ambiguity error for sentences like "Abc plus equals 5 times 1 and 3":
#	it could be interpreted as abc += 5 * 1 + 3 or abc += 5 * 1 * 3

os.system("clear")

essay = """Abc equals [(10. Abc "pl" us)] "equa" |(|ls| + a)| (5 times [(1 + "1" and [2])] and) 3. Print abc."""
"""Abc equals 10. Abc plus equals 5 times 1 and 3. Print abc.""" #25
to_words(essay)

"""
for p in to_words(essay):
	for s in p["paragraph"]:
		sentence = s["sentence"]
		sentence_iter = iter(enumerate(sentence))
		for w, word in sentence_iter:
			if "type" in word:
				print(word["raw"] + ": " + word["type"])
				continue

			def inner():
				for i in range(longest_phrase, 1, -1):
					w_prime = w + i
					if w_prime >= len(sentence): continue

					proceeding_words = sentence[w : w_prime]

					for proceeding_word in proceeding_words:
						if "type" in proceeding_word:
							return False

					proceeding_words_processed = [
						proceeding_word["processed"] for
						proceeding_word in
						proceeding_words
					]
					phrase = " ".join(proceeding_words_processed)

					phrase_word_type = word_type(phrase)
					if phrase_word_type:
						print(phrase + ": " + phrase_word_type)
						next(itertools.islice(sentence_iter, i - 1, i - 1), None)
						return True

			if inner(): continue

			print(word["processed"] + ": " + str(word_type(word["processed"])))

		print("\ts")
	print()
"""
# find all expressions in each sentence next.



