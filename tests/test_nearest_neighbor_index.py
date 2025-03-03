"""nn_search_test"""

import random
import time
import unittest

from pynn import NearestNeighborIndex


class NearestNeighborIndexTest(unittest.TestCase):
    def test_basic(self):
        """
        test_basic tests a handful of nearest neighbor queries to make sure they return the right
        result.
        """

        test_points = [
            (1, 2),
            (1, 0),
            (10, 5),
            (-1000, 20),
            (3.14159, 42),
            (42, 3.14159),
        ]

        uut = NearestNeighborIndex(test_points)

        self.assertEqual((1, 0), uut.find_nearest((0, 0)))
        self.assertEqual((-1000, 20), uut.find_nearest((-2000, 0)))
        self.assertEqual((42, 3.14159), uut.find_nearest((40, 3)))

    def test_benchmark(self):
        """
        test_benchmark tests a bunch of values using the slow and fast version of the index
        to determine the effective speedup.
        """

        def rand_point():
            return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))

        # original point amounts
        # index_points = [rand_point() for _ in range(10000)]
        # query_points = [rand_point() for _ in range(1000)]
        # more points
        index_points = [rand_point() for _ in range(50000)]
        query_points = [rand_point() for _ in range(5000)]
        expected = []
        actual = []

        # Run the baseline slow tests to get the expected values.
        start = time.time()
        for query_point in query_points:
            expected.append(NearestNeighborIndex.find_nearest_slow(query_point, index_points))
        slow_time = time.time() - start

        # don't include the indexing time when benchmarking
        uut = NearestNeighborIndex(index_points)

        # Run the indexed tests
        start = time.time()
        for query_point in query_points:
            actual.append(uut.find_nearest(query_point))
        new_time = time.time() - start

        print(f"slow time: {slow_time:0.2f}sec")
        print(f"new time: {new_time:0.2f}sec")
        print(f"speedup: {(slow_time / new_time):0.2f}x")

    # TODO: Add more test cases to ensure your index works in different scenarios

    def test_many(self):
        """
        test_benchmark tests many values using the slow and fast version of the index
        to assert correctness
        """

        def rand_point():
            return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))

        index_points = [rand_point() for _ in range(10000)]
        query_points = [rand_point() for _ in range(1000)]
        expected = []
        actual = []

        # Run the baseline slow tests to get the expected values.
        for query_point in query_points:
            expected.append(NearestNeighborIndex.find_nearest_slow(query_point, index_points))

        # Run the fast tests to get the actual values.
        uut = NearestNeighborIndex(index_points)
        for query_point in query_points:
            actual.append(uut.find_nearest(query_point))

        # Assert the actual value from the fast algorithm is the expected value for each query point
        for index in range(len(actual)):
            assert actual[index] == expected[index]

    def test_no_points(self):
        """
        test_no_points tests that the fast algorithm does not crash and returns None
        when provided no indexed points
        """
        query_point = (random.uniform(-1000, 1000), random.uniform(-1000, 1000))
        uut = NearestNeighborIndex([])
        assert uut.find_nearest(query_point) == None
    
    def test_one_point(self):
        """
        test_one_points tests that the fast algorithm does not crash and returns
        the only point when provided a single indexed point
        """
        query_point = (random.uniform(-1000, 1000), random.uniform(-1000, 1000))
        single_point = (random.uniform(-1000, 1000), random.uniform(-1000, 1000))
        uut = NearestNeighborIndex([single_point])
        assert uut.find_nearest(query_point) == single_point

    def test_closest_is_first(self):
        test_points = [
            (-1000, 20),
            (1, 2),
            (1, 0),
            (10, 5),
            (3.14159, 42),
            (42, 3.14159),
        ]

        uut = NearestNeighborIndex(test_points)

        self.assertEqual((-1000, 20), uut.find_nearest((-1000, 0)))

    def test_closest_is_last(self):
        test_points = [
            (-1000, 20),
            (1, 2),
            (1, 0),
            (10, 5),
            (3.14159, 42),
            (42, 3.14159),
        ]

        uut = NearestNeighborIndex(test_points)

        self.assertEqual((42, 3.14159), uut.find_nearest((42, 0)))
    
    def test_multiple_closest_xs(self):
        test_points = [
            (-1000, 20),
            (1, 2),
            (1, 0),
            (1, 3),
            (1, 5),
            (1, 42),
            (42, 3.14159),
        ]

        uut = NearestNeighborIndex(test_points)

        self.assertEqual((1, 3), uut.find_nearest((1, 3)))
