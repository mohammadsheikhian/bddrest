class AssertionFailed(AssertionError):
    def __init__(self, message):
        super().__init__(message)


class Assert:
    def __init__(self, target):
        self.target = target

    def get_full_qualified_name(self):
        return self.target.get_full_qualified_name()

    def resolve(self):
        return self.target

    def __getattr__(self, name):
        return AttributeAssert(self, name)

    def __getitem__(self, item):
        return GetItemAssert(self, item)


class RootAssert(Assert):
    def __init__(self, target, name='target'):
        super().__init__(target)
        self.name = name

    def get_full_qualified_name(self):
        return self.name


class AttributeAssert(Assert):
    def __init__(self, target, attribute_name=None):
        super().__init__(target)
        self.attribute_name = attribute_name

    def resolve(self):
        try:
            return getattr(self.target.resolve(), self.attribute_name)
        except AttributeError:
            raise AssertionFailed(
                f'Assertion Failed:\n'
                f'Object: {self.target.get_full_qualified_name()} has no attribute {self.attribute_name}'
            )

    def get_full_qualified_name(self):
        parent = super().get_full_qualified_name()
        return f'{parent}.{self.attribute_name}'


class GetItemAssert(Assert):
    def __init__(self, target, key=None):
        super().__init__(target)
        self.key = key

    def resolve(self):
        try:
            return self.target.resolve()[self.key]
        except (KeyError, IndexError):
            raise AssertionFailed(
                f'Assertion Failed:\n'
                f'Object: {self.target.get_full_qualified_name()} has no item {self.key}'
            )

    def get_full_qualified_name(self):
        parent = super().get_full_qualified_name()
        if isinstance(self.key, slice):
            key = f'{self.key.start or ""}:{self.key.stop or ""}'
            if self.key.step:
                key += f':{self.key.step}'
        elif isinstance(self.key, str):
            key = f'\'{self.key}\''
        else:
            key = self.key
        return f'{parent}[{key}]'


__all__ = [
    'AssertionFailed',
    'Assert',
    'RootAssert',
    'AttributeAssert',
    'GetItemAssert',
]
    # @property
    # def new_expression(self):
    #     return functools.partial(ExpressionProxy, self)
    #
    # def __eq__(self, other):
    #     return self.new_expression('==', other)
    #
    # def __ne__(self, other):
    #     return self.new_expression('!=', other, negative=True)
#
#
# class ExpressionProxy(ObjectProxy):
#
#     def __init__(self, backend, operator, expected, negative=None):
#         super().__init__(backend)
#         self.operator = operator
#         self.expected = expected
#         self.negative = negative
#
#     def evaluate(self):
#         actual = super().evaluate()
#         ok = eval(f'{actual} {self.operator} {self.expected}')
#         if not ok:
#             expression = f'response.{self.get_full_qualified_name()} {self.operator} {self.expected}'
#             print(f'The expression: {expression} is failed.')
#             print(f'{"Not " if self.negative else ""}Expected: {self.expected}')
#             print(f'Actual: {actual}')