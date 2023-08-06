from .. utils import TranspileTestCase, UnaryOperationTestCase, BinaryOperationTestCase, InplaceOperationTestCase


class SetTests(TranspileTestCase):
    def test_setattr(self):
        self.assertCodeExecution("""
            x = {1, 2, 3}
            x.attr = 42
            print('Done.')
            """)

    def test_getattr(self):
        self.assertCodeExecution("""
            x = {1, 2, 3}
            print(x.attr)
            print('Done.')
            """)

    def test_creation(self):
        # Empty dict
        self.assertCodeExecution("""
            x = set()
            print(x)
            """)

        # Set constant
        self.assertCodeExecution("""
            x = {'a'}
            print(x)
            """)

        self.assertCodeExecution("""
            x = set(['a'])
            print(x)
            """)

    def test_getitem(self):
        # Simple existent key
        self.assertCodeExecution("""
            x = {'a', 'b'}
            print('a' in x)
            """)

        # Simple non-existent key
        self.assertCodeExecution("""
            x = {'a', 'b'}
            print('c' in x)
            """)

    def test_pop(self):
        # Test empty set popping.
        self.assertCodeExecution("""
            x = set()
            x.pop()
        """)

        # Test populated set popping.
        self.assertCodeExecution("""
            x = {'a'}
            print(len(x) == 1)
            x.pop()
            print(len(x) == set())
        """)

        # Test popping returns from set.
        self.assertCodeExecution("""
            x = {'a', 'b', 'c', 'd', 'e'}
            y = x.pop()
            print(y in x)
        """)


class UnarySetOperationTests(UnaryOperationTestCase, TranspileTestCase):
    data_type = 'set'


class BinarySetOperationTests(BinaryOperationTestCase, TranspileTestCase):
    data_type = 'set'

    not_implemented = [
        'test_add_class',
        'test_add_complex',
        'test_add_frozenset',

        'test_and_class',
        'test_and_complex',
        'test_and_frozenset',
        'test_and_set',

        'test_eq_class',
        'test_eq_complex',
        'test_eq_frozenset',

        'test_floor_divide_class',
        'test_floor_divide_complex',
        'test_floor_divide_frozenset',

        'test_ge_class',
        'test_ge_complex',
        'test_ge_frozenset',

        'test_gt_class',
        'test_gt_complex',
        'test_gt_frozenset',

        'test_le_class',
        'test_le_complex',
        'test_le_frozenset',

        'test_lshift_class',
        'test_lshift_complex',
        'test_lshift_frozenset',

        'test_lt_class',
        'test_lt_complex',
        'test_lt_frozenset',

        'test_modulo_class',
        'test_modulo_complex',
        'test_modulo_frozenset',

        'test_multiply_bytearray',
        'test_multiply_bytes',
        'test_multiply_class',
        'test_multiply_complex',
        'test_multiply_frozenset',

        'test_ne_class',
        'test_ne_complex',
        'test_ne_frozenset',

        'test_or_class',
        'test_or_complex',
        'test_or_frozenset',
        'test_or_set',

        'test_power_class',
        'test_power_complex',
        'test_power_frozenset',

        'test_rshift_class',
        'test_rshift_complex',
        'test_rshift_frozenset',

        'test_subtract_class',
        'test_subtract_complex',
        'test_subtract_frozenset',
        'test_subtract_set',

        'test_subscr_class',
        'test_subscr_complex',
        'test_subscr_frozenset',

        'test_true_divide_class',
        'test_true_divide_complex',
        'test_true_divide_frozenset',

        'test_xor_class',
        'test_xor_complex',
        'test_xor_frozenset',
        'test_xor_set',
    ]


class InplaceSetOperationTests(InplaceOperationTestCase, TranspileTestCase):
    data_type = 'set'

    not_implemented = [
        'test_add_class',
        'test_add_complex',
        'test_add_frozenset',

        'test_and_class',
        'test_and_complex',
        'test_and_frozenset',
        'test_and_set',

        'test_floor_divide_class',
        'test_floor_divide_complex',
        'test_floor_divide_frozenset',

        'test_lshift_class',
        'test_lshift_complex',
        'test_lshift_frozenset',

        'test_modulo_class',
        'test_modulo_complex',
        'test_modulo_frozenset',

        'test_multiply_class',
        'test_multiply_complex',
        'test_multiply_frozenset',

        'test_or_class',
        'test_or_complex',
        'test_or_frozenset',
        'test_or_set',

        'test_power_class',
        'test_power_complex',
        'test_power_frozenset',

        'test_rshift_class',
        'test_rshift_complex',
        'test_rshift_frozenset',

        'test_subtract_class',
        'test_subtract_complex',
        'test_subtract_frozenset',
        'test_subtract_set',

        'test_true_divide_class',
        'test_true_divide_complex',
        'test_true_divide_frozenset',

        'test_xor_class',
        'test_xor_complex',
        'test_xor_frozenset',
        'test_xor_set',
    ]
