import re

from error import error
from word_types import word_type

def find_strings(essay):
	string_delimiters = ["\"", "'", "`"]

	main_delimiter = string_delimiters[0]
	split_essay = essay.split(main_delimiter)
	strings = []

	for phrase in split_essay:
		index = split_essay.index(phrase)
		strings.append({
			"raw": phrase,
			"delimiter": main_delimiter if index % 2 != 0 else None
		})

	for delimiter in string_delimiters[1:]:
		new_processed_essay = []

		for phrase in strings:
			if phrase["delimiter"]:
				new_processed_essay.append({
					"raw": phrase["raw"],
					"delimiter": phrase["delimiter"]
				})
			else:
				split_phrase = phrase["raw"].split(delimiter)
				for phrase in split_phrase:
					index = split_phrase.index(phrase)
					new_processed_essay.append({
						"raw": phrase,
						"delimiter": delimiter if index % 2 != 0 else None
					})

		strings = new_processed_essay
		if len(strings) % 2 == 0:
			error("punctuation", "strings must be closed")

	strings = [{
		"raw": phrase["raw"],
		"type": "string",
		"subtype": phrase["delimiter"]
	} if phrase["delimiter"] else {
		"raw": phrase["raw"]
	} for phrase in strings]

	return strings

def find_brackets(strings):
	bracket_types = {
		"parenthesis": {"opening": "(", "closing": ")"},
		"brackets": {"opening": "[", "closing": "]"},
		"braces": {"opening": "{", "closing": "}"},
		"pipes": {"opening": "|", "closing": "|"}
		# pipes cannot be nested within eachother unless other brackets are used,
		# for example |(|x - 1| - 1)| != ||x - 1| - 1|, the latter is nonsense
	}

	brackets = [{"content": ""}]
	depth = ""
	pipe_depth = 0

	def nested(lastElement, lenDepth):
		if lenDepth > 0:
			return nested(lastElement[-1]["content"], lenDepth - 1)
		return lastElement

	for phrase in strings:
		if "type" in phrase:
			nested(brackets, len(depth)).append({
				"content": phrase["raw"],
				"type": phrase["type"],
				"subtype": phrase["subtype"]
			})
			nested(brackets, len(depth)).append({"content": ""})
			continue

		for i, letter in enumerate(phrase["raw"]):
			single_continue = False
			for bracket_type, delimiters in bracket_types.items():

				if letter == delimiters["opening"]:
					if bracket_type != "pipes":
						nested(brackets, len(depth)).append({
							"delimiter": bracket_type,
							"content": [{"content": ""}]
						})
						depth += delimiters["opening"]
					else:
						if pipe_depth and depth[-1] == delimiters["opening"]:
							depth = depth[:-1]
							nested(brackets, len(depth)).append({"content": ""})
							pipe_depth -= 1
						else:
							nested(brackets, len(depth)).append({
								"delimiter": bracket_type,
								"content": [{"content": ""}]
							})
							depth += delimiters["opening"]
							pipe_depth += 1

					single_continue = True
					break

				elif letter == delimiters["closing"]:
					if depth[-1] == delimiters["opening"]:
						depth = depth[:-1]
						nested(brackets, len(depth)).append({"content": ""})
					else:
						error("punctuation", bracket_type + " must be matched properly")
					single_continue = True
					break

			if single_continue:
				continue

			nested(brackets, len(depth))[-1]["content"] += letter

	def loop_through_phrase(phrase):
		for subphrase in phrase:
			content = subphrase["content"]
			if type(content) is list:
				loop_through_phrase(content)

		new_phrase = [i for i in phrase if i["content"] != ""]
		del phrase[:]
		phrase.extend(new_phrase)

	loop_through_phrase(brackets)

	# add errors for pipe depth
	for phrase in brackets:
		print(phrase)


	return strings

def find_paragraphs(brackets):
	temp_paragraphs = [{
		"raw": phrase["raw"],
		"type": phrase["type"],
		"subtype": phrase["subtype"]
	} if "type" in phrase else {
		"raw": phrase["raw"].split("\n")
	} for phrase in brackets]

	paragraphs = [{"paragraph": [], "raw": ""}]

	for phrase in temp_paragraphs:
		large_break = False
		after_large_break = False

		if "type" in phrase:
			paragraphs[-1]["paragraph"].append(phrase)
			delimiter = phrase["subtype"]
			paragraphs[-1]["raw"] += delimiter + phrase["raw"] + delimiter
			continue

		blank_phrase = lambda : ({"raw": ""}).copy()

		paragraphs[-1]["paragraph"].append(blank_phrase())

		for i, subphrase in enumerate(phrase["raw"]):
			large_break = subphrase == ""

			if after_large_break and not large_break:
				new_phrase = blank_phrase()
				new_phrase["raw"] = subphrase
				paragraphs.append({"paragraph": [new_phrase], "raw": ""})
				large_break = False
			else:
				raw = paragraphs[-1]["paragraph"][-1]["raw"]
				space = " " if raw else ""
				paragraphs[-1]["paragraph"][-1]["raw"] += space + subphrase if subphrase else ""

			raw = paragraphs[-1]["raw"]
			paragraphs[-1]["raw"] += ("\n" if i and subphrase and raw else "") + subphrase
			after_large_break = large_break

	return paragraphs


def find_sentences(paragraphs):
	sentences = []
	for paragraph in paragraphs:
		sentences.append({"paragraph": [{"sentence": [], "raw": ""}], "raw": paragraph["raw"]})
		for phrase in paragraph["paragraph"]:

			if "type" in phrase:
				sentences[-1]["paragraph"][-1]["sentence"].append(phrase)
				delimiter = phrase["subtype"]
				sentences[-1]["paragraph"][-1]["raw"] += delimiter + phrase["raw"] + delimiter
				continue

			phrase.update(raw = phrase["raw"].split(". "))
			for i, raw in enumerate(phrase["raw"]):
				period = "." if i != len(phrase["raw"]) - 1 else ""
				subphrase = {"raw": raw + period}

				if i:
					sentences[-1]["paragraph"].append({"sentence": [subphrase], "raw": raw + period})
				else:
					sentences[-1]["paragraph"][-1]["sentence"].append(subphrase)
					sentences[-1]["paragraph"][-1]["raw"] += raw + period

	return sentences

def find_words(sentences):
	words = []
	for paragraph in sentences:
		words.append({"paragraph": [], "raw": paragraph["raw"]})
		for sentence in paragraph["paragraph"]:
			words[-1]["paragraph"].append({"sentence": [], "raw": sentence["raw"]})
			for phrase in sentence["sentence"]:

				if "type" in phrase:
					words[-1]["paragraph"][-1]["sentence"].append(phrase)
					continue

				phrase.update(raw = phrase["raw"].split())
				for raw in phrase["raw"]:
					subphrase = {"raw": raw}
					words[-1]["paragraph"][-1]["sentence"].append(subphrase)

	return words

def to_words(essay):
	strings = find_strings(essay)
	brackets = find_brackets(strings)
	# paragraphs = find_paragraphs(brackets)
	# sentences = find_sentences(paragraphs)
	# words = find_words(sentences)

	# for p, paragraph in enumerate(words):
	# 	for s, sentence in enumerate(paragraph["paragraph"]):
	# 		for w, word in enumerate(sentence["sentence"]):
	# 			if "type" in word:
	# 				if w == len(sentence["sentence"]) - 1:
	# 					error("punctuation", "sentence must end in period", p, s, sentence["raw"])
	# 				continue

	# 			if w == 0:
	# 				first_word = word["raw"]
	# 				first_letter = first_word[0]

	# 				new_first_word = first_letter.lower() + first_word[1:]

	# 				if first_letter.isupper():
	# 					if word_type(new_first_word):
	# 						word["processed"] = new_first_word
	# 				else:
	# 					error.warn("punctuation", "first letter of sentence should be capitalized", p, s, sentence["raw"], first_word)
	# 					word["processed"] = first_word

	# 			elif w == len(sentence["sentence"]) - 1:
	# 				last_word = word["raw"]
	# 				last_letter = last_word[-1]

	# 				if last_letter == ".":
	# 					word["processed"] = last_word[:-1]
	# 				else:
	# 					error("punctuation", "sentence must end in period", p, s, sentence["raw"])

	# 			if not "processed" in word:
	# 				word["processed"] = word["raw"]

	# return words
