from libs import rd_client


QBUY_KEY='qbuy_active' #hash

def is_qbuyable():
    #返回 一个 布尔值(是否已经抢过5次)
    return rd_client.hlen(QBUY_KEY) <5

def exits_qbuy(user_id):
    #验证是否已抢购
    return rd_client.hexists(QBUY_KEY,user_id)



def add_qbuy(user_id,goods_id):
    #添加抢购成功记录到 redis

    rd_client.hset(QBUY_KEY,user_id,goods_id)


def get_qbuy(user_id):
    return rd_client.hget(QBUY_KEY,user_id)

#
if __name__ == '__main__':
#     add_qbuy('17074292031','352')
#     print(get_qbuy('17074292031'))
     print(exits_qbuy('17074292031'))