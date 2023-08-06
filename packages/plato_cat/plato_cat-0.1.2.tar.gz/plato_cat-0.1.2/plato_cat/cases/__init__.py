import sys
import time


def get_resource(API, action, payload, result_set, max_length=400):
    """
    get max 400 length resources. that is 20 http requests round.
    """
    resources = []

    payload = payload or {}
    payload['limit'] = 20
    payload['offset'] = 0

    total = -1

    while True:
        payload['offset'] = len(resources)

        result = API.conn.call(action, payload)

        if total != result['total'] and total != -1:
            # total change. reset resources and start over.
            resources = []
            total = result['total']
            continue

        if total == -1:
            total = result['total']

        resources += result[result_set]

        if result['total'] <= len(resources):
            # have find all.
            break

        if len(resources) > max_length:
            # have reach max.
            break

    return resources


def wait_busy_resource(API, action, busy_payload, sleep, timeout=60*5):
    """
    describe busy resources, if total is not 0, means they are still busy,
    wait 4 seconds and try next time.
    """
    while True:
        result = API.conn.call(action, busy_payload)
        if result['total'] == 0:
            # no busy resource. good.
            break

        sleep(4)


def post_resource(API, action, resources, ids_key):
    """
    post max 400 resources. that is 20 http requests round.
    """
    resources = resources[0:400]

    while resources:
        payload = {}
        payload[ids_key] = resources[:20]

        API.conn.call(action, payload)

        resources = resources[20:]


def wait_for_job(API, job_id, sleep, timeout=60*4):
    """
    wait a job for at most 4 minutes.
    """
    if not timeout:
        timeout = sys.maxint

    start = time.time()

    while True:
        job_set = API.conn.call('DescribeJobs', {
            'jobIds': [job_id]
        })['jobSet']

        if len(job_set) == 0:
            sleep(2)
            continue

        job = job_set[0]

        if job['status'] == 'finished':
            break

        sleep(4)

        if time.time() - start > timeout:
            raise Exception('wait_for_job timeout.')
