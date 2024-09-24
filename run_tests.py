import unittest

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)