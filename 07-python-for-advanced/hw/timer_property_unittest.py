import unittest
import time
from timer_property import Message


class TestMessage(unittest.TestCase):
    def test_get_msg_performance(self):  #Verifies correct operation of the applied property
        m = Message()
        test_var = m.msg
        self.assertEqual(test_var, m.msg)

    def test_set_msg_performance(self):  #Verifies correct operation of the applied property
        m = Message()
        m.msg = 'I am not a random string!'
        test_var = m.msg
        self.assertEqual(test_var, m.msg)

    def test_timed_storage_performance_set(self):  #Verifies correct operation of timed data storage, time > t, user message
        m = Message()
        m.msg = 'I am not a random string!'
        test_var = m.msg
        time.sleep(11)
        self.assertNotEqual(test_var, m.msg)

    def test_timed_storage_performance_long(self):  #Verifies correct operation of timed data storage, time > t, random message
        m = Message()
        test_var = m.msg
        time.sleep(11)
        self.assertNotEqual(test_var, m.msg)

    def test_timed_storage_performance_short(self):  #Verifies correct operation of timed data storage, time < t, random message
        m = Message()
        test_var = m.msg
        time.sleep(5)
        self.assertEqual(test_var, m.msg)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=3)
