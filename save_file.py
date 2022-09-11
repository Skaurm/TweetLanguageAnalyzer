import pickle
import os


# Write
def write_to_file(filename: str, data: any):
	with open(filename, 'wb') as outp:
		pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)


# Read
def read_from_file(filename: str) -> object:
	try:
		with open(filename, 'rb') as inp:
			data = pickle.load(inp)
			return data
	except IOError:
		return False


def delete_file(filename: str):
	os.remove(filename)
