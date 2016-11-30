import hmac
import os
import re

def _generate_digit():
    """Return a string containing a single decimal digit chosen uniformly and at
    random."""
    # We use rejection sampling on the lower nibble of single byte values to
    # ensure uniformity.
    while True:
        v = os.urandom(1)[0] & 0xF
        if v < 10:
            return str(v)

def generate_pin():
    """Returns a 9 digit PIN as a string. The PIN is separated into triplets by
    hyphens.

    """
    return '-'.join(
        ''.join(_generate_digit() for _ in range(3)) for _ in range(3))

def compare_pin(given, expected):
    """Compare a PIN from the user to the one expected (generated by
    generate_pin).

    Return True iff the given PIN matches. Non-digit values are ignored in the
    given PIN. Only hyphens are stripped from the expected PIN.

    """
    expected = expected.replace('-', '')
    given = re.sub(r'[^0-9]', '', given)

    # Constant time comparison. Probably overkill for this application but let's
    # at least try to be good boys and girls.
    return hmac.compare_digest(given, expected)
