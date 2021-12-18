# https://adventofcode.com/2021/day/18

from copy import deepcopy

FILE = 'input.txt'
# FILE = 'input-small.txt'

post_order_before_explosion = None
preorder_after_explosion = None


class SnailNumber:

    def __init__(self, string: str = None, value: int = None, left: 'SnailNumber' = None, right: 'SnailNumber' = None):
        if string is not None:
            tokens = self._tokenize(string)
            s = []
            for t in tokens:
                if t == '[':
                    pass
                elif t == ']':
                    # pop two numbers
                    left, right = s[-2:]
                    del s[-2:]

                    number = SnailNumber(left=left, right=right)
                    s.append(number)
                else:
                    s.append(SnailNumber(value=int(t)))  # number

        self.value = value
        self.left = left
        self.right = right

    @staticmethod
    def _tokenize(string: str):
        return string.replace('[', '[,').replace(']', ',]').split(',')

    def __str__(self):
        if self.is_number():
            return str(self.value)

        return "[{},{}]".format(self.left, self.right)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other: 'SnailNumber'):
        if self.is_empty():
            return other
        elif other.is_empty():
            return self

        number = SnailNumber(left=deepcopy(self), right=deepcopy(other))
        number._reduce()

        return number

    def is_pair(self):
        return not self.is_number()

    def is_number(self):
        return self.value is not None

    def has_left_int(self):
        return self.left.is_number()

    def has_right_int(self):
        return self.right.is_number()

    def is_empty(self):
        return self.value == self.left == self.right is None

    def magnitude(self):
        if self.is_number():
            return self.value

        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def _reduce(self):
        reduce = True

        while reduce:
            reduce = self._explode() or self._split()

        return self

    def _split(self) -> bool:
        def find_splitting_node(node):
            if node.is_number() and node.value >= 10:
                left_value = node.value // 2

                left = SnailNumber(value=left_value)
                right = SnailNumber(value=(node.value - left_value))

                node.value = None
                node.left = left
                node.right = right

                assert node.is_pair()

                return True
            elif node.is_pair():
                return find_splitting_node(node.left) or find_splitting_node(node.right)

        return find_splitting_node(self)

    def _explode(self) -> bool:
        global post_order_before_explosion, preorder_after_explosion
        post_order_before_explosion = None
        preorder_after_explosion = None

        def find_exploding_node(node, depth, exploding_node=None):
            global post_order_before_explosion, preorder_after_explosion

            if preorder_after_explosion is not None:
                return exploding_node

            if depth == 4 and exploding_node is None:
                exploding_node = node

                # should be leaf node
                assert node.left.is_number() and node.right.is_number()

            if node.left.is_pair():
                exploding_node = find_exploding_node(node.left, depth + 1, exploding_node)
            else:
                if exploding_node is not None and preorder_after_explosion is None and node.left not in [exploding_node.left, exploding_node.right]:
                    preorder_after_explosion = node.left

                if exploding_node is None:
                    post_order_before_explosion = node.left

            if node.right.is_pair():
                exploding_node = find_exploding_node(node.right, depth + 1, exploding_node)
            else:
                if exploding_node is not None and preorder_after_explosion is None and node.right not in [exploding_node.left, exploding_node.right]:
                    preorder_after_explosion = node.right

                if exploding_node is None:
                    post_order_before_explosion = node.right

            return exploding_node

        depth = 0
        exploding_node = find_exploding_node(self, depth)

        if exploding_node is not None:
            left, right = exploding_node.left, exploding_node.right
            assert left.is_number() and right.is_number()

            exploding_node.value = 0
            exploding_node.left = None
            exploding_node.right = None

            if post_order_before_explosion is not None:
                assert post_order_before_explosion.is_number()
                post_order_before_explosion.value += left.value

            if preorder_after_explosion is not None:
                assert preorder_after_explosion.is_number()
                preorder_after_explosion.value += right.value

        return exploding_node is not None


with open(FILE) as f:
    snail_numbers = []
    for line in f.readlines():
        snail_numbers.append(SnailNumber(line.strip()))
    result = sum(snail_numbers, SnailNumber())
    # print(result)
    print(result.magnitude())  # 1. part

    max_magnitude = 0
    for n1 in snail_numbers:
        for n2 in snail_numbers:
            if n1 == n2:
                continue

            n12 = n1 + n2
            magnitude = n12.magnitude()
            if max_magnitude < magnitude:
                max_magnitude = magnitude

    print(max_magnitude)  # 2. part
