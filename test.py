import random

from decoder import Decoder
from encoder import Encoder
from settings import (
    MAX_RANDOM_SENTENCE_LEN,
    MAX_RANDOM_WORD_LEN,
    PREPARED_SENTECES,
    RANDOM_ALPHABET,
)


def generate_random_sentence(
    max_word_len: int, max_sentence_len: int, alphabet: str
) -> str:
    """Method generating random sentence.
    Args:
        max_word_len: Max length of word in sentence.
        max_sentence_len: Max number of words in sentence.
        alphabet: Alphabet to get letters from.
    Returns:
        Generated sentence.
    """
    words = []
    for _ in range(random.randint(0, max_sentence_len)):
        words.append(
            "".join(
                [
                    random.choice(alphabet)
                    for _ in range(random.randint(0, max_word_len))
                ]
            )
        )
    return " ".join(words)


def test_sentences(encoder: Encoder, decoder: Decoder, sentences_list: list):
    """Method testing given encoder and decoder.
    Args:
        encoder: Tested encoder.
        decoder: Tested decoder.
        sentences_list: List of sentences prepared to test encoder and decoder.
    """
    passed = 0
    for i, sentence in enumerate(sentences_list):
        encoded = encoder.encode(sentence)
        decoded = decoder.decode(encoded)
        # Warning! Decoding error might be caused when
        # there are multiple orignal words matching encoded one
        if sentence != decoded:
            print(f"Found error in test {i+1}!")
            print(f"ORIGINAL: {sentence}")
            print(f"DECODED:  {decoded}")
        else:
            passed += 1
    print(f"Test finished: {passed}/{len(sentences_list)} passed.")


def show_example_test(encoder: Encoder, decoder: Decoder, sentence: str):
    """Method presenting test flow.
    Args:
        encoder: Tested encoder.
        decoder: Tested decoder.
        sentence: Sentence prepared to test encoder and decoder.
    """
    print("\nExample sentence:")
    print(sentence)

    encoded = encoder.encode(sentence)
    print("\nEncoded:")
    print(encoded)

    decoded = decoder.decode(encoded)
    print("\nDecoded:")
    print(decoded)

    print(f"\nSentence properly decoded: {sentence==decoded}")


def main():
    # number of random generated sentences
    tested_random = 100
    enc = Encoder()
    dec = Decoder()

    show_example_test(
        enc, dec, "This is a long looong test sentence,\nwith some big (biiiiig) words!"
    )

    print("\nTesting prepared sentences: ")
    test_sentences(enc, dec, PREPARED_SENTECES)

    random_sentences = [
        generate_random_sentence(
            MAX_RANDOM_WORD_LEN, MAX_RANDOM_SENTENCE_LEN, RANDOM_ALPHABET
        )
        for _ in range(tested_random)
    ]
    print("\nTesting random sentences: ")
    test_sentences(enc, dec, random_sentences)


if __name__ == "__main__":
    main()
