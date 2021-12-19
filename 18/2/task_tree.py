
class SnailNumber:

    def __init__(self, left, right):
        self.parent = None
        self.left, self.right = left, right

    def __str__(self):
        return "["+str(self.left)+","+str(self.right)+"]"

    @staticmethod
    def from_array(line, parent=None):
        left, right = line
        created = SnailNumber(None, None)
        if not isinstance(left, int):
            left = SnailNumber.from_array(left, parent=created)
        if not isinstance(right, int):
            right = SnailNumber.from_array(right, parent=created)
        created = SnailNumber(left, right)
        created.parent = parent
        return created

    def _left_neighbour(self):
        coming_from = self
        node = self.parent
        " ascend the tree while coming from the left child "
        while node is not None and coming_from == node.left:
            coming_from = node
            node = node.parent
        if node is None:
            return None
        " we last came from right child "
        assert(node.right == coming_from)
        if isinstance(node.left, int):
            " left child is int value "
            return node
        node = node.left
        while True:
            if isinstance(node.right, int):
                return node
            node = node.right
        " structure demands that each node be terminated with int "
        print(node)
        assert(False)

    def _right_neighbour(self):
        coming_from = self
        node = self.parent
        while node is not None and coming_from == node.right:
            coming_from = node
            node = node.parent
        if node is None:
            return None
        " we last came from left child "
        assert(node.left == coming_from)
        node = node.right
        while True:
            if isinstance(node.left, int):
                return node
            node = node.left
        " structure demands that each node be terminated with int "
        print(node)
        assert(False)

    def _explode(self):
        left_neighbour = self._left_neighour()
        right_neighbour = self._right_neighbour()
        " this node must be removed from the tree "
        if left_neighbour is not None:
            if left_neighbour.right == self:
                left_neighbour.left += self._left
            else:
                left_neighbour.right += self._left
        if right_neighbour is not None:
            right_neighbour.left += self._right
        if self.parent.left == self:
            " we are left child "
            parent.left = 0
        else
            " we are right child "
            parent.right = 0

    @staticmethod
    def _handle(node, depth=0):
        " if any pair is nested inside four pairs, the leftomst such pair explodes "
        " if any regular number is 10 or greater, the leftmost such regular number splits "
        if isinstance(node, int):
            return True
        assert(depth < 5)
        if depth >= 4:
            " destroy this pair by adding to the left, and right subtrees "
            node._explode()
            return False
        if isinstance(node.left, int) and node.left > 10:
            self._split_left()
            return False
        if isinstance(node.right, int) and node.right > 10:
            self._split_right()
            return False
        return SnailNumber._handle(node.left, depth+1) and SnailNumber._handle(node.right, depth+1)

    def add(self, number):
        left_tree, right_tree = node
        created = SnailNumber(left_tree, right_tree)
        left_tree.parent, right_tree.parent = created, created
        SnailNumber._handle(created)
        return created

    def weight(self):
        return 0


data = [
    [[[[7,7],2],[[9,2],4]],[[[9,1],5],[[9,6],[6,4]]]],
    [[[2,0],[8,[9,4]]],[[1,0],0]],
    [8,[[[9,5],7],[9,7]]],
    [[[[1,3],[1,8]],[[8,8],5]],[[7,[4,0]],2]],
    [[[[7,8],3],[9,3]],5],
    [[5,[[9,3],4]],[[[0,1],7],[6,[8,3]]]],
    [[[[1,6],[4,1]],[0,3]],[9,[[4,3],[3,2]]]],
    [[[[7,9],8],4],[[[9,0],1],[[9,8],[0,5]]]],
    [[[8,7],[6,1]],[[[1,3],[6,6]],[5,[4,5]]]],
    [[[[9,8],[2,1]],[[2,3],2]],5],
    [6,3],
    [[[9,1],6],[[[7,1],[6,8]],[[8,3],[6,4]]]],
    [4,[[8,[7,1]],[8,[7,2]]]],
    [[[1,6],[9,[0,8]]],[[6,7],[2,[4,5]]]],
    [[[[1,8],[9,2]],5],[[[8,6],[2,1]],[0,6]]],
    [[[[0,2],4],[4,[3,6]]],7],
    [[[[7,5],5],7],[[[6,0],4],[5,0]]],
    [[2,1],[[[3,0],[1,4]],7]],
    [[[[9,4],[2,8]],9],[[[9,1],[7,3]],[1,[2,1]]]],
    [[[[4,2],3],[6,4]],[[6,0],[1,5]]],
    [2,6],
    [[4,6],[[2,2],[3,0]]],
    [[[[6,4],[0,7]],[0,8]],[[[6,7],2],7]],
    [[8,[[4,0],[8,4]]],1],
    [[3,[6,6]],[[[6,4],[1,5]],[4,0]]],
    [[[9,5],[5,[4,0]]],[[1,[0,6]],[[5,8],0]]],
    [[[[6,1],8],[3,7]],[[[6,4],0],[[4,8],4]]],
    [[[[3,1],3],[[3,6],[3,8]]],[[[6,7],0],2]],
    [[4,1],[[[4,8],7],[3,0]]],
    [[[[0,6],[1,3]],[[0,8],[1,9]]],3],
    [[0,[3,1]],[[[0,0],6],[[7,6],3]]],
    [[6,[[5,4],7]],[8,[5,5]]],
    [[[6,3],[[8,9],6]],2],
    [9,[[8,3],7]],
    [[[1,[3,0]],[[3,7],5]],[[5,8],[[3,7],[8,6]]]],
    [[[[6,1],2],[[7,8],[3,9]]],[[[3,6],[6,8]],[5,5]]],
    [[[[6,8],[7,1]],[8,1]],[[[1,6],9],[[3,3],[7,9]]]],
    [[[[6,9],0],[5,6]],3],
    [[[9,6],[[0,5],[2,0]]],[[[6,7],7],[2,6]]],
    [[0,[5,8]],[[1,[4,6]],[4,6]]],
    [[[[3,3],4],[0,1]],[[[6,5],0],[2,3]]],
    [0,4],
    [[5,5],[[[6,5],8],7]],
    [[[[7,3],[9,1]],[[9,0],2]],[[7,[8,3]],[[9,5],[7,3]]]],
    [[[[1,2],[7,7]],[9,0]],[0,7]],
    [[[0,[8,6]],[1,3]],[[6,6],9]],
    [[[0,2],[4,7]],0],
    [[[9,[9,6]],1],[[[1,5],[1,7]],[[5,1],[8,1]]]],
    [[[6,9],4],0],
    [[[[4,9],6],5],[7,[3,[9,8]]]],
    [[6,[6,[5,7]]],[0,[[7,4],8]]],
    [[4,[5,0]],[2,3]],
    [[[[8,6],9],[3,[1,2]]],[1,[8,[3,8]]]],
    [[[8,4],[7,2]],9],
    [[[[6,3],[6,2]],[2,[0,0]]],[[[6,4],[1,6]],[[3,5],6]]],
    [7,[[[2,4],0],[9,[9,9]]]],
    [[[9,2],8],[[2,[9,9]],[9,[7,4]]]],
    [1,[[0,7],[[1,6],0]]],
    [[[[5,5],4],8],[[9,[6,5]],[[7,4],7]]],
    [[[[7,6],4],[8,4]],[2,[1,[5,1]]]],
    [[[2,[1,2]],7],[7,[[9,9],3]]],
    [1,[[3,[9,9]],[5,6]]],
    [[3,[[1,8],4]],[[9,[6,9]],2]],
    [[[2,[4,5]],[1,[9,0]]],[4,1]],
    [[[7,[5,9]],[7,7]],[[3,[4,0]],[2,[0,0]]]],
    [[[0,[9,8]],0],[8,[7,1]]],
    [[[6,6],[0,[4,8]]],3],
    [[1,[[8,2],[9,9]]],3],
    [[2,[5,[6,7]]],[[5,3],3]],
    [[2,[[5,0],[8,5]]],[[7,[0,5]],[[5,7],3]]],
    [[[[9,4],[4,0]],[6,[7,8]]],[[7,6],1]],
    [[0,2],6],
    [[[7,5],[[7,4],[4,1]]],[3,[[6,6],[5,5]]]],
    [[3,[[0,7],8]],[[1,7],[5,0]]],
    [[9,[[9,7],[3,0]]],6],
    [[[[7,9],2],[3,[5,4]]],[[[9,4],[5,8]],[[5,0],[4,2]]]],
    [[[[4,3],6],7],[[2,6],[5,[0,1]]]],
    [[1,[3,5]],[[4,[5,0]],1]],
    [[[9,[3,9]],8],[9,[[2,9],[2,2]]]],
    [[[0,[5,0]],[[4,4],3]],6],
    [[[9,3],[[2,4],[8,4]]],[[[6,8],[3,6]],[[4,6],[1,2]]]],
    [[[[8,2],[3,2]],[4,[1,1]]],[[[7,2],1],[[9,9],[0,5]]]],
    [[[6,3],[[3,6],9]],[6,5]],
    [8,[[[8,7],3],[4,3]]],
    [[[[8,3],3],[[6,1],9]],[[[2,4],[5,9]],[[9,7],1]]],
    [[[2,[6,4]],[[0,1],3]],[[[1,2],9],[4,7]]],
    [7,9],
    [[[3,[1,4]],5],[[4,[5,1]],8]],
    [[[[7,6],4],0],[5,5]],
    [[4,[[5,2],5]],[[[0,4],[6,1]],[[3,0],[4,9]]]],
    [[[[8,6],[6,1]],9],[[[4,1],2],[[9,2],3]]],
    [[[6,1],[[8,9],[9,0]]],[[[4,4],[3,0]],[[4,2],[9,9]]]],
    [1,[[[8,8],3],7]],
    [[1,[4,[6,8]]],[1,[7,0]]],
    [6,[[3,[2,4]],[[4,5],[5,3]]]],
    [8,[[9,[6,0]],[[2,5],0]]],
    [[5,[0,8]],[[7,1],[[5,9],2]]],
    [[[5,8],[[1,1],4]],[[0,1],[4,3]]],
    [[3,[1,[7,3]]],[[[6,4],9],[[2,8],[0,1]]]],
    [[[6,[2,5]],5],[0,[[5,3],[4,2]]]]
]


if __name__ == "__main__":
    summ = None
    for num_list in data:
        print("list", num_list)
        number = SnailNumber.from_array(num_list)
        print("number", number)
        print()
        """
        if summ is None:
            summ = number
        else:
            summ = summ.add(number)
        """

    print(summ.weight())

