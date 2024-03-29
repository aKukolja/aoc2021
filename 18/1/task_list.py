
class Number:

    def __init__(self, tree_list, small_fry=False):
        self._list = tree_list
        if small_fry:
            self._smallify()

    def __str__(self):
        retval = ""
        prev = -1
        for depth, value in self._list:
            retval += "  " * depth + str(value) + "\n"
        return retval

    

    @staticmethod
    def _from_array(llist, node, depth=0):
        left, right = node
        if isinstance(left, int):
            llist.append([depth, left])
        else:
            Number._from_array(llist, left, depth+1)
        if isinstance(right, int):
            llist.append([depth, right])
        else:
            Number._from_array(llist, right, depth+1)

    @staticmethod
    def from_array(arrays):
        tree_list = []
        Number._from_array(tree_list, arrays, 0)
        return Number(tree_list)

    def add(self, number):
        result = [[depth + 1, value] for depth, value in self._list + number._list]
        return Number(result, small_fry=True)

    @staticmethod
    def __explode(llist):
        for i, ((depth1, value1), (depth2, value2)) in enumerate(zip(llist, llist[1:])):
            if depth1 < 4 or depth2 < 4 or depth1 != depth2:
                continue
            if i > 0:
                " left node exists "
                llist[i-1][1] += value1
            if i < len(llist)-2:
                " right node does not exist "
                llist[i+2][1] += value2
            return llist[:i] + [[depth1-1, 0]] + llist[i+2:]

        return None

    def _explode(self):
        modified = Number.__explode(self._list)
        if modified is None:
            return False
        else:
            self._list = modified
            return True

    @staticmethod
    def __split(llist):
        for i, (depth, value) in enumerate(llist):
            if value < 10:
                continue
            a = int(value/2)
            b = value - a
            return llist[:i] + [[depth+1, a], [depth+1, b]] + llist[i+1:]
        return None

    def _split(self):
        modified = Number.__split(self._list)
        if modified is None:
            return False
        else:
            self._list = modified
            return True

    def _smallify(self):
        while True:
            if self._explode():
                continue
            if not self._split():
                break

    def magnitude(self):
        " reduce the number untill only one is left "
        magnitude = [t for t in self._list]
        while len(magnitude) > 1:
            for i, ((depth1, value1), (depth2, value2)) in enumerate(zip(magnitude, magnitude[1:])):
                if depth1 != depth2:
                    continue
                " this is leftmost pair "
                val = value1 * 3 + value2 * 2
                magnitude = magnitude[:i] + [[depth1-1, val]] + magnitude[i+2:]
                break

        return magnitude[0][1]

test = [
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
    [[[5,[2,8]],4],[5,[[9,9],0]]],
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
    [[[[5,4],[7,7]],8],[[8,3],8]],
    [[9,3],[[9,9],[6,[4,9]]]],
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]],
]

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
        number = Number.from_array(num_list)
        if summ is None:
            summ = number
        else:
            summ = summ.add(number)

    print(summ.magnitude())

