from ordnet import words_that_exist
from initial_words import words


""" 
To run this program:
    Create a file called ".env" in this folder. 
    Give it two variables: "http_proxy" and "https_proxy".
    Those can be from any proxy server provider. I use packetstream.io.
    Navigate to this folder in the terminal.
    Run 'bash run.sh'
"""

def main():
    without_duplicates = remove_duplicates(words)
    real_words = words_that_exist(without_duplicates)
    with open('fixed_words.txt', 'w') as f:
        for word in real_words:
            f.write(word + '\n')


def remove_duplicates(words: list[str]) -> list[str]:
    before = len(words)
    result = list(set(words))
    after = len(result)
    print(f'Removed {before - after} duplicate words')
    return result

if __name__ == '__main__':
    main()