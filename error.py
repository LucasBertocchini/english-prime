import sys

class error:
	red = "\033[31m"
	yellow = "\033[33m"
	end = "\033[0m"


	def __init__(self, error_type, message, p = None, s = None, sentence_raw = None, word_raw = None):
		print(error.red + error_type + " error: " + message + error.end)
		traceback(p, s, sentence_raw, word_raw)
		sys.exit()

	def warn(error_type, message, p = None, s = None, sentence_raw = None, word_raw = None):
		full_error_type = "non-fatal {} error: ".format(error_type)
		print(error.yellow + full_error_type + message + error.end)
		traceback(p, s, sentence_raw, word_raw)
		print()

def traceback(p, s, sentence_raw, word_raw):
	if (p != None and s != None and sentence_raw):

		print("paragraph " + str(p) + "; sentence " + str(s))

		sentence_raw = sentence_raw.replace("\n", "\\n")
		print(sentence_raw)
		if (word_raw): print(" " * sentence_raw.index(word_raw) + "^")
		else: print(" " * len(sentence_raw) + "^")