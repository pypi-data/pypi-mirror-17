import unittest
import os
import random
import string
import array

import heatshrink


BASE_DIR = os.path.dirname(__file__)


def random_string(size):
    """
    Generate a random string of size `size`.
    """
    choices = string.lowercase + string.uppercase + string.digits + '\n'
    return ''.join(random.choice(choices) for _ in range(size))


class EncoderTest(unittest.TestCase):
    def setUp(self):
        self.encoded = heatshrink.encode(b'abcde')

    def test_encoded_size(self):
        self.assertEqual(len(self.encoded), 6)

    def test_encoded_bytes(self):
        self.assertEqual(self.encoded, b'\xb0\xd8\xacvK(')

    def test_encode_with_window_sz2(self):
        encoded = heatshrink.encode(b'abcde', window_sz2=8)
        # FIXME: Prove that this setting changes output
        self.assertEqual(encoded, b'\xb0\xd8\xacvK(')

    def test_encode_checks_window_sz2_type(self):
        with self.assertRaises(TypeError):
            heatshrink.encode(b'abcde', window_sz2='a string')
        with self.assertRaises(TypeError):
            heatshrink.encode(b'abcde', window_sz2=lambda x: None)

    def test_encode_checks_window_sz2_within_limits(self):
        with self.assertRaises(ValueError):
            heatshrink.encode(b'abcde', window_sz2=3)
        with self.assertRaises(ValueError):
            heatshrink.encode(b'abcde', window_sz2=16)
        heatshrink.encode(b'abcde', window_sz2=5)
        heatshrink.encode(b'abcde', window_sz2=14)

    def test_encode_with_lookahead_sz2(self):
        encoded = heatshrink.encode(b'abcde', lookahead_sz2=3)
        self.assertEqual(encoded, b'\xb0\xd8\xacvK(')

    def test_encode_checks_lookahead_sz2_type(self):
        with self.assertRaises(TypeError):
            heatshrink.encode(b'abcde', lookahead_sz2='a string')
        with self.assertRaises(TypeError):
            heatshrink.encode(b'abcde', lookahead_sz2=lambda x: None)

    def test_encode_checks_lookahead_sz2_within_limits(self):
        with self.assertRaises(ValueError):
            heatshrink.encode(b'abcde', lookahead_sz2=1)
        with self.assertRaises(ValueError):
            heatshrink.encode(b'abcde', lookahead_sz2=16)
        heatshrink.encode(b'abcde', lookahead_sz2=4)
        heatshrink.encode(b'abcde', lookahead_sz2=10)

    def test_different_params_yield_different_output(self):
        string = b'A string with stuff in it'
        self.assertNotEqual(heatshrink.encode(string, window_sz2=8),
                            heatshrink.encode(string, window_sz2=11))
        self.assertNotEqual(heatshrink.encode(string, lookahead_sz2=4),
                            heatshrink.encode(string, lookahead_sz2=8))

    def test_valid_encode_types(self):
        heatshrink.encode(b'abcde')
        heatshrink.encode('abcde'.encode('utf8'))
        heatshrink.encode(bytearray([1, 2, 3]))
        heatshrink.encode(array.array('B', [1, 2, 3]))
        heatshrink.encode([1, 2, 3])
        with self.assertRaises(TypeError):
            heatshrink.encode(memoryview(b'abcde'))
        try:
            with self.assertRaises(TypeError):
                heatshrink.encode(unicode('abcde'))
        except NameError:  # Python 3
            pass
        with self.assertRaises(TypeError):
            heatshrink.encode(lambda x: x)
        with self.assertRaises(TypeError):
            heatshrink.encode(True)


class DecoderTest(unittest.TestCase):
    def test_returns_string(self):
        self.assertIsInstance(heatshrink.decode('abcde'), str)

    def test_accepts_buffer_like_objects(self):
        heatshrink.decode('abcde')
        heatshrink.decode(b'abcde')
        heatshrink.decode(bytearray([1, 2, 3]))
        heatshrink.decode(array.array('B', [1, 2, 3]))
        heatshrink.decode([1, 2, 3])
        with self.assertRaisesRegexp(TypeError, "unicode .* array"):
            heatshrink.decode(u'abcde')
        with self.assertRaisesRegexp(TypeError, "memoryview .* array"):
            heatshrink.decode(memoryview(b'abcde'))
        with self.assertRaisesRegexp(TypeError, "'int' .* not iterable"):
            heatshrink.decode(1)
        with self.assertRaisesRegexp(TypeError, "'function' .* not iterable"):
            heatshrink.decode(lambda x: x)
        with self.assertRaisesRegexp(TypeError, "'bool' .* not iterable"):
            heatshrink.decode(True)

    def test_decode_with_window_sz2(self):
        decoded = heatshrink.decode(b'\xb0\xd8\xacvK(', window_sz2=11)
        self.assertEqual(decoded, 'abcde')

    def test_decode_checks_window_sz2_type(self):
        with self.assertRaises(TypeError):
            heatshrink.decode('abcde', window_sz2='a string')
        with self.assertRaises(TypeError):
            heatshrink.decode('abcde', window_sz2=lambda x: None)

    def test_decode_checks_window_sz2_within_limits(self):
        with self.assertRaises(ValueError):
            heatshrink.decode('abcde', window_sz2=3)
        with self.assertRaises(ValueError):
            heatshrink.decode('abcde', window_sz2=16)
        heatshrink.decode('abcde', window_sz2=5)
        heatshrink.decode('abcde', window_sz2=14)

    def test_decode_with_lookahead_sz2(self):
        decoded = heatshrink.decode('\xb0\xd8\xacvK(', lookahead_sz2=3)
        self.assertEqual(decoded, 'abcde')

    def test_decode_checks_lookahead_sz2_type(self):
        with self.assertRaises(TypeError):
            heatshrink.decode('abcde', lookahead_sz2='a string')
        with self.assertRaises(TypeError):
            heatshrink.decode('abcde', lookahead_sz2=lambda x: None)

    def test_decode_checks_lookahead_sz2_within_limits(self):
        with self.assertRaises(ValueError):
            heatshrink.decode('abcde', lookahead_sz2=1)
        with self.assertRaises(ValueError):
            heatshrink.decode('abcde', lookahead_sz2=16)
        heatshrink.decode('abcde', lookahead_sz2=4)
        heatshrink.decode('abcde', lookahead_sz2=10)


class EncoderToDecoderTest(unittest.TestCase):
    """
    Tests assertion that data passed through the encoder
    and then the decoder with the same parameters will be
    equal to the original data.
    """

    def test_encoder_output_to_decoder_input_valid(self):
        encoded = heatshrink.encode(b'a string')
        self.assertEqual(heatshrink.decode(encoded), 'a string')

    def test_with_a_paragraph(self):
        quotes = """I know this from my own experience, as a high school kid writing programs in Basic.
        That language didn't even support recursion. It's hard to imagine writing programs
        without using recursion, but I didn't miss it at the time. I thought in Basic.
        And I was a whiz at it. Master of all I surveyed. - Paul Graham

        A programming language is for thinking about programs, not for expressing programs you've
        already thought of. It should be a pencil, not a pen. - Paul Graham

        A recursive definition does not necessarily lead to a recursive process. - Gerald Jay Sussman
        """
        encoded = heatshrink.encode(quotes)
        self.assertEqual(heatshrink.decode(encoded), quotes)

    def test_with_large_strings(self):
        test_sizes = [1000, 10000, 100000]

        for size in test_sizes:
            contents = random_string(size)

            decoded = heatshrink.decode(heatshrink.encode(contents))
            # Check whole file, but don't use assertEqual as it will print all the data
            if decoded != contents:
                msg = ('Decoded and original file contents '
                       'do not match for size: {}')
                self.fail(msg.format(size))
