## Steven Necola
## NLP - Spring 2022

class LanguageModel:

    unigramDict = {}
    unigramWithUnk = {}
    bigramDict = {}
    trigramDict = {}
    num_of_tokens = 0

    
    def __init__ (self):
        ## Preprocessing step 1 & 2
        # self.preprocessing_step1_2()
        self.create_unigram()
        #self.preprocessing_step3()
        self.create_unigram_with_unk()
        print('# of unique tokens in the training corpus (including </s> and <unk>) ', len(self.unigramDict))
        print('# of <s> in unigramDict ', self.unigramDict['<s>'])
        print('# of unique tokens in the training corpus (replaced single instance words with <unk>)', len(self.unigramWithUnk))
        print('# of <s> in unigramWithUnk', self.unigramWithUnk['<s>'])

        #num_of_tokens = self.get_num_of_tokens()
        print('# of tokens in the training corpus not including <s>', self.num_of_tokens)


    def preprocessing_step1_2(self):
        ## Lowercase all words in the training and test corpuses
        ## Add <s> and </s> to the sentenses
        with open('./train-Spring2022.txt', 'r') as f:
            with open('trainPreprocessed.txt', 'w') as w:
                for line in f:
                    ## Get all the words, set them to lowercase
                    tokens = line.split()
                    w.write('<s> ')
                    for token in tokens:
                        token = token.lower()
                        w.write(token)
                        w.write(' ')
                    w.write('</s>\n')
        pass

    def preprocessing_step3(self):
        ## Take the file from trainPreprocessed
        with open('./trainPreprocessed.txt','r') as f:
            with open('./trainUnk.txt','w') as w:
                for line in f:
                    tokens = line.split()
                    for token in tokens:
                        if self.unigramDict[token]==1:
                            token = '<unk>'
                        w.write(token)
                        w.write(' ')
                    w.write('\n')

    def create_unigram(self):
        ## Reads from the preprocessed Training file and populates the unigramDict variable
        with open('./trainPreprocessed.txt', 'r') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    try:
                        self.unigramDict[token]+=1
                    except KeyError:
                        self.unigramDict[token]=1
                    if (token == '<s>'):
                        continue
                    self.num_of_tokens+=1

    def create_unigram_with_unk(self):
        with open('./trainUnk.txt', 'r') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    try:
                        self.unigramWithUnk[token]+=1
                    except KeyError:
                        self.unigramWithUnk[token]=1

    def get_num_of_tokens(self):
        num_of_tokens = 0
        for token in self.unigramDict:
            if token == '<s>':
                continue
            num_of_tokens+=self.unigramDict[token]
        return num_of_tokens



if __name__ == "__main__":
    l = LanguageModel()