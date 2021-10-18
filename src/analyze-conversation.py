from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords, nps_chat
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import glob
import sys

def get_words(txt):
    words = nltk.word_tokenize(txt)

    # remove stop words
    stop_words_list = list(stopwords.words('english'))
    stop_words_list.append('and')
    stop_words_list.append('or')

    words = list(filter(
        lambda e: len(e) >= 3 and e.lower() not in stop_words_list,
        words
    ))

    # remove punctuation
    words = [ word.lower() for word in words if word.isalpha() ]

    # lemmatize words
    words = [ WordNetLemmatizer().lemmatize(word) for word in words ]

    return words

def perform_classification(feature_set):
    training_size = int(len(feature_set) * 0.1)
    train_set, test_set = feature_set[training_size:], feature_set[:training_size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print('Accuracy is : ', nltk.classify.accuracy(classifier, test_set))
    return classifier

corpus_dir = '/opt/corpus/'
files = list(glob.glob('%s/*.txt' % corpus_dir))

qc = int(len(files) / 4)
files = list(map(lambda e: e.replace(corpus_dir, ''), files))

ids = [
    f.replace('question_', '').replace('.txt', '')
    for f in files
    if 'question' in f
]

corpus = PlaintextCorpusReader(corpus_dir, files)

posts = nltk.corpus.nps_chat.xml_posts()

# feature_list = []
# for i in range(len(ids)):
#     txt_q = corpus.raw('question_%s.txt' % ids[i])
#     features_q = {}
#     words = nltk.word_tokenize(txt_q)
#     for word in words:
#         features_q['contains({})'.format(word.lower())] = True
#     # class = ['whQuestion', 'Emotion', 'System', 'Continuer', 'ynQuestion', 'Bye', 'Accept', 'Reject', 'Greet', 'yAnswer', 'Statement']
#     feature_list.append((features_q, 'whQuestion'))

#     txt_a = corpus.raw('answer_%s.txt' % ids[i])
#     features_a = {}
#     words = nltk.word_tokenize(txt_a)
#     for word in words:
#         features_a['contains({})'.format(word.lower())] = True
#     # class = ['whQuestion', 'Emotion', 'System', 'Continuer', 'ynQuestion', 'Bye', 'Accept', 'Reject', 'Greet', 'yAnswer', 'Statement']
#     feature_list.append((features_a, 'Statement'))

feature_list = []
for post in posts:
    post_text = post.text
    features = {}
    words = nltk.word_tokenize(post_text)
    for word in words:
        features['contains({})'.format(word.lower())] = True
    feature_list.append((features, post.get('class')))

classifier = perform_classification(feature_list)

question_word_list = set(['what', 'where', 'when','how','why','did','do','does','have','has','am','is','are','can','could','may','would','will','should'
"didn't","doesn't","haven't","isn't","aren't","can't","couldn't","wouldn't","won't","shouldn't",'?'])

def predict_question(text, classifier):
    words = nltk.word_tokenize(text.lower())        
    if question_word_list.intersection(words) == False:
        return 0
    if '?' in text:
        return 1
    
    features = {}
    for word in words:
        features['contains({})'.format(word.lower())] = True            
    
    prediction_result = classifier.classify(features)
    if prediction_result == 'whQuestion' or prediction_result == 'ynQuestion':
        return 1
    return 0

with open('/opt/samples/%s' % sys.argv[1], 'r') as h:
    conversation = h.read().split('\n')

headers = conversation[0].split('|')
csv_data = [ row.split('|') for row in conversation[1:] ]
csv_data = list(map(lambda e: { headers[i]: e[i] for i in range(len(e))}, csv_data))

print(csv_data)

questions = []
for entry in csv_data:    
    if predict_question(entry['message'], classifier):
        questions.append({
            'txt': entry['message'],
            'words': get_words(entry['message'])
        })
    else:
        words = get_words(entry['message'])
        for q in questions:
            w = list(set(words) & set(q['words']))
            if len(w) > 1:
                w.sort()
                wk = '-'.join(w)
                print('**********', wk, q['txt'], entry['message'])
