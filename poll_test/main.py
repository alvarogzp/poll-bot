import unittest
from unittest import TextTestRunner

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("poll_test", pattern="*")
    TextTestRunner().run(suite)
