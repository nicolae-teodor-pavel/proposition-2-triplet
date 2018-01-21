import pickle, nltk, random
from pattern.en import tag
import operator

file = "./youtube2text_iccv15/dict_movieID_caption.pkl"
sentences_cnt = 0
prepositions = set()
cnt = 0
on_cnt = 0
in_cnt = 0
into_cnt = 0
over_cnt = 0
under_cnt = 0
until_cnt = 0
after_cnt = 0
at_cnt = 0
# the_cnt = 0
other_cnt = 0
freq = {}
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

with open(file, 'rb') as f:
    data = pickle.load(f)
    nltk.corpus.brown.tagged_words(tagset='universal')
    # print data
    for mov_id in data:
        for sentence in data[mov_id]:
            if is_ascii(sentence) is False:
                continue
            sentences_cnt += 1
            pos_tags = tag(sentence)
            for (word, pos_tag) in pos_tags:
                if "IN" in pos_tag:
                    cnt += 1
                    word = word.lower()
                    if word not in freq:
                        freq[word] = 0
                    freq[word] += 1
                    # if word not in prepositions:
                    #     prepositions.add(word)
                    # if word == "on":
                    #     on_cnt += 1
                    # elif word == "in":
                    #     in_cnt += 1
                    # elif word == "into":
                    #     into_cnt += 1
                    # elif word == "at":
                    #     at_cnt += 1
                    # elif word == "over":
                    #     over_cnt += 1
                    # elif word == "under":
                    #     under_cnt += 1
                    # elif word == "after":
                    #     after_cnt += 1
                    # elif word == "until":
                    #     until_cnt += 1
                    
                    # # elif word == "the":
                    # #     the_cnt += 1
                    # else:
                    #     other_cnt += 1
    sorted_x = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
    print cnt
    top5 = 0
    top10 = 0
    top15 = 0
    top20 = 0
    for i in range(20):
        word, word_cnt = sorted_x[i]
        print i, word, word_cnt
        if i < 5:
            top5 += word_cnt
        if i < 10:
            top10 += word_cnt
        if i < 15:
            top15 += word_cnt
        if i < 20:
            top20 += word_cnt
    
    print "top5", top5, 1.0 * top5 / cnt * 100
    print "top10", top10, 1.0 * top10 / cnt * 100
    print "top15", top15, 1.0 * top15 / cnt * 100
    print "top20", top20, 1.0 * top20 / cnt * 100
    # print prepositions
    # print "cnt", cnt
    # print "on_cnt", on_cnt
    # print "in_cnt", in_cnt
    # print "into_cnt", into_cnt
    # print "at_cnt", at_cnt
    # print "over_cnt", over_cnt
    # print "under_cnt", under_cnt
    # print "after_cnt", after_cnt
    # print "until_cnt", until_cnt
    # # print "the_cnt", the_cnt
    # print "other_cnt", other_cnt

        