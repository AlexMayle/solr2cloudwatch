import requests
import json

METRIC_API_PATH = "/solr/admin/metrics"

DEFAULT_OUTPUT_FORMAT = "json"

class SolrMetricService:

    def __init__(self, base_endpoint):
        self._endpoint = self._construct_metric_endpoint(base_endpoint)

    def get_query_latency_metrics(self):
        return self._make_metric_api_call(group="core",
                                          regex="QUERY\./select.*Times")

    def _construct_metric_endpoint(self, base_endpoint):
        base_endpoint = base_endpoint.rstrip('/')
        metric_endpoint = base_endpoint + METRIC_API_PATH
        return metric_endpoint

    def _make_metric_api_call(self,
                              group = None,
                              regex = None,
                              _property = None,
                              prefix = None,
                              _type = None,
                              _format = None):
        
        if _format is None:
            _format = DEFAULT_OUTPUT_FORMAT

        params = {
            "group": group,
            "regex": regex,
            "property": _property,
            "prefix": prefix,
            "type": _type,
            "wt": _format
        }
        params = {k: v for k, v in params.items() if v is not None}

        try:
            resp = requests.get(self._endpoint, params=params)
        except Exception as e:
            msg = "Error while sending request to Metric API"
            raise Exception(msg) from e

        if resp.status_code != 200:
            msg = "Status code does not imply success. Code: %d"
            raise Exception(msg)

        try:
            parsed_resp = json.loads(resp.text)
        except Exception as e:
            msg = "Couldn't parse metric API response. Response: %s"
            msg = msg % (resp.text)
            raise Exception(msg) from e

        metrics = parsed_resp["metrics"]
           
        return metrics


