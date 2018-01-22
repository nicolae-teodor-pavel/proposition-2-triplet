import json
import nltk
from parse_sentence_v1 import parse_sentence, parse_sentences, is_ascii

def convert_pos_tag_to_string(pos_tag):
    return " ".join([w for w, t in pos_tag])

def parse_subject(sentence, chunkes, tagged):
    for s in chunkes.subtrees():
        if s.label() == "NP":
            np_concat = convert_pos_tag_to_string(s.leaves())#" ".join([w for w, t in s.leaves()])
            if sentence.startswith(np_concat) or sentence.startswith(np_concat, 1):
                return np_concat
    word, tag = tagged[0]
    if tag == "PRP":
        return word 
    return ""

def parse_verbs(sentence):
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    grammar = """VERB: {<VB.?>*}"""
    chunkParser = nltk.RegexpParser(grammar)
    chunkes = chunkParser.parse(tagged)
    return parse_verbs_from_chunckes(chunkes)

def parse_verbs_from_chunckes(chunkes):
    verbs = []
    for s in chunkes.subtrees(): 
        if s.label() == "VERB":
            verbs.append(" ".join([w for w, t in s.leaves()]))
    return verbs

def parse_verb_from_verbs(sentence, verbs):
    for verb in verbs:
        if verb in sentence:
            return verb
    return None 

def parse_simple_sentence(sentence, verbs):
    print "parse_simple_sentence", sentence
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    
    grammar = """NP: {<DT>?<JJ>*<NN.*>+}
                VERB: {<VB.?>*}
                """
    chunkParser = nltk.RegexpParser(grammar)
    chunkes = chunkParser.parse(tagged)

    # print chunkes
    print "Subject", parse_subject(sentence, chunkes, tagged)
    print "Verb", parse_verb_from_verbs(sentence, verbs)
    print ""

_AS_ = " as "
_WHILE_ = " while "

def simultaneously_actions(sentence):
    if _AS_ in sentence or _WHILE_ in sentence:
        return True
    return False

def split_by_idx(sentence, idx1, idx2):
    return [sentence[:idx1], sentence[(idx2):]]
     
def split_simultaneously_actions(sentence):
    idx_as = sentence.find(_AS_)
    if idx_as != -1:
        return split_by_idx(sentence, idx_as, idx_as + len(_AS_))
    idx_while = sentence.find(_WHILE_)
    if idx_while != -1:
        return split_by_idx(sentence, idx_while, idx_while + len(_WHILE_))
    return [sentence]

def is_complex_sentence(sentence):
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    grammar = """
                COMPLEX: {<CC><VB.?>+}
                """
    chunkParser = nltk.RegexpParser(grammar)
    chunkes = chunkParser.parse(tagged)
    for s in chunkes.subtrees(): 
        if s.label() == "COMPLEX":
            return True
    return False

def split_complex_sentence(sentence):
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    grammar = """
                COMPLEX: {<CC><VB.?>*}
                """
    chunkParser = nltk.RegexpParser(grammar)
    chunkes = chunkParser.parse(tagged)
    # print chunkes
    split_by = []
    for s in chunkes.subtrees(): 
        if s.label() == "COMPLEX":
            split_by += [convert_pos_tag_to_string(s.leaves())]
    
    sentences = []
    remainder = sentence
    for spliter in split_by:
        idx = remainder.find(spliter)
        sentences += [remainder[:idx]]
        remainder = remainder[(idx+4):]
    sentences += [remainder]
    return sentences

def parse_file():
    file = "./data/train.json"
    data = json.load(open(file))
    cnt = 0
    for mov_id in data:
        cnt += 1
        if cnt == 11:
            break
        print mov_id
        print data[mov_id]["sentences"]
        print ""
        for sentence in data[mov_id]["sentences"]:
            if is_ascii(sentence) is False:
                continue
            print sentence
            print ""
            verbs = parse_verbs(sentence)
            print "Verbs", verbs
            simple_sentences = []
            if simultaneously_actions(sentence):
                simple_sentences += split_simultaneously_actions(sentence)
            elif is_complex_sentence(sentence):
                simple_sentences += split_complex_sentence(sentence)
            else:
                simple_sentences = [sentence]
            
            for simple_sentence in simple_sentences:
                parse_simple_sentence(simple_sentence, verbs)
        print "----------"
        print ""

def main():
    # debug()
    parse_file()
        
if __name__ == "__main__":
    main()