import sys
import numpy as np
from PIL import Image
import wikipedia
from wordcloud import WordCloud, STOPWORDS
from bs4 import BeautifulSoup

try:
    a = input("Enter the name of the topic for the word cloud: ")
    search_results = wikipedia.search(a)

    most_relevant_title = None

    for title in search_results:
        try:
            page = wikipedia.page(title)
            if "disambiguation" not in page.summary.lower():
                most_relevant_title = title
                break
        except wikipedia.exceptions.DisambiguationError:
            continue

    if most_relevant_title is None:
        print("No relevant page found. Cannot create a word cloud.")
        sys.exit()

    page = wikipedia.page(most_relevant_title)
    html = page.html()
    lis = BeautifulSoup(html, features="html.parser").find_all('li')
    text = " ".join([li.get_text() for li in lis])

    bg = np.array(Image.open("black.jpg"))
    unwanted_words = set(STOPWORDS)
    wordcloud = WordCloud(
        background_color="black",
        max_words=400,
        mask=bg,
        stopwords=unwanted_words
    )
    wordcloud.generate(text)
    wordcloud.to_file("sample2.png")
    print("Word cloud created successfully as 'sample2.png'.")

except wikipedia.exceptions.DisambiguationError:
    print("Disambiguation error occurred. Cannot create a word cloud.")
except wikipedia.exceptions.HTTPTimeoutError:
    print("HTTP timeout error occurred. Please check your internet connection.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

