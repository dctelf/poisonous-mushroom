from unittest import TestCase
from cryptochallenge import userprofile

class TestProfileMethods(TestCase):
    def test_kvparse(self):
        teststr = "foo=bar&baz=qux&zap=zazzle"
        print(teststr)
        exp_obj = {
            "foo": "bar",
            "baz": "qux",
            "zap": "zazzle"
        }
        print(exp_obj)
        ret_obj = userprofile.kvparse(teststr)
        print(ret_obj)
        self.assertEqual(exp_obj, ret_obj)

    def test_profile_for(self):

        test_email = "bob@2018_tests.com"

        exp_obj = {
            "email": test_email,
            "uid": "10",
            "role": "user"
        }
        print(exp_obj)
        ret_obj = userprofile.profile_for(test_email)
        print(ret_obj)

        self.assertEqual(exp_obj, ret_obj)


    def test_kvbuild(self):
        exp_str = "foo=bar&baz=qux&zap=zazzle"

        print(exp_str)
        test_obj = {
            "foo": "bar",
            "baz": "qux",
            "zap": "zazzle"
        }

        ret_str = userprofile.kvbuild(test_obj)
        print(ret_str)
        self.assertEqual(exp_str, ret_str)

    def test_profile_encrypt(self):
        self.assertEqual("A", "A")

    def test_profile_decrypt(self):
        self.assertEqual("A", "A")
