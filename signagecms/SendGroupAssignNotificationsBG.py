from django.db import connection

query = "SELECT * FROM group_groupmemberassignnotification LIMIT 100";
with connection.cursor() as cursor:
    cursor.execute(query);
    values = cursor.fetchall();
print(query);
