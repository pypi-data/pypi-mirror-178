# 项目介绍

pymongo连接池

# 作者资料

昵称: jutooy

邮箱: jutooy@qq.com

# 语法

    from pymongo import MongoClient
    from coolmongo import coolmongo


    # 创建连接池
    mkconn = lambda: MongoClient(host='localhost', port=27017)
    monPool = coolmongo(mkconn)

    # 从连接池取出1个连接
    conn = monPool.get()

    # 添加1条数据
    conn['TestcoolmongoDB']['TestcoolmongoSheet'].insert_one({'A':'AAA'})

    # 把连接归还到连接池
    monPool.append(conn)
