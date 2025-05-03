def create_tokenizer():
    tokenizer = {}

    for i in range(26):
        char = chr(ord('a') + i)
        tokenizer[char] = i

    for i in range(26):
        char = chr(ord('A') + i)
        tokenizer[char] = i + 27

    return tokenizer

def tokenize(text, tokenizer):
    word_tokens = []
    words = text.split(" ")  

    for word in words:
        tokens = []
        for char in word:
            if char in tokenizer:
                tokens.append(tokenizer[char])
            else:
                tokens.append(-1) 
        word_tokens.append(tokens)

    return word_tokens

# Example usage
tokenizer = create_tokenizer()
text = "Hello World"
tokens = tokenize(text, tokenizer)
print(tokens)
