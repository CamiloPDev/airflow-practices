from airflow.sdk import asset, Asset, Context
import requests

@asset(
    name="user",
    schedule="@daily",
    uri="https://randomuser.me/api/",
)
def user(self) -> dict[str]:
    req = requests.get(self.uri)
    return req.json()

@asset.multi(
    schedule=user,
    outlets=[
        Asset(name="user_location"),
        Asset(name="user_login")
    ]
)
def user_info(user: Asset, context: Context) -> list[dict[str]]:
    user_data = context['ti'].xcom_pull(
        dag_id=user.name,
        task_ids=user.name,
        include_prior_dates=True
    )
    return [
        user_data['results'][0]['location'],
        user_data['results'][0]['login']
    ]

# @asset(
#     name="user_location",
#     schedule=user
# )
# def user_location(user: Asset, context: Context) -> dict[str]:
#     user_data = context['ti'].xcom_pull(
#         dag_id=user.name,
#         task_ids=user.name,
#         include_prior_dates=True
#     )

#     return user_data['results'][0]['location']

# @asset(
#     name="user_login",
#     schedule=user
# )
# def user_login(user: Asset, context: Context) -> dict[str]:
#     user_data = context['ti'].xcom_pull(
#         dag_id=user.name,
#         task_ids=user.name,
#         include_prior_dates=True
#     )

#     return user_data['results'][0]['login']