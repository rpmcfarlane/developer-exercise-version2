import math


class NearestNeighborIndex:
    """
    TODO give me a decent comment

    NearestNeighborIndex is intended to index a set of provided points to provide fast nearest
    neighbor lookup. For now, it is simply a stub that performs an inefficient traversal of all
    points every time.
    """

    def __init__(self, points):
        """
        takes an array of 2d tuples as input points to be indexed.
        """
        self.points = points

    @staticmethod
    def find_nearest_slow(query_point, haystack):
        """
        find_nearest_slow returns the point that is closest to query_point. If there are no indexed
        points, None is returned.
        """

        min_dist = None
        min_point = None

        for point in haystack:
            deltax = point[0] - query_point[0]
            deltay = point[1] - query_point[1]
            dist = math.sqrt(deltax * deltax + deltay * deltay)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_point = point

        return min_point

    def find_nearest_fast(self, query_point, abs=abs):
        """
        TODO: Re-implement me with your faster solution.

        find_nearest_fast returns the point that is closest to query_point. If there are no indexed
        points, None is returned.
        """

        if (self.points):
            # reduce array indexing by setting query's x and y
            query_x, query_y = query_point

            # assume first point is closest to avoid checking min_dist's truthiness
            min_point = self.points[0]
            min_deltax = abs(self.points[0][0] - query_x)
            min_deltay = abs(self.points[0][1] - query_y)
            # square root function is continuous and increasing, unnecessary for comparisons
            min_dist_squared = min_deltax * min_deltax + min_deltay * min_deltay

            for next_x, next_y in self.points:
                deltax = abs(next_x - query_x)
                deltay = abs(next_y - query_y)

                # if both deltas are larger, distance must be greater
                if deltax > min_deltax and deltay > min_deltay:
                    continue

                dist_squared = deltax * deltax + deltay * deltay
                if dist_squared < min_dist_squared:
                    min_dist_squared = dist_squared
                    min_point = (next_x, next_y)
                    min_deltax = deltax
                    min_deltay = deltay

            return min_point

        return None

    def find_nearest(self, query_point):
        """
        find_nearest finds the nearest point to query_point using the find_nearest_fast algorithm
        """

        return self.find_nearest_fast(query_point)
