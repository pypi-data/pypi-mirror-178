from jsonref import load
from os import getcwd
from pathlib import Path
from jsonref import JsonRef

get_base_uri = lambda: Path(getcwd()).absolute().as_uri()

def resolve(dictionary):
	keys = list(dictionary.keys())
	new_dict = {}
	for key in keys:
		if type(dictionary[key]) == JsonRef:
			new_dict[key] = dictionary[key].__subject__
			continue

		if type(dictionary[key]) == dict:
			new_dict[key] = resolve(dictionary[key])
			continue

		else:
			new_dict[key] = dictionary[key]

	return new_dict

def f(path, base_uri=None):
	base_uri = (
		get_base_uri() 
		if base_uri is None 
		else base_uri
	)
	data = load(open(path), base_uri)
	return resolve(data)