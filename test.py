def mapping_to_range(val, min_o=0, max_o=1, dtype=float):
    if dtype == bool:
        return bool(round(int(val)/100, 0))
    val = int(val)
    m = (max_o - min_o)/100
    b = min_o
    mapped_value = m * val + b
    return dtype(mapped_value)


print(mapping_to_range(80, 0, 0.5))