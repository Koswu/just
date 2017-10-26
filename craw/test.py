import pymysql


def get_detail():
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='935377012',
        db='test',
        charset='utf8'
    )
    cur = connect.cursor()
    data = cur.execute("SELECT * FROM jidian")
    rs = cur.fetchall()  # 获得剩下的所有结果
    item_name = []  #
    data_list = []
    kaocha_list = []
    bixiu_list = []
    for name in cur.description:
        item_name.append(name[0])
    for item in rs:
        data = {}
        for i in range(14):
            data[item_name[i]] = item[i]
        if ("考查" in data.values()):
            kaocha_list.append(data)
        else:
            bixiu_list.append(data)
        data_list.append(data)
    return data_list

