from liqloopibapi.datatype import sqlcnx

myAccountDB = sqlcnx()
myAccountDB.host = 'hallo'

print(myAccountDB.host)
print(myAccountDB)
