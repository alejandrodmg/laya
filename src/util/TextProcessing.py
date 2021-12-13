import re

def read_data(file_path: str):
    """ Load, transform and store the
    intent dataset. """

    data = []
    temp = open(file_path, 'r', encoding="utf8", errors='ignore')
    lines = temp.readlines()
    temp.close()
    # For each line of the file:
    for l in lines:
        try:
            # Store it as a list of lists:
            # [ [sentence], [label] ].
            sentence = l.splitlines()[0]
            data.append([sentence[:-2], sentence[-1:]])
        except:
                pass
    return data

def X_y_split(data: list):
    """ Split data in X and y for ML models. """
    X = [row[0] for row in data]
    y = [row[1] for row in data]
    return X, y

def basic_tokenizer(line: str, normalize_digits=True):
    """ Basic tokenizer for raw text. """

    WORD_SPLIT = re.compile("([.,!?\"'-<>:;)(])")
    DIGIT_RE = re.compile(r"\d")

    # Clean sentence.
    line = re.sub('<u>', '', line)
    line = re.sub('</u>', '', line)
    line = re.sub('\[', '', line)
    line = re.sub('\]', '', line)

    words = []
    # For each word:
    for fragment in line.strip().lower().split():
        # For each token:
        for token in re.split(WORD_SPLIT, fragment):
            # If it an empty list - not token:
            if not token:
                continue
            # If normalize digits:
            if normalize_digits:
                # Replace digits by token #.
                token = re.sub(DIGIT_RE, '#', token)
            # Store token.
            words.append(token)
    return words

def data_cleaner(data: list, return_tokens=False):
        """ Remove punctiation marks and optionally return
        tokenize data. """

        PUNCT = re.compile("([.,!?\"'-<>:;)(])")
        output = []

        for row in data:
            # Remove punctuation marks.
            line = PUNCT.sub('', row)
            # create tokens.
            tokens = basic_tokenizer(line)
            # Store tokens.
            output.append(tokens)
            # Return tokens or entire sentence.
        if return_tokens:
            pass
        else:
            # Rebuild the sentence.
            output = [' '.join(s) for s in output]
        return output
