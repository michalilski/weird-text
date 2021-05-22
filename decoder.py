import re
from typing import Union

from settings import SEPARATOR


class Decoder:
    """Decorder class
    Prepared for decoding text encoded by WeirdText encoder.
    """

    def decode(self, encoded_text: str) -> str:
        """Method decoding encoded text by WeirdText encoder.
        Args:
            encoded_text: Text to decoded.
        Returns:
            Decoded string.
        """
        text, words_list = self._preprocess_raw_text(encoded_text)
        # regex for finding words longer than 4 - only this words could be encoded
        words_regex = re.compile(r"[\w+]{4,}", re.U)

        # iterating through all encoded words to replace them with decoded ones
        for word in words_regex.finditer(text):
            start, end = word.span()
            current_encoded = text[start:end]

            # finding matching word from list to replace encoded one
            for i in range(len(words_list)):
                current_word = words_list[i]

                # checking if current word is permutation of encoded one - if yes this should be replaced
                # first checking length, first and last character before sorting shuffled part
                if (
                    len(current_word) == end - start
                    and current_encoded[0] == current_word[0]
                    and current_encoded[-1] == current_word[-1]
                    and sorted(current_encoded[1:-1]) == sorted(current_word[1:-1])
                ):

                    # replacing encoded word in text with original one
                    text = text[:start] + current_word + text[end:]
                    # removing word from list as it is no more needed
                    del words_list[i]
                    break

        return text

    def _preprocess_raw_text(self, text: str) -> Union[str, list]:
        """Method preprocessing raw text passed to decoder.

        First text will be validated by checking number of separators
        and position of first one found. Than raw text will be split
        into encoded sentence (only) and list of original words.
        Args:
            text: Raw text to preprocess.
        Returns:
            Encoded sentence (only) and list of original words.
        """
        found_separators = re.finditer(SEPARATOR, text)

        separator_list = [x for x in found_separators]

        if len(separator_list) != 2:
            raise Exception("Encoded text does not have two separators.")

        if separator_list[0].span()[0] != 0:
            raise Exception("Encoded text does not begin with proper separator.")

        return text[separator_list[0].span()[1] : separator_list[1].span()[0]], text[
            separator_list[1].span()[1] :
        ].split(" ")
