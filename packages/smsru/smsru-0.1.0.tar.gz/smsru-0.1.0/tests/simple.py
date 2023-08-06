try:
    import unittest2 as unittest  # For Python<=2.6
except ImportError:
    import unittest
import smsru
'''
import os
'''


class SimpleTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_wrong_data(self):
        api = smsru.SmsClient('00000000-0000-0000-0000-000000000000',
                              '70000000000', '000000')
        with self.assertRaises(smsru.SmsruError):
            api.limit()
        with self.assertRaises(smsru.SmsruError):
            api.send('79834206359', u'tessms', test=True)
        with self.assertRaises(smsru.SmsruError):
            api.send('79834206359', u'tessms')
        with self.assertRaises(smsru.SmsruError):
            api.balance()
        self.assertEqual(len(api.token()), 32)

        with self.assertRaises(smsru.SmsruError):
            api.cost('79243965212', u'test sms')
        with self.assertRaises(smsru.SmsruError):
            api.status('000000-0000000')
'''
    def test_right_data(self):
        sms_api = os.environ.get('SMS_API_ID')
        sms_login = os.environ.get('SMS_LOGIN')
        sms_password = os.environ.get('SMS_PASSWORD')
        api = smsru.SmsClient(sms_api, sms_login, sms_password)
        api.limit()
        api.send('79834206359', u'tessms', test=True)
        status = api.send('79834206359', u'tessms')
        api.balance()
        api.cost('79243965212', u'test sms')
        api.status(status)
'''
