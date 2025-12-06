from airflow.sdk import dag, task
from typing import Dict

@dag
def xcom_dag():

    @task
    def t1() -> Dict[str, int]:
        number = 12
        sentence = "hello"
        return {
            "number": number,
            "sentence": sentence
        }
    
    @task
    def t2(data: Dict[str, int]) -> None:
        print(f"Received number: {data['number']}")
        print(f"Received sentence: {data['sentence']}")

    data = t1()
    t2(data)

xcom_dag()