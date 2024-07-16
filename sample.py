# Copyright 2021 Xilinx Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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