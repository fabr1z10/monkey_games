import re
def evaluate_curly_braces(s, context=None):
	if context is None:
		context = {}

	# Function to evaluate each match
	def replace_match(match):
		expression = match.group(1)  # Extract content inside curly braces
		try:
			# Evaluate the expression using eval in the provided context
			return str(eval(expression, {}, context))
		except Exception as e:
			# Handle errors (optional: log or return original text)
			return f"{{Error: {e}}}"

	# Regular expression to find text inside curly braces
	pattern = r"\{(.*?)\}"
	return re.sub(pattern, replace_match, s)