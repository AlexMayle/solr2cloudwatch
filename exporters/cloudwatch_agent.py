import statsd

class CloudWatchAgentExporter:

    def __init__(self,
                 prefix=None,
                 host="localhost",
                 port=8125):
        
        self._client = statsd.StatsClient(host=host,
                                          port=port,
                                          prefix=prefix)

    def publish(self, data_dict, data_type):
        return self._publish_rec_helper(data_dict, [], data_type)

    def _resolve_metric_name(self, dimensions):
        return '.'.join(dimensions)

    def _send_to_cw_agent(self, data, dimensions, data_type):
        name = self._resolve_metric_name(dimensions)
        self._client.gauge(name, data)
        

    def _publish_rec_helper(self,
                            working_dim,
                            dimensions,
                            data_type):

        if not isinstance(working_dim, dict):
            data = working_dim
            self._send_to_cw_agent(data,
                                   dimensions,
                                   data_type)
            return

        for key in working_dim:
            self._publish_rec_helper(working_dim[key],
                                     dimensions + [key],
                                     data_type)

            

