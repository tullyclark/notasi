def split_strip(string_var, sep):
	list_var = string_var.split(sep)
	result = []
	for l in list_var:
		result.append(l.strip())
	return result