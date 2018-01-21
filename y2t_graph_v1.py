import nltk, networkx
from pattern.en import tag

id = "SKhmFSV-XB0_12_18"
sentences2 = ['A little girl shown singing.', 'A young girl is singing on a stage.', 'A girl is singing', 'A girl is singing on a stage.', 'A girl is singing.', 'a girl is singing a song', 'a girl is singing', 'A girl is singing.', 'A girl is singing.', 'A lady is singing on the stage.', 'A lady is singing.', 'a woman singing a song', 'A young girl is singing on stage.', 'A Girl singing in the event.']
# sentences2 = ['A girl is singing a song on stage ']

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def tag_sentence(sentence):
    # words = nltk.tokenize.word_tokenize(sentence)
    # nltk.corpus.brown.tagged_words(tagset='universal')
    # print nltk.pos_tag(words)
    return tag(sentence)
    # return pos_tag, words

def find_subject(tags):
    for i in range(len(tags)):
        word, tag = tags[i]
        if tag == "NN" or tag == "NNS":
            return word
        elif "VB" in tag:
            return ""
    return ""

def after_verbs(word):
    if word == "off" or word == "up" or word == "down" or word == "out":
        return True
    return False

def find_verb(tags):
    verb = ""
    two_parts = False
    len_tags = len(tags)
    for i in range(len_tags):
        word, tag = tags[i]
        if "VB" in tag:
            verb += word
            idx = i + 1
            if idx >= len_tags:
                return verb
            next_word, next_tag = tags[idx]
            
            while "VB" in next_tag or ((word == "is" or tag == "are") and next_tag == "NN" and "ing" in next_word):
                verb += " " + next_word
                idx += 1
                if idx >= len_tags:
                    return verb
                next_word, next_tag = tags[idx]
                
            if "RP" == next_tag or after_verbs(next_word):
                verb += " " + next_word
            return verb

    return verb

def find_complement(tags, verb):
    if len(verb) == 0:
        return ""
    verb_parts = set(verb.split(" "))
    len_tags = len(tags)
    idx = -1
    for i in range(len_tags):
        word, tag = tags[i]
        if word in verb_parts:
            idx = i
            break
    while word in verb_parts:
        idx += 1
        if idx >= len_tags:
            return ""
        word, tag = tags[idx]
    
    for i in range(idx, len_tags):
        word, tag = tags[i]
        if tag == "NN" or tag == "NNS":
            return word
    return ""

def find_time_or_location(tags, idx):
    #TODO: poate trebuie pus sa mearga maxim 3-4 cuvinte
    for i in range(idx + 1, len(tags)):
        word, tag = tags[i]
        if tag == "NN" or tag == "NNS":
            return word
    return ""

def is_preposition(word):
    if word == "on" or word == "in" or word == "of" or word == "with" or word == "into":
        return True
    elif word == "from" or word == "down" or word == "at" or word == "out" or word == "by":
        return True
    elif word == "over" or word == "through" or word == "for" or word == "off" or word == "while":
        return True
    return False

def find_prepositions(tags):
    prepositions = {}
    for i in range(len(tags)):
        word, tag = tags[i]
        if is_preposition(word):
            prepositions[word] = find_time_or_location(tags, i)
    return prepositions

def parse_sentence(sentence):
    tags = tag_sentence(sentence)
    # print tags
    subject = find_subject(tags)
    verb = find_verb(tags)
    complement = find_complement(tags, verb)
    prepositions = find_prepositions(tags)
    return {
        "subject": subject,
        "verb": verb,
        "complement": complement,
        "prepositions": prepositions
    }

def parse_sentences(sentences):
    sentences_lower = [s.lower() for s in sentences]
    sentences_unique = list(set(sentences_lower))
    for sentence in sentences_unique:
        if is_ascii(sentence) is False:
            continue
        print ""
        print sentence
        print parse_sentence(sentence)

def debug():
    # print "abc"
    # parse_sentences(sentences2)
    parse_sentences(['a man fell off a motorcycle.', 
    'the woman is pouring liquid over the pasta.',
    "a cat is being slid around the floor.",
    "someone is decorating food on a plate.",
    "a stack of tortillas is being sliced.",
    "a dolphin jumps out the water in the ocean.",
    "a man is preparing to marinate some chicken.",
    "a car blows up."])
    
def run():
    import random
    import pickle
    file = "./youtube2text_iccv15/dict_movieID_caption.pkl"
    with open(file, 'rb') as f:
        data = pickle.load(f)
        for mov_id in data:
            # parse_sentences(data[mov_id])
            idx = random.randint(0, len(data[mov_id]) - 1)
            parse_sentences([data[mov_id][idx]])

def main():
    # debug()
    run()        
if __name__ == "__main__":
    main()