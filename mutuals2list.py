#!/usr/bin/env python3

from mastodon import Mastodon
from mastodon.errors import MastodonIllegalArgumentError
import os

CLIENT_ID = 'mutuals2list'
CLIENT_ID_path = CLIENT_ID+'_clientcred.secret'

def create_client_secret():
    if not os.path.exists("./"+CLIENT_ID):
        try:
            Mastodon.create_app(CLIENT_ID,
                                api_base_url=MASTODON_API_URL,
                                to_file=CLIENT_ID_path)
        except:
            print('could not create client ID')
            exit(1)

def login():
    m = Mastodon(client_id=CLIENT_ID_path)
    try:
        m.log_in(
            USERNAME,
            PASSWORD)
    except MastodonIllegalArgumentError:
        print('Wrong username or password!')
        exit(1)
    except:
        print('Something went wrong!')
    print('login successful')
    return m

def follow_mutulals(client, mutuals):
    lists = client.lists()
    mutuals_list = next(x for x in lists if x['title'] == 'mutuals')
    if mutuals_list is None:
        mutuals_list = client.list_create('mutuals')
    old_mutuals = [x['id'] for x in client.list_accounts(mutuals_list['id'])]
    new_mutuals = [set(mutuals) - set(old_mutuals)]
    client.list_accounts_add(mutuals_list['id'], new_mutuals)
    print('added mutuals to list')


try:
    MASTODON_API_URL = os.environ['MASTODON_API_URL']
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
except:
    print('could not read necessary environment variables')

create_client_secret()
client = login()
client_id = client.me()['id']
follower_ids = [follower['id'] for follower
                in client.account_followers(client_id)]
following_ids = [following['id'] for following
                 in client.account_following(client_id)]
mutuals = list(set(follower_ids) & set(following_ids))
follow_mutulals(client, mutuals)
