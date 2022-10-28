from redis import Redis

config={
    'host':'10.8.120.5',
    'port':6379,
    'db':'9',
    'password':'hongye891212',
    'decode_responses':True,




}

rd_client=Redis(**config)

