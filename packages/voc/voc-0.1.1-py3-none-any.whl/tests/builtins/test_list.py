from .. utils import TranspileTestCase, BuiltinFunctionTestCase


class ListTests(TranspileTestCase):
    pass


class BuiltinListFunctionTests(BuiltinFunctionTestCase, TranspileTestCase):
    functions = ["list"]

    not_implemented = [
        'test_bytearray',
        'test_bytes',
        'test_class',
        'test_complex',
        'test_dict',
        'test_frozenset',
        'test_set',
        'test_str',
    ]
