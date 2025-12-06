from airflow.sdk import dag, task, task_group

@dag
def group():
    @task
    def a():
        return 42

    @task_group
    def my_task_group(value: int):
        @task
        def b(value: int):
            print("value:", value + 1)

        @task_group(
            default_args={
                "retries": 3
            }
        )
        def nested_task_group():

            @task
            def c():
                print("Task C")

            c()

        b(value) >> nested_task_group()

    my_task_group(a())

group()