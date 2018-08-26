We are interested in evaluating complexity of texts in German. More broadly, we amay also want to clasify the texts based on their sentiment, complexity or other.

We may want to try some of the followng:

# NLTK
[source](https://update.hanser-fachbuch.de/2013/09/artikelreihe-python-3-nltk-natural-language-toolkit/)

## Text Complexity

```python
import ntlk
ntlk.download()

words = list(text1)
words = [word for word in words if word.isalpha()] # removes special chars
diff_words = set(words) # uniuqe words
diversity = len(diff_words) / float(len(words))
diversity

fdist1 = ntlk.FreqDist(text1)
frequencies = fdist1.items()
frequencies[:30]
[ ... ]
frequencies[-30:]
[ ... ]

fdist1.plot(50, cumulative=True)
```

## Readability index
The [following website](https://stackoverflow.com/questions/35900029/average-sentence-length-for-every-text-in-corpus-python3-nltk) gives couple of nice examples of evaluating a complexity in texts. Iti usually relies on some list of "hard words" that are either predefined or sleected as e.g. very long words in the text. Some of that may apply only for english. To get some ideas also for German, check the [following listing](http://www.textquest.de/pages/en/analysis-of-texts/readability-analysis.php?lang=EN) of readibility formulas for german language.

```python
import spacy
from textstat.textstat import textstatistics, easy_word_set, legacy_round
 
# Splits the text into sentences, using 
# Spacy's sentence segmentation which can 
# be found at https://spacy.io/usage/spacy-101
def break_sentences(text):
    nlp = spacy.load('en')
    doc = nlp(text)
    return doc.sents
 
# Returns Number of Words in the text
def word_count(text):
    sentences = break_sentences(text)
    words = 0
    for sentence in sentences:
        words += len([token for token in sentence])
    return words
 
# Returns the number of sentences in the text
def sentence_count(text):
    sentences = break_sentences(text)
    return len(sentences)
 
# Returns average sentence length
def avg_sentence_length(self, text):
    words = word_count(text)
    sentences = sentence_count(text)
    average_sentence_length = float(words / sentences)
    return average_sentence_length
 
# Textstat is a python package, to calculate statistics from 
# text to determine readability, 
# complexity and grade level of a particular corpus.
# Package can be found at https://pypi.python.org/pypi/textstat
def syllables_count(word):
    return textstatistics().syllable_count(word)
 
# Returns the average number of syllables per
# word in the text
def avg_syllables_per_word(text):
    syllable = syllables_count(text)
    words = word_count(text)
    ASPW = float(syllable) / float(words)
    return legacy_round(ASPW, 1)
 
# Return total Difficult Words in a text
def difficult_words(text):
 
    # Find all words in the text
    words = []
    sentences = break_sentences(text)
    for sentence in sentences:
        words += [token for token in sentence]
 
    # difficult words are those with syllables >= 2
    # easy_word_set is provide by Textstat as 
    # a list of common words
    diff_words_set = set()
     
    for word in words:
        syllable_count = syllables_count(word)
        if word not in easy_word_set and syllable_count >= 2:
            diff_words_set.add(word)
 
    return len(diff_words_set)
 
# A word is polysyllablic if it has more than 3 syllables
# this functions returns the number of all such words 
# present in the text
def poly_syllable_count(text):
    count = 0
    words = []
    sentences = break_sentences(text)
    for sentence in sentences:
        words += [token for token in sentence]
     
 
    for word in words:
        syllable_count = syllables_count(word)
        if syllable_count >= 3:
            count += 1
    return count
 
```

The [following paper](http://www.sfs.uni-tuebingen.de/~dm/papers/Hancke.Vajjala.Meurers-12.pdf) discuss assesing German text readability.

Another option is using this `readability` module that also supports German:
https://pypi.org/project/readability/

# Other Resources
As a proxy for text complexity, we may want to use sentence length. Check out this [example](https://stackoverflow.com/questions/35900029/average-sentence-length-for-every-text-in-corpus-python3-nltk):

## Clasifying Texts

This is a toy example but potentially useful.

```python
import nltk
import random

def gender_features(word):
    return {'last_letter': word[-1]}

def classify(name):
    return classifier.classify(gender_features(name))

male_names     = nltk.corpus.names.words('male.txt')
female_names   = nltk.corpus.names.words('female.txt')
labelled_names = ([(name, 'male') for name in male_names] + 
[(name, 'female') for name in female_names])

random.shuffle(labelled_names)

featuresets = [(gender_features(n), g) for (n,g) in labelled_names]
train_set  = featuresets[500:]
test_set   = featuresets[:500]

classifier = nltk.NaiveBayesClassifier.train(train_set)
```

## SpaCy - multipurpose CNN model
[Source](https://spacy.io/models/de)

They provide a multi-task Convolutional Neural Net trained on big german texts, prepacked and available for us to use.
It can be used to extract parts of the speech, extracted named entities and assign dependencies. It would be also interesting to extract bi-grams or tri-grams from the texts.

```python
import spacy
from spacy.lang.de.examples import sentences

nlp = spacy.load('de_core_news_sm')
doc = nlp(sentences[0])
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_)
```