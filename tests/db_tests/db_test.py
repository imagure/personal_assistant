from Crypto.Cipher import DES

from db.sql.db_interface import DbInterface

des = DES.new('01234567', DES.MODE_ECB)
db_interface = DbInterface()

team_id = "THGD0P2GN"
token = bytes(db_interface.search_slack_workspace(team_id))
print("Token=", token)
token = des.decrypt(token)
token = token[0:-4].decode('utf-8')
print("token here: ", token)
