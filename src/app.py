from calc import count_words, avg_word_length
from service import fetch_text

print("Running TextAnalyzer")

URL = "https://www.gutenberg.org/files/1342/1342-0.txt"

try:
    text = fetch_text(URL)
    words = count_words(text)
    avg_len = avg_word_length(text.split())
    print(f"Words: {words}, Avg length: {avg_len:.2f}")
except Exception as e:
    print(f"Error: {e}")
