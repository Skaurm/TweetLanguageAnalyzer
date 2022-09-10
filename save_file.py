import pickle
import pandas as pd


# Write
def write_df_to_file(filename: str, df: pd.DataFrame):
	with open(filename, 'wb') as outp:
		pickle.dump(df, outp, pickle.HIGHEST_PROTOCOL)


# Read
def read_df_from_file(filename: str):
	with open(filename, 'rb') as inp:
		df = pickle.load(inp)
		return df
