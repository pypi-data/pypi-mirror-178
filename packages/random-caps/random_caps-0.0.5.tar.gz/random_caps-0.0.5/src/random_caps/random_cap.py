import random


def random_cap(string: str | list, chance: int) -> str | list:
    """
    Randomly applies uppercase to letters in a string.

        Parameters:
            string (str | list): the string to apply to.
            chance (int): the chance of applying uppercase to a letter.

        Returns:
            The string or a list of strings with random uppercase and lowercase letters.

        Example:
            random_cap("random", 100) > each letter has a 1 in a 100 chance of turning uppercase

        Raises:
            TypeError: either a element in a list is not a string or
            the argument "string" is not a string.
    """

    if type(string) == int:
        raise TypeError

    if type(string) == str:
        result = []
        for l in string:
            rand = random.randint(0, chance)
            if rand == 1:
                result.append(l.capitalize())
            else:
                result.append(l)

        return "".join(result)

    elif type(string) == list:
        strings = []
        for s in string:
            result = []
            if type(s) == int:
                raise TypeError
            for l in s:

                rand = random.randint(0, chance)
                if rand == 1:
                    result.append(l.capitalize())
                else:
                    result.append(l)
            strings.append(result)

        return strings

    else:
        raise TypeError
