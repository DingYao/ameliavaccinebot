import re


def checkNric(string):
  if not re.match(r'[ST][0-9]{7}[A-Z]', string):
    return False
  if not checkNricChecksum(string):
    return False
  return True


def checkNricChecksum(string):
  weights = [2, 7, 6, 5, 4, 3, 2]
  checksums = ['J', 'Z', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
  sum = 0
  for w, d in zip(string[1:8], weights):
    sum += int(w) * d
  if string[0] == 'T':
    sum += 4
  remainder = sum % 11
  if string[-1] != checksums[remainder]:
    return False
  return True