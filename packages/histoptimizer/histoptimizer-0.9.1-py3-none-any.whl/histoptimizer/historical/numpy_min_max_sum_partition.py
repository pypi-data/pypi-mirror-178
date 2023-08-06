import numpy
from histoptimizer import Histoptimizer

class NumpyMinMaxSumOptimizer(Histoptimizer):
    name = 'numpy_min_max_sum'

    @classmethod
    def build_matrices(cls, buckets, prefix_sum):
        n = len(prefix_sum)
        min_cost = numpy.zeros((n, buckets + 1), dtype=numpy.float32)
        divider_location = numpy.zeros((n, buckets + 1), dtype=numpy.int32)

        for item in range(1, len(prefix_sum)):
            # min_cost[item, 1] = prefix_sum[item]
            min_cost[item, 1] = prefix_sum[item]
        for bucket in range(1, buckets + 1):
            min_cost[1, bucket] = prefix_sum[1]
        for item in range(2, len(prefix_sum)):
            # evaluate main recurrence
            for bucket in range(2, buckets + 1):
                min_cost_temp = numpy.finfo(dtype=numpy.float32).max
                divider_location_temp = 0
                for previous_item in range(1, item):
                    # Skiena's original cost function.
                    cost = max(min_cost[previous_item, bucket - 1],
                               prefix_sum[item] - prefix_sum[previous_item])
                    if min_cost_temp > cost:
                        min_cost_temp = cost
                        divider_location_temp = previous_item
                min_cost[item, bucket] = min_cost_temp
                divider_location[item, bucket] = divider_location_temp

        return min_cost, divider_location

    @classmethod
    def partition(cls, items, num_buckets, debug_info=None):
        padded_items = [0]
        padded_items.extend(items)
        items = padded_items
        n = len(items) - 1
        prefix_sum = numpy.zeros((n + 1), dtype=numpy.float32)
        # Cache cumulative sums
        for item in range(1, n + 1):
            prefix_sum[item] = prefix_sum[item - 1] + items[item]

        (min_cost, divider_location) = cls.build_matrices(num_buckets, prefix_sum)

        if debug_info is not None:
            debug_info['items'] = items
            debug_info['prefix_sum'] = prefix_sum
            debug_info['min_cost'] = min_cost
            debug_info['divider_location'] = divider_location

        partition = cls.reconstruct_partition(divider_location, n, num_buckets)
        return partition, min_cost / num_buckets
