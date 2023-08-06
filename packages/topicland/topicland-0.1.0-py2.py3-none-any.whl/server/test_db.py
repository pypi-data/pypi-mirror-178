import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='wawa316',
                             database='cyberpunk_edgerunner',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `nodes` (`name`, `display_name`) VALUES (%s, %s)"
        #cursor.execute(sql, ('a', 'aa'))
        cursor.executemany(sql, [('a1', 'aa1'), ("a2", "aa2")])

    connection.commit()

