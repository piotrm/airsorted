import unittest
from airsorted_address_book.validators import EmailParamsValidator

class EmailParamsValidatorTestCase(unittest.TestCase):
    def test_incorrect_params_type(self):
        params = 'olaf@abcde.com'
        self.assertFalse(EmailParamsValidator.check(params),\
            'Params should be a list')

    def test_incorrect_email_format(self):
        params = [
            'olaf@abcde.com',
            'osnowmanabcdecom'
        ]
        self.assertFalse(EmailParamsValidator.check(params),\
            'Emails should be properly formatted')

    def test_correct_params(self):
        params = [
            'olaf@abcde.com',
            'osnowman@abcde.com'
        ]

        self.assertTrue(EmailParamsValidator.check(params))

if __name__ == '__main__':
    unittest.main()
