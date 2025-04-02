import colorama
import yaml
import jinja2
import re
from . import assets
from box import Box
from .util import exit_with_err



env = jinja2.Environment()

def addScripts(s):
    assets.scripts = s

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
    except yaml.YAMLError as ye:
        print(f"An error occurred while parsing YAML: {ye}")
        exit(1)


def readStrings(file):
    a = readYAML(file)
    assets.strings = a['strings']

def readRooms(file):
    a = readYAML(file)
    assets.rooms = a['rooms']
    assets.items = a['items']
    assets.state = Box(a['state'])
    if 'verbs' not in a:
        exit_with_err(' -- Game file requires a verb section!')
    assets.verbs = Box(a['verbs'])



def readYAML(file):
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
        print(data)

    templates = data.get('templates', {})

    def process_data(data):
        if isinstance(data, list):
            return [process_data(item) for item in data]

        elif isinstance(data, dict):
            return {k: process_data(v) if k != "templates" else v for k, v in data.items()}

        elif isinstance(data, str):
            match = re.match(r"(\w+)\((.*)\)", data.strip())
            if match:
                template_name, args_str = match.groups()
                try:
                    # Convert to dictionary format
                    args_dict = eval(f"dict({args_str})")
                    if template_name in templates:
                        return process_string_with_template(templates[template_name], args_dict)
                except Exception as e:
                    print(f"Error parsing arguments for {template_name}: {e}")
            return data

        return data

    return process_data(data)

def eval_string(id):
    """
    Replaces `{expression}` in the template string with the evaluated result.

    Args:
		template (str): The string containing `{...}` expressions.
		env (dict, optional): A dictionary of variables to be used in evaluation.

	Returns:
		str: The transformed string with evaluated expressions.
	"""

    if isinstance(id, int):
        env = {}
        sid = id
    else:
        sid = id[0]
        env = id[1]

    s = assets.strings[sid]
    def eval_match(match):
        expr = match.group(1).strip()  # Extract the content inside `{...}`
        try:
            result = eval(expr, {"__builtins__": {}}, env)  # Secure eval
            return str(result)  # Convert everything to string
        except Exception as e:
            return f"[ERROR: {e}]"  # Handle errors gracefully

    pattern = re.compile(r"\{([^{}]+)\}")  # Match `{...}` without nesting
    return pattern.sub(eval_match, s)
