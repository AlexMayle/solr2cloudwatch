import requests

from solr_metric_service.solr_metric_service import SolrMetricService
from metric_processors.metric_processors import MetricProcessor
from exporters.cloudwatch_agent import CloudWatchAgentExporter

SOLR_ADMIN_ENDPOINT = "http://localhost:8983/solr"
BASE_SOLR_ENDPOINT = "http://localhost:8983"

def solr_is_running(endpoint):
    resp = requests.get(endpoint)
    assert resp.status_code == 200 

def successful_response_from_metric_api(sms):
    resp = sms.get_query_latency_metrics()
    print(resp)
    return resp

def successful_shard_and_rep_agg(mp, metric_data):
    resp = mp.process_latency_metrics(metric_data)
    print(resp)
    return resp

def successful_send_metric_to_cw(cwx, data, data_type):
    cwx.publish(data, data_type)


def run_tests():
    solr_is_running(SOLR_ADMIN_ENDPOINT)

    sms = SolrMetricService(BASE_SOLR_ENDPOINT)
    metrics = successful_response_from_metric_api(sms)

    mp = MetricProcessor()
    metrics = successful_shard_and_rep_agg(mp, metrics)

    cwx = CloudWatchAgentExporter()
    successful_send_metric_to_cw(cwx, metrics, "gauge")
    
