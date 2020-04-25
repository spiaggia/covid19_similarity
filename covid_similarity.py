import Levenshtein


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
for covid_nucleic_acid_sequence in covid_nucleic_acid_sequence_array:
#  print(covid_nucleic_acid_sequence_array_length)
  str_array1 = covid_nucleic_acid_sequence_array[1].splitlines()[1:]

  str1 = ""
  for x in str_array1:
      str1 += x

#  print(str1)

  str_array2 = covid_nucleic_acid_sequence.splitlines()[1:]

  str2 = ""
  for x in str_array2:
      str2 += x

#  print(str2)


  lev_dist = Levenshtein.distance(str1, str2)
  print(lev_dist)

  divider = len(str1) if len(str1) > len(str2) else len(str2)
  lev_dist = lev_dist / divider
  lev_dist = 1 - lev_dist


  print(lev_dist)
