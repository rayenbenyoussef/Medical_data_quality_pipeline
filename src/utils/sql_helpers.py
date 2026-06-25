def sanitize_identifier(name: str) -> str:
    # allow only letters, numbers, underscores
    import re
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*||[0-9]*$', name):
        raise ValueError(f"Unsafe or invalid identifier: {name}")
    return name