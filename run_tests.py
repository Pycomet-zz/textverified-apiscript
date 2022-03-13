import unittest
from utils import TextVerifiedApi, TelegramApi

print("Running Tests")

class TestTextVerifiedApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.account = TextVerifiedApi()
        cls.account.authentication()


    def clean_up(self):
        "Reports Existing Verifications"
        verification = self.account.fetch_verifications()
        self.account.close_verification(verification['id'])
    
    def test_authentication(self):
        "Fetch And Returns The Access Token"
        # funciton to get_auth
        result = self.account.authentication()
        self.assertIsInstance(result, str)
    

    def test_fetch_number_success(self):
        "Ge New Number From Text Verified"
        self.clean_up()
        result = self.account.fetch_number()
        self.assertIsInstance(result['id'], str)
        self.assertEqual(result['target_name'], "Telegram")
        self.assertEqual(result['status'], "Pending")



    def test_fetch_number_fail(self):
        result = self.account.fetch_number()
        self.assertEqual(result, False)



class TestTelegramApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.api = TelegramApi()
        cls.api.start

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.stop

    def test_create_account(self):
        result = self.api.create_account("TestingNewBie")
        print(result)
        self.assertEqual(result['session'], str)

if __name__ == '__main__':
    unittest.main()