import re
from collections import Counter

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def count_words(text):
    words = text.split()
    return len(words)

def word_frequency(text):
    words = text.split()
    frequency = Counter(words)
    return frequency

def most_common_word(text):
    frequency = word_frequency(text)
    most_common = frequency.most_common(1)
    return most_common[0] if most_common else None

def main():
    text = input("Enter a paragraph of text: ")

    cleaned_text = clean_text(text)
    word_count = count_words(cleaned_text)
    frequency = word_frequency(cleaned_text)
    common_word = most_common_word(cleaned_text)

    print(f"\nTotal number of words: {word_count}")
    print("\nWord frequencies:")
    for word, count in frequency.items():
        print(f"{word}: {count}")

    if common_word:
        print(f"\nMost common word: '{common_word[0]}' with {common_word[1]} occurrences.")
    else:
        print("\nNo words found.")

if __name__ == "__main__":
    main()