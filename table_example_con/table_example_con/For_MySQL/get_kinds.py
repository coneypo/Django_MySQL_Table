import MySQLdb

db = MySQLdb.connect("localhost", "root", "intel@123", "ithome_news", charset='utf8')
cursor = db.cursor()


sql_cmd = "select * from news;"
sql_cmd = "select category, count(*) from news group by category"
cursor.execute(sql_cmd)

resp = cursor.fetchall()
print(resp)

kind_list=[]
for kind in range(len(resp)):
    print(resp[kind])
    print(resp[kind][0])
    kind_list.append(resp[kind][0])

print(kind_list)