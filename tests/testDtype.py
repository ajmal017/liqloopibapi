from liqloopibapi.datatype import sqlcnx
from liqloopibapi.datatype import contractArray

myAccountDB = sqlcnx()
myAccountDB.host = 'hallo'

print(myAccountDB.host)
print(myAccountDB)

conArr = contractArray()
print(conArr.sqlhead)
print(conArr.df)
