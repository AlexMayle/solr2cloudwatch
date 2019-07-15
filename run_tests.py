import argparse

from tests import solr_metric_service_tests

parser = argparse.ArgumentParser("Solr Monitoring Unit Tests")

parser.add_argument('host',
                     type=str,
                     default="localhost:8983",
                     help="Solr base endpoint"
                    )

if __name__ == "__main__":
    args = parser.parse_args()

    solr_metric_service_tests.run_tests(args.host)
