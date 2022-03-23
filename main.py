# Steven Necola
# NLP - Spring 2022

import math


class LanguageModel:

    # Unigram variables
    unigram_dict = {}
    unigram_with_unk = {}
    test_dict = {}
    test_unigram = {}

    # Bigram variables
    bigram_training = {}
    bigram_test = {}

    # Bigram with Add-One smoothing
    bigram_add_one = {}

    # Counters for different training data
    # including <s>
    total_num_of_tokens = 0
    # of <s> since we dont include it in the unigram model
    num_of_start = 0
    # not including <s>
    num_of_tokens = 0
    # num of tokens in training data with <unk> (should be same as num_of_tokens)
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
        # print('# of unique tokens in the training corpus (including </s> and <unk>) ', len(self.unigram_dict)+1)
        # print('# of <s> in unigram_dict ', self.unigram_dict['<s>'])
        print('# of unique tokens in the training corpus (replaced single instance words with <unk>)', len(
            self.unigram_with_unk))
        # print('# of <s> in unigram_with_unk', self.unigram_with_unk['<s>'])

        # Answer to Question 2
        print("Question 2:")
        #num_of_tokens = self.get_num_of_tokens()
        print('# of tokens in the training corpus not including <s>',
              self.num_of_tokens)

        # Preprocessing for test
        self.preprocessing_step1_2_test()
        self.create_test_dict()
        print("Question 3:")
        # print('# of unique tokens in the test corpus (including </s> and <unk>) ', len(self.test_dict)+1)
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

        print("Question 5:\nUnigram:")
        log_sums_unigram, m_unigram = self.log_probability_unigram()
        print("Bigram:")
        self.log_probability_bigram()
        print("Bigram Add-One Smoothing")
        log_sums_bigram_addone, m_bigram_addone = self.log_probability_bigram_add_one()

        print("Question 6:")
        print("Unigram Perplexity=", self.perplexity(
            log_sums_unigram, m_unigram))
        print("Bigram Perplexity= undefined")
        print("Bigram Add-One Smoothing Perplexity=",
              self.perplexity(log_sums_bigram_addone, m_bigram_addone))

        self.create_test_unigram_with_unk()
        print("Question 7:")
        self.test_unigram_perplexity()

    def preprocessing_step1_2(self):
        # Lowercase all words in the training and test corpuses
        # Add <s> and </s> to the sentenses
        with open('train-Spring2022.txt', 'r', encoding='utf8') as f:
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
        with open('trainPreprocessed.txt', 'r', encoding='utf8') as f:
            with open('trainUnk.txt', 'w', encoding='utf8') as w:
                for line in f:
                    tokens = line.split()
                    for token in tokens:
                        if token == '<s>':
                            w.write(token)
                            w.write(' ')
                            continue
                        if self.unigram_dict[token] == 1:
                            token = '<unk>'
                        w.write(token)
                        w.write(' ')
                    w.write('\n')

    def create_unigram(self):
        # Reads from the preprocessed Training file and populates the unigram_dict variable
        with open('trainPreprocessed.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        self.total_num_of_tokens += 1
                        self.num_of_start += 1
                        continue
                    try:
                        self.unigram_dict[token] += 1
                    except KeyError:
                        self.unigram_dict[token] = 1
                    # Two counters, first one without <s> and the second with <s>
                    self.num_of_tokens += 1
                    self.total_num_of_tokens += 1

    def create_unigram_with_unk(self):
        with open('trainUnk.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        continue
                    try:
                        self.unigram_with_unk[token] += 1
                    except KeyError:
                        self.unigram_with_unk[token] = 1
                    self.num_of_tokens_unk += 1

    # def get_num_of_tokens(self):
    #     num_of_tokens = 0
    #     num_of_tokens_unk = 0
    #     for token in self.unigram_dict:
    #         if token == '<s>':
    #             continue
    #         num_of_tokens += self.unigram_dict[token]
    #     for token in self.unigram_with_unk:
    #         if token == '<s>':
    #             continue
    #         num_of_tokens_unk += self.unigram_with_unk[token]
    #     return [num_of_tokens, num_of_tokens_unk]

    def preprocessing_step1_2_test(self):
        # Lowercase all words in the training and test corpuses
        # Add <s> and </s> to the sentenses
        with open('test.txt', 'r', encoding='utf8') as f:
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
        with open('test.txt', 'r', encoding='utf8') as f:
            with open('testUnk.txt', 'w', encoding='utf8') as w:
                for line in f:
                    # Get all the words, set them to lowercase
                    tokens = line.split()
                    w.write('<s> ')
                    for token in tokens:
                        token = token.lower()
                        if token in self.unigram_with_unk:
                            w.write(token)
                            w.write(' ')
                        else:
                            w.write('<unk> ')
                    w.write('</s>\n')

    def create_test_dict(self):
        # Reads from the preprocessed test file and populates the test_dict variable
        with open('testPreprocessed.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        continue
                    try:
                        self.test_dict[token] += 1
                    except KeyError:
                        self.test_dict[token] = 1

    def create_test_unigram_with_unk(self):
        with open('testUnk.txt', 'r', encoding='utf8') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    if (token == '<s>'):
                        continue
                    try:
                        self.test_unigram[token] += 1
                    except KeyError:
                        self.test_unigram[token] = 1

    def percentages_not_found(self):
        # What percentage of tokens and word types did not occur in the training data
        num_of_tokens_not_found = 0
        total_tokens = 0
        total_types = 0
        num_of_types_not_found = 0
        for token in self.test_dict:
            if token == '<s>':
                continue
            total_tokens += self.test_dict[token]
            total_types += 1
            if token in self.unigram_dict:
                continue
            num_of_tokens_not_found += self.test_dict[token]
            num_of_types_not_found += 1
        return [num_of_tokens_not_found/total_tokens, num_of_types_not_found/total_types]

    def train_bigrams(self):
        # Training bigram
        with open('trainUnk.txt', 'r', encoding='utf8') as f:
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
        with open('testUnk.txt', 'r', encoding='utf8') as f:
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
        try:
            p_i = math.log(self.unigram_with_unk['i'] / self.num_of_tokens, 2)
        except KeyError:
            p_i = 0
        p_look = math.log(
            self.unigram_with_unk['look'] / self.num_of_tokens, 2)
        p_forward = math.log(
            self.unigram_with_unk['forward'] / self.num_of_tokens, 2)
        p_to = math.log(
            self.unigram_with_unk['to'] / self.num_of_tokens, 2)
        p_hearing = math.log(
            self.unigram_with_unk['hearing'] / self.num_of_tokens, 2)
        p_your = math.log(
            self.unigram_with_unk['your'] / self.num_of_tokens, 2)
        p_reply = math.log(
            self.unigram_with_unk['reply'] / self.num_of_tokens, 2)
        p_dot = math.log(
            self.unigram_with_unk['.'] / self.num_of_tokens, 2)
        p_stop = math.log(
            self.unigram_with_unk['</s>'] / self.num_of_tokens, 2)
        print("Log p(i)", p_i)
        print("Log p(look)", p_look)
        print("Log p(forward)", p_forward)
        print("Log p(to)", p_to)
        print("Log p(hearing)", p_hearing)
        print("Log p(your)", p_your)
        print("Log p(reply)", p_reply)
        print("Log p(.)", p_dot)
        print("Log p(</s>)", p_stop)
        log_sums = p_i+p_look + p_forward+p_to+p_hearing+p_your+p_reply+p_dot+p_stop
        print("The log probability of this unigram is", log_sums)
        return [log_sums, 9]

    def log_probability_bigram(self):
        # I look forward to hearing your reply
        try:
            p_s_i = math.log(
                self.bigram_training['<s> i'] / self.num_of_start, 2)
        except KeyError:
            p_s_i = 0
        try:
            p_i_look = math.log(
                self.bigram_training['i look'] / self.unigram_with_unk['i'], 2)
        except KeyError:
            p_i_look = 0
        try:
            p_look_forward = math.log(
                self.bigram_training['look forward'] / self.unigram_with_unk['look'], 2)
        except KeyError:
            p_look_forward = 0
        try:
            p_forward_to = math.log(
                self.bigram_training['forward to'] / self.unigram_with_unk['forward'], 2)
        except KeyError:
            p_forward_to = 0
        try:
            p_to_hearing = math.log(
                self.bigram_training['to hearing'] / self.unigram_with_unk['to'], 2)
        except KeyError:
            p_to_hearing = 0
        try:
            p_hearing_your = math.log(
                self.bigram_training['hearing your'] / self.unigram_with_unk['hearing'], 2)
        except KeyError:
            p_hearing_your = 0
        try:
            p_your_reply = math.log(
                self.bigram_training['your reply'] / self.unigram_with_unk['your'], 2)
        except KeyError:
            p_your_reply = 0
        try:
            p_reply_dot = math.log(
                self.bigram_training['reply .'] / self.unigram_with_unk['reply'], 2)
        except KeyError:
            p_reply_dot = 0
        try:
            p_dot_stop = math.log(
                self.bigram_training['. </s>'] / self.unigram_with_unk['.'], 2)
        except KeyError:
            p_dot_stop = 0
        print("Log p(i | <s>)", p_s_i)
        print("Log p(look | i)", p_i_look)
        print("Log p(forward | look)", p_look_forward)
        print("Log p(to | forward)", p_forward_to)
        print("Log p(hearing | to)", p_to_hearing)
        print("Log p(your | hearing)", p_hearing_your)
        print("Log p(reply | your)", p_your_reply)
        print("Log p(. | reply)", p_reply_dot)
        print("Log p(</s> | .)", p_dot_stop)
        print("Log probability of this bigram is undefined")

    def log_probability_bigram_add_one(self):
        vocabulary_size = len(self.unigram_with_unk)+1
        try:
            p_s_i = math.log(
                (self.bigram_training['<s> i'] + 1) / (self.num_of_start + vocabulary_size), 2)
        except KeyError:
            p_s_i = 0
        try:
            p_i_look = math.log(
                (self.bigram_training['i look'] + 1) / (self.unigram_with_unk['i'] + vocabulary_size), 2)
        except KeyError:
            p_i_look = math.log(
                (1) / (self.unigram_with_unk['i'] + vocabulary_size), 2)
        try:
            p_look_forward = math.log(
                (self.bigram_training['look forward']+1) / (self.unigram_with_unk['look'] + vocabulary_size), 2)
        except KeyError:
            p_look_forward = 0
        try:
            p_forward_to = math.log(
                (self.bigram_training['forward to']+1) / (self.unigram_with_unk['forward'] + vocabulary_size), 2)
        except KeyError:
            p_forward_to = 0
        try:
            p_to_hearing = math.log(
                (self.bigram_training['to hearing']+1) / (self.unigram_with_unk['to'] + vocabulary_size), 2)
        except KeyError:
            p_to_hearing = 0
        try:
            p_hearing_your = math.log(
                (self.bigram_training['hearing your']+1) / (self.unigram_with_unk['hearing'] + vocabulary_size), 2)
        except KeyError:
            p_hearing_your = math.log(
                (1) / (self.unigram_with_unk['hearing'] + vocabulary_size), 2)
        try:
            p_your_reply = math.log(
                (self.bigram_training['your reply']+1) / (self.unigram_with_unk['your'] + vocabulary_size), 2)
        except KeyError:
            p_your_reply = math.log(
                (1) / (self.unigram_with_unk['your'] + vocabulary_size), 2)
        try:
            p_reply_dot = math.log(
                (self.bigram_training['reply .']+1) / (self.unigram_with_unk['reply'] + vocabulary_size), 2)
        except KeyError:
            p_reply_dot = math.log(
                (1) / (self.unigram_with_unk['reply'] + vocabulary_size), 2)
        try:
            p_dot_stop = math.log(
                (self.bigram_training['. </s>']+1) / (self.unigram_with_unk['.'] + vocabulary_size), 2)
        except KeyError:
            p_dot_stop = math.log(
                (1) / (self.unigram_with_unk['.'] + vocabulary_size), 2)
        print("Log p(i | <s>)", p_s_i)
        print("Log p(look | i)", p_i_look)
        print("Log p(forward | look)", p_look_forward)
        print("Log p(to | forward)", p_forward_to)
        print("Log p(hearing | to)", p_to_hearing)
        print("Log p(your | hearing)", p_hearing_your)
        print("Log p(reply | your)", p_your_reply)
        print("Log p(. | reply)", p_reply_dot)
        print("Log p(</s> | .)", p_dot_stop)
        log_sums = p_s_i+p_i_look+p_look_forward + p_forward_to + \
            p_to_hearing+p_hearing_your+p_your_reply+p_reply_dot+p_dot_stop
        print("Log probability of this bigram is", log_sums)
        return [log_sums, 10]

    def perplexity(self, avg_log, m):
        return math.pow(2, (-1)*(avg_log/m))

    def test_unigram_perplexity(self):
        vocab_size = len(self.test_dict)
        log_sum = 0
        for token in self.test_dict:
            if token == '<s>':
                continue
            p_token = math.log(
                self.unigram_with_unk[token] / self.num_of_tokens, 2)
            log_sum += p_token
        print("Unigram Perplexity =", self.perplexity(log_sum, vocab_size))


if __name__ == "__main__":
    l = LanguageModel()
