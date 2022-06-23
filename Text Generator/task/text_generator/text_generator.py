import random
import re
import sys
from nltk.tokenize import WhitespaceTokenizer
from collections import Counter


def check_input(list, head):
    print(f"token_list: {list}")
    if head == "exit":
        sys.exit()
    while True:
        if head not in list:
            print("Key Error. The requested word is not in the model. Please input another word.")
            head = input()
        else:
            break


def create_trigram(list):
    trigram_list = []
    for index in range(len(list)):
        if index < len(list) - 2:
            head = ' '.join((list[index], list[index + 1]))
            tail = list[index + 2]
            trigram_list.append((head, tail))
        else:
            pass
    return trigram_list


def choose_head(trigram_list):
    random_tuple = random.choices(trigram_list)[0]
    first_head_word, second_head_word = random_tuple[0].split(' ')
    while not re.match(r'^[A-Z].*[^.?!]$', first_head_word):
        random_tuple = random.choices(trigram_list)[0]
        first_head_word, second_head_word = random_tuple[0].split(' ')
    head = random_tuple[0]
    return head


def print_token(trigram_list, min_token_amount):
    sentenced_printed = False
    while not sentenced_printed:
        sentence_list = []
        head = choose_head(trigram_list)
        first_head_word, second_head_word = head.split(' ')
        sentence_list.append(first_head_word)
        sentence_list.append(second_head_word)
        is_stop = False
        while not is_stop:
            tail_list = []
            # has_match = False
            for (head_, tail_) in trigram_list:
                if head_ == head:
                    tail_list.append(tail_)
            freq_counter = Counter(tail_list)
            most_common_freq_counter = freq_counter.most_common()
            population = [x[0] for x in most_common_freq_counter]
            weights = [x[1] for x in most_common_freq_counter]
            if len(population) < 1:
                break
            random_word = random.choices(population=population, weights=weights)[0]
            if len(sentence_list) < min_token_amount:
                if re.match(r'^[A-Za-z].*[.?!]$', random_word):
                    random_word = random.choices(population=population, weights=weights)[0]
            tail = random_word
            sentence_list.append(tail)
            head = sentence_list[-2] + " " + sentence_list[-1]
            if len(sentence_list) >= min_token_amount:
                if re.match(r'^[A-Za-z].*[.?!]$', tail):
                    print(' '.join(sentence_list))
                    is_stop = True
                    sentenced_printed = True


def main():
    filename = str(input())
    with open(filename, "r", encoding="utf-8") as file:
        MIN_TOKEN_AMOUNT = 5
        SENTENCE_AMOUNT = 10
        text = file.read()
        word_tokenize_list = WhitespaceTokenizer().tokenize(text)
        trigram_list = create_trigram(word_tokenize_list)
        for _ in range(SENTENCE_AMOUNT):
            print_token(trigram_list, MIN_TOKEN_AMOUNT)


if __name__ == '__main__':
    main()
