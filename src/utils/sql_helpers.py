import re

def sanitize_identifier(name: str) -> str:
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
        raise ValueError(f"Unsafe or invalid identifier: {name}")
    return name