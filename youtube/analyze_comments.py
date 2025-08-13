import pandas as pd
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams

# Read your comments file
df = pd.read_csv("youtube_comments.csv")

# Combine all comments into one big string
text = " ".join(df['comment'].dropna().astype(str))

# Lowercase & remove non-alphabet characters
text = re.sub(r'[^a-z\s]', '', text.lower())

# Tokenize into words
words = text.split()

# Remove stop words
stop_words = set(stopwords.words("english"))
cleaned_words = [w for w in words if w not in stop_words and len(w) > 1]

# Count single word frequencies
word_freq = Counter(cleaned_words).most_common(50)  # top 50

# Create bigrams & trigrams
bigrams = Counter(ngrams(cleaned_words, 2)).most_common(30)
trigrams = Counter(ngrams(cleaned_words, 3)).most_common(30)

# Save to CSV
pd.DataFrame(word_freq, columns=["word", "count"]).to_csv("word_frequency.csv", index=False)
pd.DataFrame([(" ".join(bg), count) for bg, count in bigrams], columns=["bigram", "count"]).to_csv("bigram_frequency.csv", index=False)
pd.DataFrame([(" ".join(tg), count) for tg, count in trigrams], columns=["trigram", "count"]).to_csv("trigram_frequency.csv", index=False)

print("\nTop Words:\n", word_freq[:10])
print("\nTop Bigrams:\n", bigrams[:10])
print("\nTop Trigrams:\n", trigrams[:10])
print("\n✅ Analysis complete — CSV files created.")
