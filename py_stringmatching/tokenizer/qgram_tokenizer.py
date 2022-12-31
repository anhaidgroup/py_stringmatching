from py_stringmatching import utils
from py_stringmatching.tokenizer.definition_tokenizer import DefinitionTokenizer


class QgramTokenizer(DefinitionTokenizer):
    """Returns tokens that are sequences of q consecutive characters.
    
    A qgram of an input string s is a substring t (of s) which is a sequence of q consecutive characters. Qgrams are also known as
    ngrams or kgrams. 

    Args:
        qval (int): A value for q, that is, the qgram's length (defaults to 2).
        return_set (boolean): A flag to indicate whether to return a set of
                              tokens or a bag of tokens (defaults to False).
        padding (boolean): A flag to indicate whether a prefix and a suffix should be added
                           to the input string (defaults to True).
        prefix_pad (str): A character (that is, a string of length 1 in Python) that should be replicated 
                          (qval-1) times and prepended to the input string, if padding was 
                          set to True (defaults to '#').
        suffix_pad (str): A character (that is, a string of length 1 in Python) that should be replicated 
                          (qval-1) times and appended to the input string, if padding was 
                          set to True (defaults to '$').

    Attributes:
        qval (int): An attribute to store the q value.
        return_set (boolean): An attribute to store the flag return_set.
        padding (boolean): An attribute to store the padding flag.
        prefix_pad (str): An attribute to store the prefix string that should be used for padding.
        suffix_pad (str): An attribute to store the suffix string that should
                          be used for padding.
    """

    def __init__(self, qval=2,
                 padding=True, prefix_pad='#', suffix_pad='$',
                 return_set=False):
        if qval < 1:
            raise AssertionError("qval cannot be less than 1")
        self.qval = qval

        if not type(padding) == type(True):
            raise AssertionError('padding is expected to be boolean type')
        self.padding = padding

        if not isinstance(prefix_pad, str):
            raise AssertionError('prefix_pad is expected to be of type string')
        if not isinstance(suffix_pad, str):
            raise AssertionError('suffix_pad is expected to be of type string')
        if not len(prefix_pad) == 1:
            raise AssertionError("prefix_pad should have length equal to 1")
        if not len(suffix_pad) == 1:
            raise AssertionError("suffix_pad should have length equal to 1")

        self.prefix_pad = prefix_pad
        self.suffix_pad = suffix_pad

        super(QgramTokenizer, self).__init__(return_set)

    def tokenize(self, input_string):
        """Tokenizes input string into qgrams.

        Args:
            input_string (str): The string to be tokenized. 

        Returns:
            A Python list, which is a set or a bag of qgrams, depending on whether return_set flag is True or False. 

        Raises:
            TypeError : If the input is not a string

        Examples:
            >>> qg2_tok = QgramTokenizer()
            >>> qg2_tok.tokenize('database')
            ['#d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e$']
            >>> qg2_tok.tokenize('a')
            ['#a', 'a$']
            >>> qg3_tok = QgramTokenizer(qval=3)
            >>> qg3_tok.tokenize('database')
            ['##d', '#da', 'dat', 'ata', 'tab', 'aba', 'bas', 'ase', 'se$', 'e$$']
            >>> qg3_nopad = QgramTokenizer(padding=False)
            >>> qg3_nopad.tokenize('database')
            ['da', 'at', 'ta', 'ab', 'ba', 'as', 'se']
            >>> qg3_diffpads = QgramTokenizer(prefix_pad='^', suffix_pad='!')
            >>> qg3_diffpads.tokenize('database')
            ['^d', 'da', 'at', 'ta', 'ab', 'ba', 'as', 'se', 'e!']
                      
        """
        utils.tok_check_for_none(input_string)
        utils.tok_check_for_string_input(input_string)

        qgram_list = []

        # If the padding flag is set to true, add q-1 "prefix_pad" characters
        # in front of the input string and  add q-1 "suffix_pad" characters at
        # the end of the input string.
        if self.padding:
            input_string = (self.prefix_pad * (self.qval - 1)) + input_string \
                           + (self.suffix_pad * (self.qval - 1))

        if len(input_string) < self.qval:
            return qgram_list

        qgram_list = [input_string[i:i + self.qval] for i in
                      range(len(input_string) - (self.qval - 1))]
        qgram_list = list(filter(None, qgram_list))

        if self.return_set:
            return utils.convert_bag_to_set(qgram_list)

        return qgram_list

    def get_qval(self):
        """Gets the value of the qval attribute, which is the length of qgrams. 

        Returns:
            The value of the qval attribute. 
        """
        return self.qval

    def set_qval(self, qval):
        """Sets the value of the qval attribute. 

        Args:
            qval (int): A value for q (the length of qgrams). 

        Raises:
            AssertionError : If qval is less than 1.
        """
        if qval < 1:
            raise AssertionError("qval cannot be less than 1")
        self.qval = qval
        return True

    def get_padding(self):
        """
        Gets the value of the padding flag. This flag determines whether the
        padding should be done for the input strings or not.

        Returns:
            The Boolean value of the padding flag.

        """
        return self.padding

    def set_padding(self, padding):
        """
        Sets the value of the padding flag.

        Args:
            padding (boolean): Flag to indicate whether padding should be
                done or not.

        Returns:
            The Boolean value of True is returned if the update was
            successful.

        Raises:
            AssertionError: If the padding is not of type boolean

        """
        if not type(padding) == type(True):
            raise AssertionError('padding is expected to be boolean type')
        self.padding = padding
        return True

    def get_prefix_pad(self):
        """
        Gets the value of the prefix pad.


        Returns:
            The prefix pad string.

        """
        return self.prefix_pad

    def set_prefix_pad(self, prefix_pad):
        """
        Sets the value of the prefix pad string.

        Args:
            prefix_pad (str): String that should be prepended to the
                input string before tokenization.

        Returns:
            The Boolean value of True is returned if the update was
            successful.

        Raises:
            AssertionError: If the prefix_pad is not of type string.
            AssertionError: If the length of prefix_pad is not one.

        """
        if not isinstance(prefix_pad, str):
            raise AssertionError('prefix_pad is expected to be of type string')
        if not len(prefix_pad) == 1:
            raise AssertionError("prefix_pad should have length equal to 1")
        self.prefix_pad = prefix_pad
        return True

    def get_suffix_pad(self):
        """
        Gets the value of the suffix pad.


        Returns:
            The suffix pad string.

        """
        return self.suffix_pad

    def set_suffix_pad(self, suffix_pad):
        """
        Sets the value of the suffix pad string.

        Args:
            suffix_pad (str): String that should be appended to the
                input string before tokenization.

        Returns:
            The boolean value of True is returned if the update was
            successful.

        Raises:
            AssertionError: If the suffix_pad is not of type string.
            AssertionError: If the length of suffix_pad is not one.

        """
        if not isinstance(suffix_pad, str):
            raise AssertionError('suffix_pad is expected to be of type string')
        if not len(suffix_pad) == 1:
            raise AssertionError("suffix_pad should have length equal to 1")
        self.suffix_pad = suffix_pad
        return True
