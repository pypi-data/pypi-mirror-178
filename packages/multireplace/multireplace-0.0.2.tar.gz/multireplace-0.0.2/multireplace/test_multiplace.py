import unittest

from multireplace import NewString


class TestStrMetod(unittest.TestCase):

    def test_errors(self):
        new_str = NewString('qwerty')
        init_params = [
            ((i for i in range(3)), ''),            # generator and str
            (print, ''),                            # function and str
            ('', print),                            # str and function
            ('', (i for i in range(3))),            # str and generator
            (['q', 'w', 'e'], ('a', 'b')),          # different number
            ('', {'q'}),                            # wrong type new_sumbols
        ]
        for param in init_params:
            self.assertRaises(ValueError, new_str.multireplace, *param)

    def test_functionality(self):
        new_str = NewString('qwerty 351')
        init_params = [
            (['w', 'r'], ''),
            ('ert', ''),
            (['q', 'ty'], ('b', 'q')),
            (('1', 'y'), ['2', 'q']),
            ([3, 2, 5], (10, 11, 12))
        ]

        results = [
            'qety 351',
            'qwy 351',
            'bwerq 351',
            'qwertq 352',
            'qwerty 10121'
        ]

        for sumbols, result in zip(init_params, results):
            replacement_sumbols, new_sumbols = sumbols
            self.assertEqual(
                new_str.multireplace(replacement_sumbols=replacement_sumbols, new_sumbols=new_sumbols),
                result
            )

    def test_working_string_metods(self):
        new_str = NewString('qwerty')

        self.assertEqual(new_str.replace('q', ''), 'werty')
        self.assertEqual(new_str.split('e'), ['qw', 'rty'])
        self.assertEqual(new_str[2], 'e')
        self.assertEqual(new_str[1:3], 'we')
        self.assertEqual(new_str.upper(), 'QWERTY')
        self.assertEqual(new_str.title(), 'Qwerty')
        self.assertEqual(new_str.endswith('ty'), True)
        self.assertEqual(new_str.startswith('qu'), False)



