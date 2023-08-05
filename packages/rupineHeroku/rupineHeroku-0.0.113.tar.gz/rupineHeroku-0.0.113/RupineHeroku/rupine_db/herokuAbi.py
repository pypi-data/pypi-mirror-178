from RupineHeroku.rupine_db import herokuDbAccess
from psycopg2 import sql

def getAbi(connection, schema, token_address, chain_id):
    
    #NOTE: ABI not in DB for now (Sept. 2022)
    return None

    query = sql.SQL("SELECT abi FROM {}.evm_token \
           WHERE chain_id = %s AND token_address = %s").format(sql.Identifier(schema))
           
    params = (chain_id, token_address)
    
    result = herokuDbAccess.fetchDataInDatabase(query, params, connection)
    if len(result) == 0:
           return None
           
    return result[0][0]

def updateAbi(connection, schema, abi, token_address, chain_id):
    
    #NOTE: ABI not in DB for now (Sept. 2022)
    return None
    
    query = sql.SQL("UPDATE {}.evm_token \
           SET abi=%s \
           WHERE chain_id = %s AND token_address = %s").format(sql.Identifier(schema))
           
    params = (abi, chain_id, token_address)
    
    herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    