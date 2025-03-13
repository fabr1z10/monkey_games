import colorama
import yaml
import jinja2
import re

def exit_with_err(msg: str):
	print(f"{colorama.Fore.RED}{msg}{colorama.Style.RESET_ALL}")
	exit(1)

env = jinja2.Environment()

def process_string_with_template(template_str, context):
	"""
	Applies Jinja2 templating to a string, and returns the result in its raw form
	(could be a dict, list, string, etc.).
	"""
	# Render the template with the context
	template = env.from_string(template_str)
	rendered_str = template.render(context)

	# Try parsing it as YAML to get structured data (dict, list, etc.)
	try:
		return yaml.safe_load(rendered_str)
	except yaml.YAMLError:
		print('CANNNNOOTT ', rendered_str)
		exit(1)
		# If it's not valid Y, just return the raw string
		return rendered_str


def readYAML(file):
	with open(file, 'r') as f:
		data = yaml.safe_load(f)
	templates = data.get('templates', {})

	def process_data(data):
		if isinstance(data, list):      # process each item in the list
			return [process_data(item) for item in data]

		elif isinstance(data, dict):
			processed_dict = {}
			for key, value in data.items():
				if key != "templates": # skip templates section
					processed_dict[key] = process_data(value)
				else:
					processed_dict[key] = value # don't process template section
			return processed_dict

		elif isinstance(data, str):
			match = re.match(r"(\w+)\((.*)\)", data)
			if match:
				template_name, args_str = match.groups()
				args = eval(f"[{args_str}]")
				arg_dict = {f"arg{i}": arg for i, arg in enumerate(args)}
				if template_name in templates:
					#template = env.from_string(templates[template_name])
					#rendered = template.render(**arg_dict)
					return process_string_with_template(templates[template_name], arg_dict)
			return data
		return data # return original data if it's not a string, list or dict

	processed_data = process_data(data)
	return processed_data