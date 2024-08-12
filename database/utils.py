import pymysql

class DataBaseExecution:
    """MySQL database execution class"""
    def __init__(self, host='localhost', port=9526, user='root', password='root', database='testdb', charset='utf8'):
        self.connection = pymysql.connect(host=host, port=port, database=database, user=user, password=password, charset=charset)
        self.cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
    
    def submit(self):
        self.connection.commit()
    
    def rollback(self):
        self.connection.rollback()
    
    def close(self):     
        self.cursor.close()
        self.connection.close()