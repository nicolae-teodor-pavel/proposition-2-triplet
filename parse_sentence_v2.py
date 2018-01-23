import json
import nltk
from parse_sentence_v1 import parse_sentence, parse_sentences, is_ascii
import re

def convert_pos_tag_to_string(pos_tag):
    return " ".join([w for w, t in pos_tag])

def parse_subject(sentence, chunkes, tagged):
    f_word, f_tag = tagged[0]
    s_word, s_tag =  tagged[1] if len(tagged) > 1 else (None, None)
    if f_tag == "RB":
        idx = sentence.find(f_word)
        sentence = sentence[idx+len(f_word):]
    if f_tag == "IN" and s_tag == ",":
        idx = sentence.find(f_word)
        sentence = sentence[idx+len(f_word)+len(s_word):]
    
    for s in chunkes.subtrees():
        if s.label() == "NP":
            np_concat = convert_pos_tag_to_string(s.leaves())#" ".join([w for w, t in s.leaves()])
            if sentence.startswith(np_concat) or sentence.startswith(np_concat, 1):
                return np_concat, 0
    if f_tag == "PRP":
        return f_word, 0
    return None, -1

def parse_verbs(sentence):
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    # print tagged
    grammar = """VERB: {<VB.?>+(<RB>?<RP>?<TO><VB>)?}"""
    chunkParser = nltk.RegexpParser(grammar)
    chunkes = chunkParser.parse(tagged)
    return parse_verbs_from_chunckes(sentence, chunkes)

def remove_followed_if_followed_by(verb, sentence):
    string = "followed"
    string_by = "followed by"
    if string not in verb:
        return verb
    idx = sentence.find(verb) + len(verb)
    if string == sentence[(idx-len(string)):idx] and sentence[(idx+1):(idx+3)] == "by":
        return verb[:-len(string)-1]
    return verb

    
def parse_verbs_from_chunckes(sentence, chunkes):
    verbs = []
    for s in chunkes.subtrees(): 
        if s.label() == "VERB":
            # composed_verb = s.leaves()
            verb = convert_pos_tag_to_string(s.leaves())
            verb = remove_followed_if_followed_by(verb, sentence)
            if len(verb) != 0:
                verbs.append(verb)
    return verbs

def parse_verb_from_verbs(sentence, verbs):
    for verb in verbs:
        if verb in sentence:
            return verb, sentence.find(verb)
    return None, -1

def parse_simple_sentence(sentence, verbs, p_subject):
    print "parse_simple_sentence", sentence
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    
    grammar = """NP: {<DT>?<CD>?<JJ>*,*<CC>*<JJ>*<NN.*>+(<CC><DT>?<JJ>*<NN.*>+)?}
                VERB: {<VB.?>*}
                """
    chunkParser = nltk.RegexpParser(grammar)
    chunkes = chunkParser.parse(tagged)
    # print chunkes
    
    verb, verb_positon = parse_verb_from_verbs(sentence, verbs)
    subject, subject_position = p_subject, -1
    if verb_positon > 0:
        subject, subject_position = parse_subject(sentence, chunkes, tagged)
    
    # print "Subject", subject, subject_position
    # print "Verb", verb, verb_positon
    return subject, verb

_AS_ = " as "
_WHILE_ = " while "
_FOLLOWEDBY_ = " followed by "
_BEFORE_ = " before "

def simultaneously_actions(sentence):
    if _AS_ in sentence or _WHILE_ in sentence or _BEFORE_ in sentence:
        return True
    return False

def split_by_idx(sentence, idx1, idx2):
    return [sentence[:idx1], sentence[(idx2):]]
     
def split_simultaneously_actions(sentence):
    idx = sentence.find(_AS_)
    if idx != -1:
        return split_by_idx(sentence, idx, idx + len(_AS_))
    idx = sentence.find(_WHILE_)
    if idx != -1:
        return split_by_idx(sentence, idx, idx + len(_WHILE_))
    idx = sentence.find(_BEFORE_)
    if idx != -1:
        return split_by_idx(sentence, idx, idx + len(_BEFORE_))
        
    return [sentence]

def is_followed_by_sentence(sentence, verbs):
    idx = sentence.find(_FOLLOWEDBY_)
    sentences = sentence.split(_FOLLOWEDBY_)
    for s in sentences:
        has_verb = False
        for verb in verbs:
            if verb in s:
                has_verb = True
                break
        if has_verb is False:
            return False
    return True

def split_followed_by(sentence, verbs):
    idx = sentence.find(_FOLLOWEDBY_)
    posible_sentences = sentence.split(_FOLLOWEDBY_)
    sentences = []
    for s in posible_sentences:
        has_verb = False
        for verb in verbs:
            if verb in s:
                has_verb = True
                break
        if has_verb is False:
            sentences[-1] += _FOLLOWEDBY_ + s
        else:
            sentences.append(s)
    return sentences

grammar_complex = """
                COMPLEX: {<VB.?>+([\s\S]*)?<CC>([\s\S]*)<VB.?>+}
                """
def is_complex_sentence(sentence):
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    # print tagged
    grammar = grammar_complex
    chunkParser = nltk.RegexpParser(grammar)
    chunkes = chunkParser.parse(tagged)
    for s in chunkes.subtrees(): 
        if s.label() == "COMPLEX":
            return True
    return False

def split_complex_sentence(sentence):
    tokenized = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized)
    
    grammar = grammar_complex
    chunkParser = nltk.RegexpParser(grammar)
    chunkes = chunkParser.parse(tagged)
    
    split_by = []
    for s in chunkes.subtrees(): 
        if s.label() == "COMPLEX":
            string = convert_pos_tag_to_string(s.leaves())

            idx = string.find(" and ")
            split_by += [string[idx+1:min(idx+6,len(string))]]
    sentences = []
    remainder = sentence
    for spliter in split_by:
        idx = remainder.find(spliter)
        sentences += [remainder[:idx]]
        remainder = remainder[(idx+4):]
    sentences += [remainder]
    return sentences

def create_simple_senteces(sentence, verbs):
    sentences = []
    if simultaneously_actions(sentence):
        sentences += split_simultaneously_actions(sentence)
    elif is_complex_sentence(sentence):
        sentences += split_complex_sentence(sentence)
    elif is_followed_by_sentence(sentence, verbs):
        sentences += split_followed_by(sentence, verbs)
    else:
        return [sentence]
    if len(sentences) == 1:
        return [sentences[0]]
    simple_sentences = []
    for s in sentences:
        simple_sentences += create_simple_senteces(s, verbs)
    return simple_sentences

def parse_file():
    file = "./data/train.json"
    data = json.load(open(file))
    cnt = 0
    cnt_sentences = 0
    for mov_id in data:
        cnt += 1
        if cnt == 30:
            break
        print mov_id
        print data[mov_id]["sentences"]
        print ""
        for sentence in data[mov_id]["sentences"]:
            if is_ascii(sentence) is False:
                continue
            cnt_sentences += 1
            print sentence
            print ""
            verbs = parse_verbs(sentence)
            print "Verbs", verbs
            simple_sentences = create_simple_senteces(sentence, verbs)
            # print simple_sentences
            p_subject = None
            for simple_sentence in simple_sentences:
                p_subject, p_verb = parse_simple_sentence(simple_sentence, verbs, p_subject)
                print "Subject", p_subject
                print "Verb", p_verb
                print ""
        print "----------"
        print ""
    print cnt_sentences

def debug():
    # sentence = " Then the chef places the ingredients in a salad bowl."
    # sentence = "After,the ball is placed on the ground and he picks it up and hits it as if he's playing baseball."
    # sentence = "A girl is seen climbing across a set of monkey bars followed by her waving to the camera."
    # sentence = "Various clips begin to play and it briefly shows parts of a city, then most of it is of men outdoors and playing soccer on sand in a middle of city and occasionally blue words pop up on the screen when certain plays in the game are made."
    sentence = "He continues laying tiles on the floor while standing down to speak to the camera."
    verbs = parse_verbs(sentence)
    print verbs
    simple_sentences = create_simple_senteces(sentence, verbs)
    print simple_sentences
    p_s = None
    for simple_sentence in simple_sentences:
        p_s, p_v = parse_simple_sentence(simple_sentence, verbs, p_s)
    
def main():
    # debug()
    parse_file()
        
if __name__ == "__main__":
    main()