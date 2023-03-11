import pickle
import re

import nltk

lemmatize = nltk.WordNetLemmatizer()


def lemmatize_text(in_text):
    # удаляем неалфавитные символы
    out_text = re.sub("[^a-zA-Z]", " ", in_text)
    # токенизируем слова
    # text = nltk.word_tokenize(text,language = "english")
    # лемматирзируем слова
    out_text = [lemmatize.lemmatize(word) for word in out_text]
    # соединяем слова
    out_text = "".join(out_text)
    return out_text


def pred(text):
    if 'Ошибка' not in text:
        pkl_filename_tfidf = "Pickle_RL_Model_tfidf.pkl"
        pkl_filename_nb = "Pickle_RL_Model_nb.pkl"
        pkl_filename_logreg = "Pickle_RL_Model_logreg.pkl"
        pkl_filename_svm = "Pickle_RL_Model_svm.pkl"
        with open(pkl_filename_tfidf, 'rb') as file:
            pickled_tfidf_vectorizer = pickle.load(file)
        texts_for_predict = text
        test_text = [lemmatize_text(text) for text in texts_for_predict]
        X_test_vector = pickled_tfidf_vectorizer.transform(test_text)
        r = []
        for i in [pkl_filename_nb, pkl_filename_svm, pkl_filename_logreg]:
            with open(i, 'rb') as file:
                pickled_nb_model = pickle.load(file)
            Y_test_pred = pickled_nb_model.predict(X_test_vector.toarray())
            r.append(list(Y_test_pred)[0] - 1)

        return r
    else:
        print(text)
        return
