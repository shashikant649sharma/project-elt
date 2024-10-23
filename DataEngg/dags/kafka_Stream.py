from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 9, 19, 10, 00, 00),
}


def get_data():
    import requests
    
    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]
    return res


def fromate_data(res):
    data = {}
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(res['location']['street']['number'])} {res['location']['street']['name']}, " \
                    f"{res['location']['city']}, {res['location']['state']}, {res['location']['country']}"
    data['postcode'] = res['location']['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']



def stream_data():
    import json
    res = get_data()
    res = fromate_data(res)
    print(json.dumps(res, indent=3))


# with DAG('user_automation',
#          default_args=default_args,
#             schedule='@daily',
#             catchup=False) as dag:
    
#     streaming_task = PythonOperator(
#         task_id='stream_data_from_api',
#         python_callable=stream_data,
#     )
stream_data()