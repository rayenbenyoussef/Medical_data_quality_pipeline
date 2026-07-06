import numpy as np
from pandas import isna
def _convert_row(row_values: tuple) -> tuple:
    converted = []
    for v in row_values:
        if isna(v) if not isinstance(v, (str, bool)) else False:
            converted.append(None)
        elif isinstance(v, np.integer):
            converted.append(int(v))
        elif isinstance(v, np.floating):
            converted.append(float(v))
        elif isinstance(v, np.bool_):
            converted.append(bool(v))
        else:
            converted.append(v)
    return tuple(converted)