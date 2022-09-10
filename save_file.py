import pickle
import pandas as pd
import os


# Write
def write_df_to_file(filename: str, df: pd.DataFrame):
	with open(filename, 'wb') as outp:
		pickle.dump(df, outp, pickle.HIGHEST_PROTOCOL)


# Read
def read_df_from_file(filename: str) -> object:
	try:
		with open(filename, 'rb') as inp:
			df = pickle.load(inp)
			return df
	except IOError:
		return False


def delete_file(filename: str):
	os.remove(filename)
