import datetime
import json

import requests

def __get_request(url:str):
    print(url)
    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"Failed to execute GET against {url} (Error: {error})")
    else:
        if not 200 <= int(response.status_code) < 300:
            raise ConnectionError(f"Failed to execute GET against {url} (Network Code: {response.status_code})")
    return response.json()


def get_node_status()->(dict, dict):
    """
    :sample data:
    {
      "configuration": {
        "exchange_api": "http://192.168.56.10:3090/v1/",
        "exchange_version": "2.126.1",
        "required_minimum_exchange_version": "2.90.1",
        "preferred_exchange_version": "2.110.1",
        "mms_api": "http://192.168.56.10:9443",
        "architecture": "amd64",
        "horizon_version": "2.31.0-1657"
      },
      "liveHealth": null
    }
    :sample output:
    {
        "timestamp": "2025-01-01 00:00:00",
        "exchange_api": "http://192.168.56.10:3090/v1/",
        "exchange_version": "2.126.1",
        "required_minimum_exchange_version": "2.90.1",
        "preferred_exchange_version": "2.110.1",
        "mms_api": "http://192.168.56.10:9443",
        "architecture": "amd64",
        "horizon_version": "2.31.0-1657"
    }

    {
        "timestamp": "2025-01-01 00:00:00",
        "exchange_api": "http://192.168.56.10:3090/v1/",
        "status" : "Ok"
    }
    """
    url = 'http://localhost:8510/status'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    node_status = {'timestamp': timestamp}
    node_info = {'timestamp': timestamp}

    output = __get_request(url)
    if 'configuration' in output:
        node_info = {'timestamp': timestamp, **output['configuration']}
        node_status['exchange_api'] = output['configuration']['exchange_api']
    if 'liveHealth' in output and output['liveHealth'] is not None:
        node_status['status'] = output['liveHealth']
    elif 'liveHealth' in output:
        node_status['status'] = 'OK'

    return node_status, node_info


def get_event_log(last_timestamp:int=None)->(list, int):
    """
    :sample data:
    {
        "record_id": "26",
        "timestamp": 1747941803,
        "severity": "info",
        "message": "Workload service containers for myorg/service-edgelake-operator are up and running.",
        "event_code": "container_running",
        "source_type": "agreement",
        "event_source": {
          "agreement_id": "bd9cd93249975585047e10e9b82d0ef6aae4fc25f7d21ec0f576e5cf3d8d3c11",
          "workload_to_run": {
            "url": "service-edgelake-operator",
            "org": "myorg",
            "version": "1.3.5",
            "arch": "amd64"
          },
          "dependent_services": [],
          "consumer_id": "IBM/agbot",
          "agreement_protocol": "Basic"
    }
    :sample output:
    {
        "record_id": "26",
        "timestamp": 1747941803,
        "severity": "info",
        "message": "Workload service containers for myorg/service-edgelake-operator are up and running.",
        "event_code": "container_running",
        "source_type": "agreement",
        "agreement_id": "bd9cd93249975585047e10e9b82d0ef6aae4fc25f7d21ec0f576e5cf3d8d3c11",
        "url": "service-edgelake-operator",
        "org": "myorg",
        "dependent_services": [],
        "consumer_id": "IBM/agbot",
        "agreement_protocol": "Basic"
    }
    """
    payloads = []
    url = 'http://localhost:8510/eventlog'
    output = __get_request(url)
    for row in output:
        payload = {}
        if last_timestamp is None or row['timestamp'] > last_timestamp:
            for key in row:
                if key == 'record_id':
                    payload[key] = int(row[key])
                elif key == 'timestamp':
                    payload[key] = datetime.datetime.fromtimestamp(row[key]).strftime('%Y-%m-%d %H:%M:%S')
                    last_timestamp = row['timestamp']
                elif key == 'event_source':
                    if 'workload_to_run' in row[key]:
                        for event_key in ['org', 'url']:
                            if event_key in row[key]['workload_to_run']:
                                payload[event_key] = row[key]['workload_to_run'][event_key]
                else:
                    payload[key] = row[key]
            payloads.append(payload)

    return  payloads, last_timestamp



print(json.dumps(get_node_status(), indent=2))
print(json.dumps(get_event_log(), indent=2))