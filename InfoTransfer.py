import pymysql.cursors
import wxpy


bot = wxpy.Bot()

gs = bot.groups()
g_info = []
for g in gs:
    g_info.append(g.name)

for i in range(len(g_info)):
    print("%d、%s" % (i, g_info[i]))

# 读取要记录的群
i = input("输入群的序号\n")
g = gs[int(i)]
g.update_group(True)
gms = g.members
print("本群的概况如下：")
print(gms.stats_text())

# 读取信息并将他们记录在一个字典里
gmt = {}
for gm in gms:
    sex = ''
    if gm.sex == 1:
        sex = "男性"
    elif gm.sex == 2:
        sex = "女性"
    gmt[gm.name] = (sex, gm.city, gm.province)

# Connect to the database

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='guoup_info',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `horticulture_grp` (`name`, `sex`, `city`, `province`) VALUES (%s, %s, %s, %s)"
        for name, info in gmt.items():
            sex = info[0]
            city = info[1]
            province = info[2]
            cursor.execute(sql, (name, sex, city, province))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    # with connection.cursor() as cursor:
    #     # Read a single record
    #     sql = "SELECT `email`, `password` FROM `users` WHERE `email`=%s"
    #     cursor.execute(sql, ('webmaster@python.org'))
    #     result = cursor.fetchone()
    #     print(result)
finally:
    connection.close()
