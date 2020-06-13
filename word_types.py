longest_phrase = 2

types = (
	"number",
		"integer",
		"float",
		"complex",
	"string",
	"boolean",
	"list",
	"dictionary",
	"function"
)

functions = {
	"exponential": {

	},
	"sum": {

	},
	"print": {

	}
}

# to updates the variable on the right.
# to:
# add a to b
# add a and b to c
# add a, b, and c, to d

# with:
# add a with b
# add a with b and c
# add a with b, c, and d
# add a and b with c
# add a, b, and c, with d

# and:
# add a and b
# add a, b, and c
# add a, b, c, and d

# any pseudolist length

operators = {
	"plus": {
		"num_variables": 2,
		"usage": [
			{
				"raw": "$v0 plus $v1",
				"result": lambda v0, v1 : v0 + v1
			}
		]
	},
	"times": {
		"num_variables": 2,
		"usage": [
			{
				"raw": "$v0 times $v1",
				"result": lambda v0, v1 : v0 * v1
			}
		]
	},
}

assignment_operators = {
	"equals": {

	},
	# "add": {
	# 	# "num_variables": math.inf,
	# 	# "usage": [
	# 	# 	{
	# 	# 		"raw": "add $v0 to $v1",
	# 	# 		"func": lambda a, b: a + b
	# 	# 	},
	# 	# ]
	# },
	# "multiply": lambda a, b: a * b,
	"exponentiate": {

	},
	"plus equals": {
	},
}

def word_type(word):
	if word in functions.keys():
		return "function"
	if word in operators.keys():
		return "operator"
	if word in assignment_operators.keys():
		return "assignment operator"

	word_without_sign_isnumeric = lambda word : \
		len(word) > 1 and word[0] in ["+", "-"] and word[1:].isnumeric()
	word_or_word_without_sign_isnumeric = \
		lambda word : word.isnumeric() or word_without_sign_isnumeric(word)

	if word_or_word_without_sign_isnumeric(word):
		return "integer"
	if word_or_word_without_sign_isnumeric(word.replace(".", "", 1)):
		return "float"
