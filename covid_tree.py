import datetime
import Levenshtein
import pandas as pd

now = datetime.datetime.now()
filename = './results/log_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'

def get_country_code(s):
  country_code = "UNKNOWN" 
  list = s.split("/")
  if "human" in list:
    country_code = list[list.index("human") + 1]
  if "Wuhan" in s:
    country_code = "CHN"
  if "USA" in s:
    country_code = "USA"
  return country_code 


def get_region_name(s):
  region_name = "UNKNOWN" 
  list = s.split("/")
  if "human" in list:
    if len(list) > list.index("human") + 3:
      region_name = list[list.index("human") + 2][:10]
  if "Wuhan" in s:
    region_name = "Wuhan"
  return region_name 



sequence_df = pd.DataFrame(columns=['version', 'country_code', 'region_name', 'sequence'])


path = 'sequences.fasta'

s = ""

with open(path) as f:
    s = f.read()
#    print(type(s))
#    print(s.split('>')[1])
#    print(s.split('>')[2])
    print(len(s.split('>')))

f.close()

covid_nucleic_acid_sequence_array = s.split('>')

covid_nucleic_acid_sequence_array_length = len(covid_nucleic_acid_sequence_array)

for num in range(1,len(covid_nucleic_acid_sequence_array)):
  covid_nucleic_acid_sequence_data = covid_nucleic_acid_sequence_array[num]
  covid_nucleic_acid_sequence_definition = covid_nucleic_acid_sequence_data.splitlines()[0]
  version = covid_nucleic_acid_sequence_definition.split(" ")[0]
  country_code = get_country_code(covid_nucleic_acid_sequence_definition)
  region_name = get_region_name(covid_nucleic_acid_sequence_definition)
  
  str_array = covid_nucleic_acid_sequence_data.splitlines()[1:]

  covid_nucleic_acid_sequence = ""
  for x in str_array:
      covid_nucleic_acid_sequence += x
  
  sequence_s = pd.Series([version, country_code, region_name, covid_nucleic_acid_sequence], index=sequence_df.columns) 
  sequence_df = sequence_df.append(sequence_s, ignore_index=True) 

#pd.options.display.max_colwidth = 1000
pd.set_option('display.max_rows', 3000)
print(sequence_df)

print(sequence_df["country_code"].drop_duplicates())
s = sequence_df["country_code"].drop_duplicates()
sampled_sequence_df = sequence_df[:1]
for v in s:
  print(v)
  country_sequence_df = sequence_df[sequence_df['country_code'].isin([v])]
  sampled_sequence_df = pd.concat([sampled_sequence_df, country_sequence_df.sample(n=min([20, len(country_sequence_df)]))])
# sampled_sequence_df = pd.concat([sampled_sequence_df, sequence_df.sample(n=10)])

sampled_sequence_df = sampled_sequence_df.drop_duplicates()
print(sampled_sequence_df)

original = sampled_sequence_df.iloc[0]
print(original)
sampled_sequence_df["dist_from_original"] = 0
for index, row in sampled_sequence_df.iterrows():

  lev_dist = Levenshtein.distance(original.sequence, row.sequence)
  print()

  divider = len(original.sequence) if len(original.sequence) > len(row.sequence) else len(row.sequence)
  lev_dist = lev_dist / divider
  lev_dist = 1 - lev_dist
  print(lev_dist)

  sampled_sequence_df.loc[index, "dist_from_original"] = lev_dist 

sampled_sequence_df = sampled_sequence_df.query('dist_from_original > 0.9')
sorted_sampled_sequence_df = sampled_sequence_df.sort_values("dist_from_original" , ascending=False)



print(sorted_sampled_sequence_df)
i = 0
for index1, row1 in sorted_sampled_sequence_df.iterrows():
  dist_df = pd.DataFrame(columns=['version1', 'country_code1', 'region_name1', 'version2', 'country_code2', 'region_name2', 'dist'])
  for index2, row2 in sorted_sampled_sequence_df.query("dist_from_original > " + str(row1.dist_from_original)).iterrows():
    lev_dist = Levenshtein.distance(row1.sequence, row2.sequence)
    divider = len(row1.sequence) if len(row1.sequence) > len(row2.sequence) else len(row2.sequence)
    lev_dist = lev_dist / divider
    lev_dist = 1 - lev_dist
    print(str(index1) + " " + str(index2) + " " + str(lev_dist))
    s = pd.Series([row1.version, row1.country_code, row1.region_name, row2.version, row2.country_code, row2.region_name, lev_dist], index=dist_df.columns)
    dist_df = pd.concat([dist_df, pd.DataFrame([s])]) 
  print(dist_df)
  dist_df = dist_df.reset_index()
  ddf = dist_df.groupby('version1')
  dddf = dist_df.loc[ddf['dist'].idxmax(),:]

  print(dddf)
  if i == 0:
    dddf.to_csv(filename)
  else:
    dddf.to_csv(filename, mode='a', header=False)
  i = i + 1
