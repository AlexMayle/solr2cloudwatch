import requests

from solr_metric_service.solr_metric_service import SolrMetricService
from metric_processors.metric_processors import MetricProcessor
from exporters.cloudwatch_agent import CloudWatchAgentExporter

SOLR_ADMIN_ENDPOINT = "http://localhost:8983/solr"
BASE_SOLR_ENDPOINT = "http://localhost:8983"

def solr_is_running(endpoint):
    resp = requests.get(endpoint)
    assert resp.status_code == 200 

def successful_get_latency_metrics(sms):
    resp = sms.get_query_latency_metrics()
    print(resp)
    return resp

def successful_latency_shard_and_rep_agg(mp, metric_data):
    resp = mp.process_latency_metrics(metric_data)
    print(resp)
    return resp

def successful_send_metric_to_cw(cwx, data, data_type):
    cwx.publish(data, data_type)

def successful_get_memory_metrics(sms):
    resp = sms.get_memory_metrics()
    print(resp)
    return resp

def successful_process_mem_memtrics(mp, metrics):
    resp = mp.process_memory_metrics(metrics)
    print(resp)
    return resp


def run_tests(base_host):
    solr_admin_endpoint = base_host + "/solr"
    solr_is_running(solr_admin_endpoint)

    # Latency metrics
    sms = SolrMetricService(base_host)
    metrics = successful_get_latency_metrics(sms)

    mp = MetricProcessor()
    metrics = successful_latency_shard_and_rep_agg(mp, metrics)

    cwx = CloudWatchAgentExporter()
    successful_send_metric_to_cw(cwx, metrics, "gauge")
    

    # Memory metrics
    metrics = successful_get_memory_metrics(sms)
    metrics = successful_process_mem_memtrics(mp, metrics)
    successful_send_metric_to_cw(cwx, metrics, "guage")
