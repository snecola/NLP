## Steven Necola
## NLP - Spring 2022

class LanguageModel:

    ## Unigram variables
    unigramDict = {}
    unigramWithUnk = {}
    testDict = {}

    ## Bigram variables
    bigram_training = {}
    bigram_test = {}


    ## Test training data num of tokens
    num_of_tokens = 0

    
    def __init__ (self):
        ## Preprocessing step 1 & 2
        # self.preprocessing_step1_2()
        self.create_unigram()
        ## Preprocessing step 3
        #self.preprocessing_step3()
        self.create_unigram_with_unk()

        ## Answer to Question 1
        print('Question 1:')
        #print('# of unique tokens in the training corpus (including </s> and <unk>) ', len(self.unigramDict)+1)
        #print('# of <s> in unigramDict ', self.unigramDict['<s>'])
        print('# of unique tokens in the training corpus (replaced single instance words with <unk>)', len(self.unigramWithUnk)+1)
        #print('# of <s> in unigramWithUnk', self.unigramWithUnk['<s>'])

        ## Answer to Question 2
        print("Question 2:")
        #num_of_tokens = self.get_num_of_tokens()
        print('# of tokens in the training corpus not including <s>', self.num_of_tokens)

        ## Preprocessing for test
        # self.preprocessing_step1_2_test()
        self.create_test_dict()
        print("Question 3:")
        #print('# of unique tokens in the test corpus (including </s> and <unk>) ', len(self.testDict)+1)
        tokens_not_found, types_not_found = self.percentages_not_found()
        print("Percent of missing tokens", tokens_not_found * 100)
        print("Percent of missing word types", types_not_found * 100)

        print("Questio 4:")


        


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
                    if (token == '<s>'):
                        continue
                    try:
                        self.unigramDict[token]+=1
                    except KeyError:
                        self.unigramDict[token]=1
                    ## If the token is <s> we dont want to count it as num of tokens
                    # if (token == '<s>'):
                    #     continue
                    self.num_of_tokens+=1

    def create_unigram_with_unk(self):
        with open('./trainUnk.txt', 'r') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        continue
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

    def preprocessing_step1_2_test(self):
        ## Lowercase all words in the training and test corpuses
        ## Add <s> and </s> to the sentenses
        with open('./test.txt', 'r') as f:
            with open('testPreprocessed.txt', 'w') as w:
                for line in f:
                    ## Get all the words, set them to lowercase
                    tokens = line.split()
                    w.write('<s> ')
                    for token in tokens:
                        token = token.lower()
                        w.write(token)
                        w.write(' ')
                    w.write('</s>\n')

    def create_test_dict(self):
        ## Reads from the preprocessed test file and populates the testDict variable
        with open('./testPreprocessed.txt', 'r') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        continue
                    try:
                        self.testDict[token]+=1
                    except KeyError:
                        self.testDict[token]=1
                    ## If the token is <s> we dont want to count it as num of tokens
                    # if (token == '<s>'):
                    #     continue
                    self.num_of_tokens+=1

    def percentages_not_found(self):
        ## What percentage of tokens and word types did not occur in the training data
        num_of_tokens_not_found=0
        total_tokens=0
        total_types=0
        num_of_types_not_found=0
        for token in self.testDict:
            if token == '<s>': 
                continue
            total_tokens+=self.testDict[token]
            total_types+=1
            if token in self.unigramDict:
                continue
            num_of_tokens_not_found+=self.testDict[token]
            num_of_types_not_found+=1
        return [num_of_tokens_not_found/total_tokens, num_of_types_not_found/total_types]

    def train_bigrams(self):
        ## Training bigram
        with open('./trainUnk.txt', 'r') as f:
            


if __name__ == "__main__":
    l = LanguageModel()