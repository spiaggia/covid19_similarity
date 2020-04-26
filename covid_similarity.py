import Levenshtein
import pandas as pd


def pick_place_name(s):
  place = s
  if "Wuhan" in s:
    place = "Wuhan"
  if "TWN" in s:
    place = "TWN"
  if "USA" in s:
    place = "USA"
  return place

df = pd.DataFrame(columns=['place1', 'place2', 'dist'])

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

for num1 in range(1,10):
  covid_nucleic_acid_sequence_data1 = covid_nucleic_acid_sequence_array[num1]
  covid_nucleic_acid_sequence_definition1 = covid_nucleic_acid_sequence_data1.splitlines()[0]
  str_array1 = covid_nucleic_acid_sequence_data1.splitlines()[1:]

  covid_nucleic_acid_sequence1 = ""
  for x in str_array1:
      covid_nucleic_acid_sequence1 += x

#  print(covid_nucleic_acid_sequence1)
  for num2 in range(1,10):
    covid_nucleic_acid_sequence_data2 = covid_nucleic_acid_sequence_array[num2]
    covid_nucleic_acid_sequence_definition2 = covid_nucleic_acid_sequence_data2.splitlines()[0]
    str_array2 = covid_nucleic_acid_sequence_data2.splitlines()[1:]


    covid_nucleic_acid_sequence2 = ""
    for x in str_array2:
        covid_nucleic_acid_sequence2 += x

  #  print(covid_nucleic_acid_sequence2)

    if num1 != num2:
      lev_dist = Levenshtein.distance(covid_nucleic_acid_sequence1,covid_nucleic_acid_sequence2)
      print()
      place1 = pick_place_name(covid_nucleic_acid_sequence_definition1)
      place2 = pick_place_name(covid_nucleic_acid_sequence_definition2)

      divider = len(covid_nucleic_acid_sequence1) if len(covid_nucleic_acid_sequence1) > len(covid_nucleic_acid_sequence2) else len(covid_nucleic_acid_sequence2)
      lev_dist = lev_dist / divider
      lev_dist = 1 - lev_dist
      print(lev_dist)
      s = pd.Series([place1,place2,lev_dist], index=df.columns)
      print(s)
      df = df.append(s, ignore_index=True )
print(df.sort_values('dist'))


