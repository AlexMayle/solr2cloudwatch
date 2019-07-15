

class MetricProcessor:

    def __init__(self):
        pass

    def _aggregate(self, aggregates, new_value, dimensions):
        working_dimension = aggregates
        for i in range(len(dimensions) - 1):
            try:
                maybe_exists = working_dimension[dimensions[i]]
            except KeyError:
                # turns out it doesn't exist
                working_dimension[dimensions[i]] = dict()
            finally:
                # move up one dimension
                working_dimension = \
                        working_dimension[dimensions[i]]

        # We have to stop one before the last dimension because
        # numbers are copied by value and we'll lose our reference
        # to the memory slot
        prev_value = working_dimension.get(dimensions[-1], 0) 
        working_dimension[dimensions[-1]] = prev_value + new_value

    def process_latency_metrics(self, metric_dict):
        aggregates = dict()

        # Filter out unwanted metrics
        for core_name in metric_dict:
            core_metrics = metric_dict[core_name]
            collection_name = core_name.split('.')
            collection_name = collection_name[2]
            for handler_name in core_metrics:
                metric_props = core_metrics[handler_name]
                self._aggregate(aggregates,
                          metric_props["median_ms"],
                          dimensions=[collection_name, handler_name, "median_ms"])
                self._aggregate(aggregates,
                          metric_props["p75_ms"],
                          dimensions=[collection_name, handler_name, "p75_ms"])
                self._aggregate(aggregates,
                          metric_props["p95_ms"],
                          dimensions=[collection_name, handler_name, "p95_ms"])
                self._aggregate(aggregates,
                          metric_props["p99_ms"],
                          dimensions=[collection_name, handler_name, "p99_ms"])

        return aggregates 
                

