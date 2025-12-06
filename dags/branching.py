from airflow.sdk import dag, task

@dag
def branching_dag():

    @task
    def a() -> int:
        return 0

    @task.branch
    def b(val: int) -> None:
        if val == 1:
            return "equal_1"
        return "different_than_1"


    @task
    def equal_1(val: int) -> None:
        print(f"Value is equal to {val}")

    @task
    def different_than_1(val: int) -> None:
        print(f"Value is different than 1: {val}")

    val = a()
    b(val) >> [equal_1(val), different_than_1(val)]

branching_dag()