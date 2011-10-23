from sympy.core import Basic
from sympy.combinatorics.graycode import GrayCode

import itertools

class Subset(Basic):
    """
    Represents a basic subset object.

    We generate subsets using essentially two techniques,
    binary enumeration and lexicographic enumeration.

    Examples:
    >>> from sympy.combinatorics.subsets import Subset
    >>> a = Subset(['c','d'],['a','b','c','d'])
    >>> a.next_binary()
    Subset(['b'], ['a', 'b', 'c', 'd'])
    >>> a.prev_binary()
    Subset(['c'], ['a', 'b', 'c', 'd'])
    """

    _rank_binary = None
    _rank_lex = None
    _rank_graycode = None

    def iterate_binary(self, k):
        """
        This is a helper function. It iterates over the
        binary subsets by k steps. This variable can be
        both positive or negative.

        Examples:
        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset(['c','d'],['a','b','c','d'])
        >>> a.iterate_binary(-2)
        Subset(['d'], ['a', 'b', 'c', 'd'])
        >>> a = Subset(['a','b','c'],['a','b','c','d'])
        >>> a.iterate_binary(2)
        Subset([], ['a', 'b', 'c', 'd'])
        """
        bin_list = Subset.get_bitlist_from_subset(self.subset, self.superset)
        next_bin_list = list(bin((int(reduce(lambda x, y:
                                             x + y, bin_list), 2) + k)
                                 % 2**self.superset_size))[2:]
        next_bin_list = [0] * (self.superset_size - len(next_bin_list)) + \
                        next_bin_list
        return Subset.get_subset_from_bitlist(self.superset, next_bin_list)


    def next_binary(self):
        """
        Generates the next binary ordered subset.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset(['c','d'],['a','b','c','d'])
        >>> a.next_binary()
        Subset(['b'], ['a', 'b', 'c', 'd'])
        >>> a = Subset(['a','b','c','d'],['a','b','c','d'])
        >>> a.next_binary()
        Subset([], ['a', 'b', 'c', 'd'])
        """
        return self.iterate_binary(1)

    def prev_binary(self):
        """
        Generates the previous binary ordered subset.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset([],['a','b','c','d'])
        >>> a.prev_binary()
        Subset(['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'])
        >>> a = Subset(['c','d'],['a','b','c','d'])
        >>> a.prev_binary()
        Subset(['c'], ['a', 'b', 'c', 'd'])
        """
        return self.iterate_binary(-1)

    def next_lexicographic(self):
        """
        Generates the next lexicographically ordered
        subset.

        Examples:
        """
        raise NotImplementedError()

    def prev_lexicographic(self):
        """
        Generates the previous lexicographically ordered
        subset.

        Examples:
        """
        raise NotImplementedError()

    def iterate_graycode(self, k):
        """
        Helper function used for prev_graycode and next_graycode.
        It performs k step overs to get the respective graycodes.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset([1,2,3],[1,2,3,4])
        >>> a.iterate_graycode(3)
        Subset([3, 4], [1, 2, 3, 4])
        >>> a.iterate_graycode(-2)
        Subset([2], [1, 2, 3, 4])
        """
        unranked_code = GrayCode.unrank_gray_code((self.rank_graycode+k)\
                                                  % self.cardinality,
                                                  self.superset_size)
        return Subset.get_subset_from_bitlist(self.superset,
                                              unranked_code._current)

    def next_graycode(self):
        """
        Generates the next gray code ordered subset.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset([1,2,3],[1,2,3,4])
        >>> a.next_graycode()
        Subset([1, 3], [1, 2, 3, 4])
        """
        return self.iterate_graycode(1)

    def prev_graycode(self):
        """
        Generates the previous gray code ordered subset.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset([2,3,4],[1,2,3,4,5])
        >>> a.prev_graycode()
        Subset([1, 2, 3, 4], [1, 2, 3, 4, 5])
        """
        return self.iterate_graycode(-1)

    @property
    def rank_binary(self):
        """
        Computes the binary ordered rank.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset([],['a','b','c','d'])
        >>> a.rank_binary
        0
        >>> a = Subset(['c','d'],['a','b','c','d'])
        >>> a.rank_binary
        3
        """
        if self._rank_binary == None:
            self._rank_binary = int("".join(
                Subset.get_bitlist_from_subset(self.subset,
                                               self.superset)), 2)
        return self._rank_binary

    @property
    def rank_lexicographic(self):
        """
        Computes the lexicographic ranking of the subset.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset(['c','d'],['a','b','c','d'])
        >>> a.rank_lexicographic
        14
        >>> a = Subset([2,4,5],[1,2,3,4,5,6])
        >>> a.rank_lexicographic
        43
        """
        if self._rank_lex == None:
            superset_index = list(xrange(self.superset_size))
            subset_index = [self.superset.index(j) for j in self.subset]
            def ranklex(self, subset_index, i, n):
                if subset_index == [] or i > n:
                    return 0
                if i in subset_index:
                    subset_index.remove(i)
                    return 1 + ranklex(self, subset_index, i + 1, n)
                return 2**(n - i - 1) + ranklex(self, subset_index, i + 1, n)
            self._rank_lex = ranklex(self, subset_index, 0, self.superset_size)
        return self._rank_lex

    @property
    def rank_graycode(self):
        """
        Computes the gray code ranking of the subset.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> a = Subset(['c','d'],['a','b','c','d'])
        >>> a.rank_graycode
        8
        >>> a = Subset([2,4,5],[1,2,3,4,5,6])
        >>> a.rank_graycode
        19
        """
        if self._rank_graycode == None:
            bits = Subset.get_bitlist_from_subset(self.subset, self.superset)
            self._rank_graycode = GrayCode(start = bits).rank
        return self._rank_graycode

    @property
    def subset(self):
        """
        Gets the subset represented by the current instance.
        """
        return self.args[0]

    @property
    def size(self):
        """
        Gets the size of the subset.
        """
        return len(self.subset)

    @property
    def superset(self):
        """
        Gets the superset of the subset.
        """
        return self.args[1]

    @property
    def superset_size(self):
        """
        Returns the size of the superset.
        """
        return len(self.superset)

    @property
    def cardinality(self):
        """
        Returns the number of all possible subsets.
        """
        return 2**(self.superset_size)

    @classmethod
    def get_subset_from_bitlist(self, super_set, bitlist):
        """
        Gets the subset defined by the bitlist.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> Subset.get_subset_from_bitlist(['a','b','c','d'], \
        ['0','0','1','1'])
        Subset(['c', 'd'], ['a', 'b', 'c', 'd'])
        """
        if len(super_set) != len(bitlist):
            raise ValueError("The sizes of the lists are not equal")
        ret_set = []
        for i in xrange(len(bitlist)):
            if bitlist[i] == '1':
                ret_set.append(super_set[i])
        return Subset(ret_set, super_set)

    @classmethod
    def get_bitlist_from_subset(self, subset, superset):
        """
        Gets the bitlist corresponding to a subset.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> Subset.get_bitlist_from_subset(['c','d'],['a','b','c','d'])
        ['0', '0', '1', '1']
        """
        bitlist = ['0'] * len(superset)
        if type(subset) is Subset:
            subset = subset.args[0]
        for i in subset:
            bitlist[superset.index(i)] = '1'
        return bitlist

    @classmethod
    def unrank_binary(self, rank, superset):
        """
        Gets the binary ordered subset of the
        specified rank.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> Subset.unrank_binary(4,['a','b','c','d'])
        Subset(['b'], ['a', 'b', 'c', 'd'])
        """
        bin_list = list(bin(rank))[2:]
        bin_list = [0] * (len(superset) - len(bin_list)) + bin_list
        return Subset.get_subset_from_bitlist(superset, bin_list)

    @classmethod
    def unrank_graycode_subset(self, rank, superset):
        """
        Gets the gray code ordered subset of the
        specified rank.

        Examples:
        >>> from sympy.combinatorics.subsets import Subset
        >>> Subset.unrank_graycode_subset(4, ['a','b','c'])
        Subset(['b', 'c'], ['a', 'b', 'c'])
        >>> Subset.unrank_graycode_subset(0, ['a','b','c'])
        Subset([], ['a', 'b', 'c'])
        """
        graycode_bitlist = GrayCode.unrank_gray_code(rank,
                                                     len(superset))._current
        return Subset.get_subset_from_bitlist(superset, graycode_bitlist)

def ksubsets(superset, k):
    """
    Finds the subsets of size k in lexicographic order.

    This uses the itertools generator.

    Examples:
    >>> from sympy.combinatorics.subsets import ksubsets
    >>> list(ksubsets([1,2,3], 2))
    [(1, 2), (1, 3), (2, 3)]
    >>> list(ksubsets([1,2,3,4,5], 2))
    [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), \
    (2, 5), (3, 4), (3, 5), (4, 5)]
    """
    return (itertools.combinations(superset, k))
