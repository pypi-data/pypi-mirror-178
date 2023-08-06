# multireplace
### Method for multi replace in strings


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

____

### Installation

For installation:

`pip install multireplace`

____

### Sample using

1) To use, you need to create object `NewString`.
2) For the received object, use the method `multireplace`.
The method returns a new string, but does not edit the original string.
To save a new string, you must assign the result of the method execution to a variable.
3) After multiple replace, you can use all original methods for string.

```Python

from multireplace import multireplace

same_str = multireplace.NewString("I'll be back").multireplace(replacement_sumbols=['I', "'", 'll', 'k'],
                                                  new_sumbols=['We', ' ', 'will', 'k!'])
```

You can also use the method `multireplace` to remove multiple characters from a string. 
To do this, specify the characters to be removed in the parameter `replacement_sumbols`

```Python

from multireplace import multireplace

same_str = multireplace.NewString("I'll be back").multireplace(replacement_sumbols=[' ', 'be', 'back'])
```
