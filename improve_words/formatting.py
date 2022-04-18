with open('fixed_words.txt', 'r') as file:
    words = [line.rstrip() for line in file]

with open('fixed_words_2.txt', 'w') as file:
    for word in words:
        file.write('\t"' + word + '",\n')