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
dist_df = pd.DataFrame(columns=['version1', 'country_code1', 'region_name1', 'version2', 'country_code2', 'region_name2', 'dist'])


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
  sampled_sequence_df = pd.concat([sampled_sequence_df, country_sequence_df.sample(n=min([10, len(country_sequence_df)]))])

sampled_sequence_df = sampled_sequence_df.drop_duplicates()
print(sampled_sequence_df)
i = 0
for index, row1 in sampled_sequence_df.iterrows():
  
  version1 = row1.version
  for index2, row2 in sampled_sequence_df.iterrows():
    version2 = row2.version
    if version1 != version2:

      country_code1 = row1["country_code"] 
      country_code2 = row2["country_code"] 

      region_name1 = row1["region_name"] 
      region_name2 = row2["region_name"] 

      covid_nucleic_acid_sequence1 = row1["sequence"]
      covid_nucleic_acid_sequence2 = row2["sequence"]

      lev_dist = Levenshtein.distance(covid_nucleic_acid_sequence1, covid_nucleic_acid_sequence2)

      divider = len(covid_nucleic_acid_sequence1) if len(covid_nucleic_acid_sequence1) > len(covid_nucleic_acid_sequence2) else len(covid_nucleic_acid_sequence2)
      lev_dist = lev_dist / divider
      lev_dist = 1 - lev_dist
      print(str(index) + " " + str(index2) + " " + str(lev_dist))
      s = pd.Series([version1, country_code1, region_name1, version2, country_code2, region_name2, lev_dist], index=dist_df.columns)
      dist_df = pd.DataFrame([s])
      if i == 0:
        dist_df.to_csv(filename)
      else:
        dist_df.to_csv(filename, mode='a', header=False)
      i = i + 1
