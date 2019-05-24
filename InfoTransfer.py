import pymysql.cursors
import wxpy

# 登陆微信
bot = wxpy.Bot()

# 获取群列表
groups = bot.groups()
groups_info = [group.name for group in groups]

# 输出群列表
for i, each_group in enumerate(groups_info):
    print("%d、%s" % (i, each_group))

# 读取要记录的群
i = input("输入群的序号\n")
group = groups[int(i)]

print("稍等片刻，正在获取成员信息")
# 更新群信息，打印输出群概况
group.update_group(True)
group_members = group.members
print("本群的概况如下：")
print(group_members.stats_text())

# 读取信息并将他们记录在一个字典里
group_members_dit = {}
for group_member in group_members:
    sex = ''
    if group_member.sex == 1:
        sex = "男性"
    elif group_member.sex == 2:
        sex = "女性"
    group_members_dit[group_member.name] = (sex, group_member.city, group_member.province)

# Connect to the database

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='group_info',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    with connection.cursor() as cursor:
        print("正在创建数据表")
        # 创建数据表named group's name
        group_name = "`{0}`".format(group.name)
        sql = "CREATE TABLE IF NOT EXISTS {0} (name VARCHAR(255),sex TEXT,city TEXT,province TEXT)".format(group_name)
        cursor.execute(sql)

        # 配置表，使emoji表情可以存入
        sql = "alter table {0} convert to character set utf8mb4 collate utf8mb4_bin".format(group_name)
        cursor.execute(sql)

        print("正在录入数据")
        # 录入数据
        sql = "INSERT INTO {0} (`name`, `sex`, `city`, `province`) VALUES (%s, %s, %s, %s)".format(group_name)
        for name, info in group_members_dit.items():
            sex = info[0]
            city = info[1]
            province = info[2]
            cursor.execute(sql, (name, sex, city, province))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

finally:
    connection.close()
    bot.logout()
    print("程序结束")

