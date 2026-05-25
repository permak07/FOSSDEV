import requests

print("Running TextAnalyzer")

URL = "https://www.gutenberg.org/files/1342/1342-0.txt"

try:
    response = requests.get(URL)
    print(f"Fetched {len(response.text)} characters")
except Exception as e:
    print(f"Error: {e}")