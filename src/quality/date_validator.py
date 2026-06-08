def _validate_str(value, name):
    if not isinstance(value, str) or not value.strip():
        raise TypeError(f"{name} must be a non-empty string")

def _validate_integer(value, name):
    if not isinstance(value, int):
        raise TypeError(f"{name} must be a non-empty integer")