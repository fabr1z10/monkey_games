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
    except yaml.YAMLError as ye:
        print(f"An error occurred while parsing YAML: {ye}")
        exit(1)

def readYAML(file):
    with open(file, 'r') as f:
        data = yaml.safe_load(f)

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