class NewString(str):
    """
    New string class that inherits all attributes and methods of the object str
    """

    def multireplace(self, replacement_sumbols, new_sumbols=''):
        """
        Method for replacing specified characters in a string with new characters.
        Single replacement and new characters are objects that are
        single words, parts of words, letters, special characters,
        or combinations thereof, enclosed in string literals.

        There are three ways to specify replacement and new characters:
        1)  Replaced and new characters are grouped into lists or tuples of the same length.
            In this case, each character being replaced is changed to
            a new character located in the same place (having the same index).

        2)  One replacement character and one new character specified.

        3)  One new character and multiple replacement characters are specified,
            grouped into a list or tuple.
            In this case, each character being replaced is changed to the same new character.

        When setting parameters in other ways than the above three, an valueError exception is thrown.
        All values contained in the replacement_sumbols and new_sumbols will be converted to strings.

        :param replacement_sumbols: str, list, tuple,
        :param new_sumbols: str, list, tuple
        :return: str
        """

        # verification stage
        if isinstance(replacement_sumbols, (list, tuple)):
            if isinstance(new_sumbols, (list, tuple)):
                if len(replacement_sumbols) != len(new_sumbols):
                    raise ValueError('different number of elements replacement_sumbols and new_sumbols')
            elif not isinstance(new_sumbols, str):
                raise ValueError('wrong type new_sumbols')
        elif isinstance(replacement_sumbols, str):
            if not isinstance(new_sumbols, str):
                raise ValueError('wrong type new_sumbols')
        else:
            raise ValueError('wrong type replacement_sumbols')

        # replacement stage
        index = 0
        if isinstance(replacement_sumbols, (list, tuple)):
            replacement_sumbols = [str(i) for i in replacement_sumbols]
            while index < len(self):
                letter = self[index]
                for position, sumbol in enumerate(replacement_sumbols):
                    if letter == sumbol[0]:
                        if self[index:index + len(sumbol)] == sumbol:
                            if isinstance(new_sumbols, str):
                                new_sumbol = new_sumbols
                            else:
                                new_sumbol = str(new_sumbols[position])
                            self = self[:index] + new_sumbol + self[index + len(sumbol):]
                            index += len(new_sumbol) - 1
                            break
                index += 1
        else:
            while index < len(self):
                letter = self[index]
                if letter != replacement_sumbols[0]:
                    index += 1
                    continue
                if self[index: index + len(replacement_sumbols)] == replacement_sumbols:
                    self = self[:index] + new_sumbols + self[index + len(replacement_sumbols):]
                    index += len(new_sumbols)
                    continue
                index += 1
        return self