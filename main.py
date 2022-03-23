# Steven Necola
# NLP - Spring 2022

import math


class LanguageModel:

    # Unigram variables
    unigramDict = {}
    unigramWithUnk = {}
    testDict = {}

    # Bigram variables
    bigram_training = {}
    bigram_test = {}

    # Test training data num of tokens
    total_num_of_tokens = 0
    num_of_tokens = 0
    num_of_tokens_unk = 0

    def __init__(self):
        # Preprocessing step 1 & 2
        self.preprocessing_step1_2()
        self.create_unigram()
        # Preprocessing step 3
        self.preprocessing_step3()
        self.create_unigram_with_unk()

        # Answer to Question 1
        print('Question 1:')
        # print('# of unique tokens in the training corpus (including </s> and <unk>) ', len(self.unigramDict)+1)
        # print('# of <s> in unigramDict ', self.unigramDict['<s>'])
        print('# of unique tokens in the training corpus (replaced single instance words with <unk>)', len(
            self.unigramWithUnk)+1)
        # print('# of <s> in unigramWithUnk', self.unigramWithUnk['<s>'])

        # Answer to Question 2
        print("Question 2:")
        #num_of_tokens = self.get_num_of_tokens()
        print('# of tokens in the training corpus not including <s>',
              self.num_of_tokens, self.total_num_of_tokens)

        # Preprocessing for test
        self.preprocessing_step1_2_test()
        self.create_test_dict()
        print("Question 3:")
        # print('# of unique tokens in the test corpus (including </s> and <unk>) ', len(self.testDict)+1)
        tokens_not_found, types_not_found = self.percentages_not_found()
        print("Percent of missing tokens", tokens_not_found * 100)
        print("Percent of missing word types", types_not_found * 100)

        print("Question 4:")
        self.preprocessing_step3_test()
        self.train_bigrams()
        bigram_tokens_not_found, bigram_types_not_found = self.bigrams_not_found()
        print("Percent of missing bigram tokens",
              bigram_tokens_not_found * 100)
        print("Percent of missing bigram types", bigram_types_not_found * 100)

        print("Question 5:")
        self.log_probability_unigram()
        print(self.get_num_of_tokens())

    def preprocessing_step1_2(self):
        # Lowercase all words in the training and test corpuses
        # Add <s> and </s> to the sentenses
        with open('./train-Spring2022.txt', 'r', encoding='utf8') as f:
            with open('trainPreprocessed.txt', 'w', encoding='utf8') as w:
                for line in f:
                    # Get all the words, set them to lowercase
                    tokens = line.split()
                    w.write('<s> ')
                    for token in tokens:
                        token = token.lower()
                        w.write(token)
                        w.write(' ')
                    w.write('</s>\n')

    def preprocessing_step3(self):
        # Take the file from trainPreprocessed
        with open('./trainPreprocessed.txt', 'r', encoding='utf8') as f:
            with open('./trainUnk.txt', 'w', encoding='utf8') as w:
                for line in f:
                    tokens = line.split()
                    for token in tokens:
                        if token == '<s>':
                            w.write(token)
                            w.write(' ')
                            continue
                        if self.unigramDict[token] == 1:
                            token = '<unk>'
                        w.write(token)
                        w.write(' ')
                    w.write('\n')

    def create_unigram(self):
        # Reads from the preprocessed Training file and populates the unigramDict variable
        with open('./trainPreprocessed.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        self.total_num_of_tokens += 1
                        continue
                    try:
                        self.unigramDict[token] += 1
                    except KeyError:
                        self.unigramDict[token] = 1
                    # Two counters, first one without <s> and the second with <s>
                    self.num_of_tokens += 1
                    self.total_num_of_tokens += 1

    def create_unigram_with_unk(self):
        with open('./trainUnk.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        continue
                    try:
                        self.unigramWithUnk[token] += 1
                    except KeyError:
                        self.unigramWithUnk[token] = 1
                    self.num_of_tokens_unk += 1

    def get_num_of_tokens(self):
        num_of_tokens = 0
        num_of_tokens_unk = 0
        for token in self.unigramDict:
            if token == '<s>':
                continue
            num_of_tokens += self.unigramDict[token]
        for token in self.unigramWithUnk:
            if token == '<s>':
                continue
            num_of_tokens_unk += self.unigramWithUnk[token]
        return [num_of_tokens, num_of_tokens_unk]

    def preprocessing_step1_2_test(self):
        # Lowercase all words in the training and test corpuses
        # Add <s> and </s> to the sentenses
        with open('./test.txt', 'r', encoding='utf8') as f:
            with open('testPreprocessed.txt', 'w', encoding='utf8') as w:
                for line in f:
                    # Get all the words, set them to lowercase
                    tokens = line.split()
                    w.write('<s> ')
                    for token in tokens:
                        token = token.lower()
                        w.write(token)
                        w.write(' ')
                    w.write('</s>\n')

    def preprocessing_step3_test(self):
        with open('./test.txt', 'r', encoding='utf8') as f:
            with open('testUnk.txt', 'w', encoding='utf8') as w:
                for line in f:
                    # Get all the words, set them to lowercase
                    tokens = line.split()
                    w.write('<s> ')
                    for token in tokens:
                        token = token.lower()
                        if token in self.unigramWithUnk:
                            w.write(token)
                            w.write(' ')
                        else:
                            w.write('<unk> ')
                    w.write('</s>\n')

    def create_test_dict(self):
        # Reads from the preprocessed test file and populates the testDict variable
        with open('./testPreprocessed.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        continue
                    try:
                        self.testDict[token] += 1
                    except KeyError:
                        self.testDict[token] = 1

    def percentages_not_found(self):
        # What percentage of tokens and word types did not occur in the training data
        num_of_tokens_not_found = 0
        total_tokens = 0
        total_types = 0
        num_of_types_not_found = 0
        for token in self.testDict:
            if token == '<s>':
                continue
            total_tokens += self.testDict[token]
            total_types += 1
            if token in self.unigramDict:
                continue
            num_of_tokens_not_found += self.testDict[token]
            num_of_types_not_found += 1
        return [num_of_tokens_not_found/total_tokens, num_of_types_not_found/total_types]

    def train_bigrams(self):
        # Training bigram
        with open('./trainUnk.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                # For all tokens starting after <s>
                for i in range(1, len(tokens)):
                    s = tokens[i-1] + " " + tokens[i]
                    try:
                        self.bigram_training[s] += 1
                    except KeyError:
                        self.bigram_training[s] = 1
        # Testing bigram
        with open('./testUnk.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                # For all tokens starting after <s>
                for i in range(1, len(tokens)):
                    s = tokens[i-1] + " " + tokens[i]
                    try:
                        self.bigram_test[s] += 1
                    except KeyError:
                        self.bigram_test[s] = 1

    def bigrams_not_found(self):
        # What percentage of bigram tokens and bigram types did not occur in the training data
        num_of_tokens_not_found = 0
        total_tokens = 0
        total_types = 0
        num_of_types_not_found = 0
        for bigram in self.bigram_test:
            total_tokens += self.bigram_test[bigram]
            total_types += 1
            if bigram in self.bigram_training:
                continue
            num_of_tokens_not_found += self.bigram_test[bigram]
            num_of_types_not_found += 1
        return [num_of_tokens_not_found/total_tokens, num_of_types_not_found/total_types]

    def log_probability_unigram(self):
        # P(i) = c(i)/c(total)
        # I look forward to hearing your reply
        p_i = math.log(self.unigramWithUnk['i'] / self.num_of_tokens, 2)
        p_look = math.log(
            self.unigramWithUnk['look'] / self.num_of_tokens, 2)
        p_forward = math.log(
            self.unigramWithUnk['forward'] / self.num_of_tokens, 2)
        p_to = math.log(
            self.unigramWithUnk['to'] / self.num_of_tokens, 2)
        p_hearing = math.log(
            self.unigramWithUnk['hearing'] / self.num_of_tokens, 2)
        p_your = math.log(
            self.unigramWithUnk['your'] / self.num_of_tokens, 2)
        p_reply = math.log(
            self.unigramWithUnk['reply'] / self.num_of_tokens, 2)
        p_dot = math.log(
            self.unigramWithUnk['.'] / self.num_of_tokens, 2)
        p_stop = math.log(
            self.unigramWithUnk['</s>'] / self.num_of_tokens, 2)
        print("Log p(i)", p_i)
        print("Log p(look)", p_look)
        print("Log p(forward)", p_forward)
        print("Log p(to)", p_to)
        print("Log p(hearing)", p_hearing)
        print("Log p(your)", p_your)
        print("Log p(reply)", p_reply)
        print("Log p(.)", p_dot)
        print("Log p(</s>)", p_stop)


if __name__ == "__main__":
    l = LanguageModel()
