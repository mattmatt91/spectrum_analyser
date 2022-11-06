# mapping values between 0 and 100 to range
def mapping_to_range(val, min_o, max_o, dtype):
	m = (max_o - min_o)/100
	b = min_o
	mapped_value = m * val + b
	return dtype(mapped_value)


print(bool(round(0.2, 0)), bool(round(0.9, 0)))