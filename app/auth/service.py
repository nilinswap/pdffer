from appmigrations.models import ApiToken

def verify(api_key: str):
    ## TODO: Implement a get_or_404
    api_token_list = ApiToken.objects.filter(api_key = api_key)
    n =  len(api_token_list)
    if not n:
        return None
    elif n == 1:
        return api_token_list[0].client.id
    else:
        return Exception(f'api_token_list has more elements than 1!! {n}')
