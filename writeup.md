## Book Recommender Engine
This project was to build a book recommender engine that took in a unique key that would identfy a book within the science fiction and speculative fiction genres, and deliver back recommendations based on shared keywords from reviews that rated the books highly. I gathered this data from Goodreads, primarily because it was easily to traverse through web scraping tools but partially because Goodreads uses a collaborative, rather than content-based, recommendation system. This meant that my engine would be able to make new recommendations based on information Goodreads wasn't previously using. I was also able to include book-specific keywords in my user information file to contextualize the cosine similarity score provided for each item.

### Design
I wanted to develop an engine that was primarily interpretable by the user. That led me to use a simple keyword-based system where users inputted a URL of a book that was known by Goodreads, and receive back recommendations within seconds as long as the book was within the dataset that I had scraped.
I also opted to include a word cloud (contained within word_cloud.py) due to its popularity and its interpretability as well. 

### Data
The data was scraped from Goodreads, a literary social networking site (two webscraping files used, webscraping.py and webscraping_metadata.py). Up to 30 reviews of any sentiment were gathered for each book and stored, along with metadata about the book and star-based ratings for each review left. Later this data was cleaned to exclude reviews that were lower than 4 stars or impractically short. My data initially came to 76 MB but was eventually pared down to 23 MB.

### Algorithms
I used NLTK's Rapid Automatic Keyword Extraction (RAKE) library to extract the most relevant keywords (contained within keyword_generation.py). The main algorithm I used involved the cosine similarity calculating ability from sklearn (contained within input_analysis_and_output.py). 

### Tools
* Selenium: web scraping
* NumPy, pandas: data processing and cleaning
* Re: further data processing
* TfidVectorizer/Counter: eliminating overly common and uncommon words
* Levenshtein Distance: spellchecker
* NLTK: tokenization
* WordCloud: topic visualization
* Sklearn's cosine_similarity: calculating cosine distance between texts
* Openpyxl: Excel export functionality

### Communication

I built a wordcloud (seen below) to illustrate some of the topics that were gathered during the recommendation engine's construction. I also presented on the engine using a PowerPoint file. I also built a simple export function that provided book recommendation information for a user through an Excel file. 

![image](https://user-images.githubusercontent.com/71529189/123396703-a0281680-d56f-11eb-9449-145a53a0405a.png)

![image](https://user-images.githubusercontent.com/71529189/123410788-b210b600-d57d-11eb-9eba-5363d4366608.png)
