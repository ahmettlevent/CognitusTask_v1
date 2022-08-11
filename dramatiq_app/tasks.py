import dramatiq

@dramatiq.actor(actor_name="hello_user")
def hello_user(user_name: str):
    res =  f"Hello {user_name}"
    print(res)
    return res








