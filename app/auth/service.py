from appmigrations.models import Client

def verify(api_key: str):
    ## TODO: Implement a get_or_404 https://docs.djangoproject.com/en/dev/topics/db/managers/
    api_token_list = Client.objects.filter(api_key = api_key)
    n =  len(api_token_list)
    if not n:
        return None
    elif n == 1:
        return api_token_list[0].id
    else:
        return Exception(f'api_token_list has more elements than 1!! {n}')
