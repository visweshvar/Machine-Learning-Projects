PRONUNCIATION_CSV_PATH = "data/pronunciation.csv"

import csv, re

# Convert raw user input to a list of words
# TODO: convert numerical values to words
import re
import inflect

def tokenize(data):
    p = inflect.engine()
    tokens = re.findall(r"[\w']+|[.,!?;]", data.lower())
    processed_tokens = []
    for token in tokens:
        if token.isdigit():
            # Convert numerical values to words
            processed_tokens.extend(p.number_to_words(token).split())
        else:
            processed_tokens.append(token)
    return processed_tokens


def get_pronunciation(word):
  with open(PRONUNCIATION_CSV_PATH, 'rt') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      if word == row[0]:
        numbers = row[1].strip().split(' ')
        # map string to integers
        return list(map(int, numbers))
      