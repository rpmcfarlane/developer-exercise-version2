import math


class NearestNeighborIndex:
    """
    TODO give me a decent comment

    NearestNeighborIndex is indexes a set of provided points using a selection sort
    on the x coordinate to provide fast nearest neighbor lookup. After performing the
    selection sort, the point nearest the query point is found by ruling out the edges
    of the lists of indexed points by comparing their x coordinate to the current 
    minimum distance.
    """

    def __init__(self, points):
        """
        takes an array of 2d tuples as input points to be indexed.
        """
        self.points = points
        self.sorted_points = self.selection_sort()

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
        find_nearest_fast returns the point that is closest to query_point. If there are no indexed
        points, None is returned.
        """

        if self.points:
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

                if deltax < min_deltax:
                    new_dist_squared = deltay * deltay
                    # if the y distance is not larger than the prev distance, check with the x
                    if new_dist_squared < min_dist_squared:
                        new_dist_squared += deltax * deltax
                        if new_dist_squared < min_dist_squared:
                            min_dist_squared = new_dist_squared
                            min_point = (next_x, next_y)
                            min_deltax = deltax
                            min_deltay = deltay
                elif deltay < min_deltay:
                    new_dist_squared = deltax * deltax
                    # if the x distance is not larger than the prev distance, check with the y
                    if new_dist_squared < min_dist_squared:
                        new_dist_squared += deltay * deltay
                        if new_dist_squared < min_dist_squared:
                            min_dist_squared = new_dist_squared
                            min_point = (next_x, next_y)
                            min_deltax = deltax
                            min_deltay = deltay

            return min_point

        return None

    def find_nearest_x(self, query_x, abs=abs):
        """
        find_nearest_x returns the point that has the closest x
        coordinate to the query_point using a list of points sorted by their x coordinate.
        The search diverges from a starting point and checks the left and right sides,
        stopping its search on a given side when the difference in x starts to grow,
        indicating that it has passed the closest. 
        """
        # start with the median x coordinate
        starting_index = round(len(self.sorted_points)/2)
        point_x, _ = self.sorted_points[starting_index]
        min_index = starting_index
        min_deltax = abs(point_x - query_x)
        index = starting_index
        while index >= 0:
            deltax = abs(self.sorted_points[index][0] - query_x)
            # if the x distance is starting to grow, the closest has been surpassed
            if deltax > min_deltax:
                break
            if deltax < min_deltax:
                min_deltax = deltax
                min_index = index
            index -= 1
        # if a closer x has been found on the left side, one won't be found on the right
        if index != starting_index:
            return index
        while starting_index < len(self.sorted_points):
            deltax = abs(self.sorted_points[starting_index][0] - query_x)
            # if the x distance is starting to grow, the closest has been surpassed
            if deltax > min_deltax:
                break
            if deltax < min_deltax:
                min_deltax = deltax
                min_index = starting_index
            starting_index += 1

        return min_index

    def find_nearest_sorted(self, query_point, abs=abs):
        """
        find_nearest_sorted returns the point that is closest to query_point
        using a list of points sorted by their x coordinate. The search diverges
        from a starting point and checks the left and right sides, stopping the
        search of a given side when the x is so far from the query point that
        it rules out the remaining points from being closer. 
        If there are no indexed points, None is returned.
        """
        min_point = None
        if self.sorted_points:
            # reduce array indexing by setting query's x and y
            query_x, query_y = query_point
            # find the start index, the point with the nearest x coordinate
            start_index = self.find_nearest_x(query_x)
            min_point = self.sorted_points[start_index]
            start_x, start_y = min_point
            min_deltax = abs(start_x - query_x)
            min_deltay = abs(start_y - query_y)
            min_dist_squared = min_deltax * min_deltax + min_deltay * min_deltay
            min_dist = math.sqrt(min_dist_squared)
            # check left side
            index = start_index
            while index >= 0:
                next_x, next_y = self.sorted_points[index]
                deltax = abs(next_x - query_x)
                # if the x distance alone rules out a point, no other points on this side could work
                if deltax > min_dist: 
                    break
                deltay = abs(next_y - query_y)
                new_dist_squared = deltax * deltax + deltay * deltay
                if new_dist_squared < min_dist_squared:
                    min_dist_squared = new_dist_squared
                    min_point = (next_x, next_y)
                    min_deltax = deltax
                    min_deltay = deltay
                    min_dist = math.sqrt(min_dist_squared)
                index -= 1
            # check right side
            while start_index < len(self.sorted_points):
                next_x, next_y = self.sorted_points[start_index]
                deltax = abs(next_x - query_x)
                # if the x distance alone rules out a point, no other points on this side could work
                if deltax > min_dist:
                    break
                deltay = abs(next_y - query_y)
                new_dist_squared = deltax * deltax + deltay * deltay
                if new_dist_squared < min_dist_squared:
                    min_dist_squared = new_dist_squared
                    min_point = (next_x, next_y)
                    min_deltax = deltax
                    min_deltay = deltay
                    min_dist = math.sqrt(min_dist_squared)
                start_index += 1

        return min_point
    
    def selection_sort(self):
        """
        selection_sort performs a selection sort on the points based on their x coordinate.
        Not in place, not particularly fast but indexing time is not measured. 
        """
        sorted_points = self.points.copy()
        for i in range(len(sorted_points)):
            min = None
            min_index = None
            for j in range(i, len(sorted_points)):
                if (min is None or sorted_points[j][0] < min[0]):
                    min = sorted_points[j]
                    min_index = j
            temp = sorted_points[i]
            sorted_points[i] = min
            sorted_points[min_index] = temp

        return sorted_points

    def find_nearest(self, query_point):
        """
        find_nearest finds the nearest point to query_point using the find_nearest_sorted algorithm
        """

        return self.find_nearest_sorted(query_point)
