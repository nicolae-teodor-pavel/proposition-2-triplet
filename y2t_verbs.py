import pickle, nltk, random
file = "./youtube2text_iccv15/dict_movieID_caption.pkl"
sentences_cnt = 0
verb_tenses = set()
vbz_cnt = 0
vbz_sample = []
vbg_cnt = 0
vbg_sample = []
vbp_cnt = 0
vbp_sample = []
vb_cnt = 0
vb_sample = []
vbd_cnt = 0
vbd_sample = []
vbd_sample_id = []
vbn_cnt = 0
vbn_sample = []
vbother_cnt = 0
cnt = 0

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

with open(file, 'rb') as f:
    data = pickle.load(f)
    nltk.corpus.brown.tagged_words(tagset='universal')
    for mov_id in data:
        for sentence in data[mov_id]:
            if is_ascii(sentence) is False:
                continue
            sentences_cnt += 1
            text = nltk.tokenize.word_tokenize(sentence)
            pos_tag = nltk.pos_tag(text)
            for (s, tag) in pos_tag:
                if "VB" in tag:
                    cnt += 1
                    i = random.random()
                    if tag not in verb_tenses:
                        verb_tenses.add(tag)
                    if tag == "VBZ":
                        vbz_cnt += 1
                        if len(vbz_sample) < 10 and i < 0.1:
                            vbz_sample.append((sentence, s))
                    elif tag == "VBG":
                        vbg_cnt += 1
                        if len(vbg_sample) < 10 and i < 0.1:
                            vbg_sample.append((sentence, s))
                    elif tag == "VBP":
                        vbp_cnt += 1
                        if len(vbp_sample) < 10 and i < 0.1:
                            vbp_sample.append((sentence, s))
                    elif tag == "VB":
                        vb_cnt += 1
                        if len(vb_sample) < 10 and i < 0.1:
                            vb_sample.append((sentence, s))
                    elif tag == "VBD":
                        vbd_cnt += 1
                        if len(vbd_sample) < 10 and i < 0.1:
                            vbd_sample.append((sentence, s))
                            vbd_sample_id.append(mov_id)
                    elif tag == "VBN":
                        vbn_cnt += 1
                        if len(vbn_sample) < 10 and i < 0.1:
                            vbn_sample.append((sentence, s))
                    else:
                        vbother_cnt += 1
    print "sentences_cnt", sentences_cnt

    print ""
    print "----------------------------"
    print ""

    print verb_tenses
    print "verbs cnt", cnt

    print ""
    print "----------------------------"
    print ""

    print "vbz_cnt", vbz_cnt
    print "vbg_cnt", vbg_cnt
    print "vbp_cnt", vbp_cnt
    print "vb_cnt", vb_cnt
    print "vbd_cnt", vbd_cnt
    print "vbn_cnt", vbn_cnt
    print "vbother_cnt", vbother_cnt
    
    print ""
    print "----------------------------"
    print ""

    print "vbz_sample"
    print vbz_sample
    print "vbg_sample"
    print vbg_sample
    print "vbp_sample"
    print vbp_sample
    print "vb_sample"
    print vb_sample
    print "vbd_sample"
    print vbd_sample
    print vbd_sample_id
    print "vbn_sample"
    print vbn_sample
        