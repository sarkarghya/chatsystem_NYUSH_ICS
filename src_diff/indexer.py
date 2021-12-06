# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
import pickle
import string

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n]
        
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)
 
    def indexing(self, m, l):
        """
        updates self.total_words and self.index
        m: message, l: current line number
        """
        for word in m.split():
            #Avoid if the word is the roman number
            if not (word[-1] == '.' and word[-2].isupper()):
                word = word.strip(string.punctuation) #else remove puncs
            if word not in self.index:
                self.index[word] = [l,]
                # Increment total_words when the word was not in dictionary
                self.total_words += 1 
            else:
                self.index[word].append(l)
    '''
    def indexing(self, m, l):
        """
        updates self.total_words and self.index
        m: message, l: current line number
        """
        for word in m.split():
            #Avoid if the word is the roman number
            if not (word[-1] == '.' and word[-2].isupper()):
                word = word.strip(string.punctuation) #else remove puncs
            self.total_words += 1 
            self.index.setdefault(word, []).append(l)
    '''
    # implement: query interface

#    def search(self, term):
#        msgs = [(ln, m) for ln, m in self.index.items() if term in m]
#        return msgs
                                    
    def search(self, term):
        msgs = []
        terms = term.split()
        if terms[0] in self.index:
            t_msgs = set((i, self.msgs[i].rstrip('\n')) for i in self.index[terms[0]])
            msgs.extend([x for x in t_msgs if term in x[1]])
        return sorted(msgs, key=lambda x: x[0])


class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # load poems
    def load_poems(self):
        lines = open(self.name, 'r').readlines()
        for l in lines:
            self.add_msg_and_index(l.rstrip())
    
    def get_poem(self, p):
        p_str = self.int2roman[p] + '.'
        p_next_str = self.int2roman[p + 1] + '.'
        temp = self.search(p_str)
        if temp:
            [(go_line, m)] = temp
        else:
            return []
        # in case of wrong number
        poem = []
        end = self.get_msg_size()
        while go_line < end:
            this_line = self.get_msg(go_line)
            if this_line == p_next_str:
                break
            poem.append(this_line)
            go_line += 1
        # poem = "\n".join(poem)
        return poem
    
if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    p3 = sonnets.get_poem(3)
    print(p3)
    s_love = sonnets.search("love")
    print(s_love)
