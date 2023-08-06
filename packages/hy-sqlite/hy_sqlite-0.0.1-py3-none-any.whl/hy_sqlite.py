import sqlite3

class DataBase:
    def __init__(self, DbName=None):
       self.DbName=DbName

    def createDb(self):
        return  sqlite3.connect(self.DbName)
        print("Creation db ressit")

    def createTable(self,TabName=None,Fields=None):

       db= self.createDb()
       db.execute(
             "CREATE TABLE IF NOT EXISTS "+TabName+"("+Fields+");"
       )
       print("Creation table ressit")

    def insert(self,TabName=None,Fields=None,Values=None,Value=None):
        db=self.createDb()
        donne=Value
        req="INSERT INTO "+TabName+"("+Fields+") VALUES(" +Values+ ")"
        try:
         db.execute(req,donne)
        except ValueError:
            print(ValueError)
        db.commit()
        print("Insertion reussit")
        db.close()

    def delete(self,TabName=None,Id=None,Value=None):
        db=self.createDb()
        req="DELETE FROM "+TabName+" WHERE "+Id+"="+Value+""
        db.execute(req)
        db.commit()
        print("Supression reussit")
        db.close()





