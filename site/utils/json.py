import pandas


def flatten_json(json, return_type = 'json', sep = "_", cols = [], col_names = None):
	df = pandas.DataFrame(json)
	while any((df.applymap(type) == list).any()) or any((df.applymap(type) == dict).any()):
		df = explode_list(split_dict(df, sep))
	if cols:
		df = df[cols].reset_index(drop=True).loc[df[cols].reset_index(drop=True).astype(str).drop_duplicates().index].reset_index(drop=True)
	if type(col_names) == list:
		df.columns = col_names
	if type(col_names) == dict:
		df = df.rename(columns=col_names)
	if return_type =='df':
		return(df).where((pandas.notnull(df)), None)
	if return_type =='json':
		return(df.where((pandas.notnull(df)), None).to_dict(orient='records'))

def split_dict(df, sep):
	for index, value in (df.applymap(type) == dict).any().iteritems():
		if value:
			df1 = df[index].apply(pandas.Series)
			cols = []
			for col in df1.columns:
				cols.append(str(index) + sep +str(col))
			df1.columns = cols
			df = pandas.concat([df.drop([index], axis=1), df1], axis=1)
	return(df)

def explode_list(df):
	for index, value in (df.applymap(type) == list).any().iteritems():
		if value:
			df[index] = df[index].apply(lambda d: d if isinstance(d, list) else [])
			df = df.reset_index(drop=True).explode(index).reset_index(drop=True)
	return(df)