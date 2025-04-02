from . import assets
import colorama
import monkey2

def exit_with_err(msg: str):
    print(f"{colorama.Fore.RED}{msg}{colorama.Style.RESET_ALL}")
    exit(1)

def m_assert(value, msg):
    if not value:
        exit_with_err(msg)

def add_tag(key: str, node):
    assets.ids[key] = node.id

def get_tag(key: str):
    if key not in assets.ids:
        exit_with_err(f"Don't know id: {key}")
    return monkey2.getNode(assets.ids[key])


