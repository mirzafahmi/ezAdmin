def create_acronym(phrase):
   acronym = ""
   words = phrase.split()
   for word in words:
      acronym += word[0].upper()
   return acronym