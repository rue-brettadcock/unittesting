import fudge
import unittest

class Foo():

    def foo_func(self, num):
        res = lambda l: 'foo' * l
        if num < 0: num = num*(-1)
        return res(num)


class Bar():

    def bar_func(self, num):
        if num >= 0:
            return 'bar'
        else:
            return 'rab'


class FooBar():

    def __init__(self, f, b):
        self.f = f
        self.b = b

    def do(self, num):
        if num < -5:
            raise NumTooSmall("Enter number greater than -5")
        elif num % 2 == 0:
            res = self.f.foo_func(num)
        elif num % 3 == 0:
            res = self.b.bar_func(num)
        else:
            res = self.f.foo_func(num) + self.b.bar_func(num)
        
        return res


class FooBarErrors(Exception):
    """You made a FooBar Error"""
    pass


class NumTooSmall(FooBarErrors):
    """Number entered was too small"""
    def __init__(self, msg):
        super(NumTooSmall, self).__init__("Number entered is too small :: " + msg)
    pass


class TestSuite(unittest.TestCase):

    @fudge.test
    def test_foo_func_positives(self):
        #Arrange
        expected = ['', 'foo', 'foofoo', 'foofoofoo']
        f = Foo()
        
        #Act
        actual = []
        for i in range(4):
            actual.append(f.foo_func(i))

        #Assert
        self.assertEqual(expected, actual, msg='%s != %s' % (expected, actual))
    
    @fudge.test
    def test_foo_func_negatives(self):
        #Arrange
        expected = ['', 'foo', 'foofoo', 'foofoofoo']
        f = Foo()
        
        #Act
        actual = []
        for i in range(0, -4, -1):
            actual.append(f.foo_func(i))

        #Assert
        self.assertEqual(expected, actual, msg='%s != %s' % (expected, actual))

    @fudge.test
    def test_bar_func_positives(self):
        #Arrage
        expected = 'bar'
        b = Bar()

        #Act and Assert
        for i in range(10):
            actual = b.bar_func(i)
            self.assertEqual(expected, actual, msg='%s != %s' % (expected, actual))

    @fudge.test
    def test_bar_func_negatives(self):
        #Arrage
        expected = 'rab'
        b = Bar()

        #Act and Assert
        for i in range(-1, -10, -1):
            actual = b.bar_func(i)
            self.assertEqual(expected, actual, msg='%s != %s' % (expected, actual))

    @fudge.test
    def test_do_positive_even_input(self):
        #Arrange
        expected = 'foofoo'
        fakeFoo = fudge.Fake('Foo').provides('foo_func').with_args(2).returns('foofoo')
        fakeBar = fudge.Fake('Bar')
        fb = FooBar(fakeFoo, fakeBar)

        #Act
        actual = fb.do(2)

        #Assert
        self.assertEqual(expected, actual, msg='%s != %s' % (expected, actual))

    @fudge.test
    def test_do_negative_noneven_mod3(self):
        #Arrange
        expected = 'rab'
        fakeFoo = fudge.Fake('Foo')
        fakeBar = fudge.Fake('Bar').provides('bar_func').returns('rab')
        fb = FooBar(fakeFoo, fakeBar)

        #Act
        actual = fb.do(-3)

        #Assert 
        self.assertEqual(expected, actual, msg='%s != %s' % (expected, actual))

    @fudge.test
    def test_do_positive_lambda_foo_bar(self):
        #Arrange
        expected = "foofoofoofoofoobar"
        fakeFoo = fudge.Fake('Foo').provides('foo_func').returns('foofoofoofoofoo')
        fakeBar = fudge.Fake('Bar').provides('bar_func').returns('bar')
        fb = FooBar(fakeFoo, fakeBar)

        #Act
        actual = fb.do(5)
        
        #Assert
        self.assertEqual(expected, actual, msg='%s != %s' % (expected, actual))
        
    @fudge.test
    def test_do_check_exception_edge_case(self):

        #Arrange
        fakeFoo = fudge.Fake('Foo').is_a_stub()
        fakeBar = fudge.Fake('Bar').is_a_stub()
        fb = FooBar(fakeFoo, fakeBar)
        
        #Act & Assert
        self.assertRaises(NumTooSmall, fb.do, -6)     

    @fudge.test
    def test_do_check_exception_neg_10_to_100(self):

        #Arrange
        fakeFoo = fudge.Fake('Foo').is_a_stub()
        fakeBar = fudge.Fake('Bar').is_a_stub()
        fb = FooBar(fakeFoo, fakeBar)
        
        #Act & Assert
        for num in range(-10, -100, -1):
            self.assertRaises(NumTooSmall, fb.do, num)

#if __name__ == '__main__':
#    unittest.main()


suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
unittest.TextTestRunner(verbosity=4).run(suite)






















