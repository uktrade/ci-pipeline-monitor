import environ
from flask import Flask
import requests
import json
from datetime import timedelta

application = Flask(__name__)

env = environ.Env()
application.config["CONSUL_API"] = env('CONSUL_API', default='http://consul:8500/')
application.config["VAULT_API"] = env('VAULT_API', default='http://vault:8200/')
application.config["JENKINS_URL"] = env('JENKINS_URL', default='http://jenkins:8080/')

@application.route("/")
def status():
    service_degraded = 0
    totaltime = timedelta()

    try:
        consul_status = requests.get(application.config["CONSUL_API"] + '/v1/status/leader')
        consul_status.close()
        totaltime += consul_status.elapsed
        if consul_status.status_code != 200:
            raise ApiError('GET /v1/status/leader {}'.format(consul_status.status_code))
            service_degraded += 1
    except requests.exceptions.RequestException as e:
        print(e)
        service_degraded += 1

    try:
        vault_status = requests.get(application.config["VAULT_API"] + '/v1/sys/health')
        vault_status.close()
        totaltime += vault_status.elapsed
        if vault_status.status_code != 200:
            raise ApiError('GET /v1/sys/health {}'.format(vault_status.status_code))
            service_degraded += 1
    except requests.exceptions.RequestException as e:
        print(e)
        service_degraded += 1

    try:
        jenksin_status = requests.get(application.config["JENKINS_URL"])
        jenksin_status.close()
        totaltime += jenksin_status.elapsed
        if jenksin_status.status_code != 200:
            raise ApiError('GET / {}'.format(jenksin_status.status_code))
            service_degraded += 1
    except requests.exceptions.RequestException as e:
        print(e)
        service_degraded += 1

    if service_degraded == 0:
        return('<pingdom_http_custom_check><status>OK</status><response_time>' + str(totaltime.total_seconds()) + '</response_time></pingdom_http_custom_check>')
    elif service_degraded == 3:
        return('<pingdom_http_custom_check><status>DOWN</status><response_time>' + str(totaltime.total_seconds()) + '</response_time></pingdom_http_custom_check>')
    elif service_degraded < 3:
        return('<pingdom_http_custom_check><status>DEGRADED</status><response_time>' + str(totaltime.total_seconds()) + '</response_time></pingdom_http_custom_check>')


if __name__ == "__main__":
    application.run(host='0.0.0.0')
