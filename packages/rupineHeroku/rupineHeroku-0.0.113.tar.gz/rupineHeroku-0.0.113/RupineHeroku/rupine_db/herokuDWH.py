from RupineHeroku.rupine_db import herokuDbAccess
from psycopg2 import sql
from datetime import datetime
import pytz

def getUniqueTokenFromTransactions(connection, schema, public_address:str=None, chain_id:int=None):
    
    queryStrSend = "select distinct(amount_send_dwh_token_id) \
        FROM {}.dwh_transaction \
        WHERE amount_send_dwh_token_id is not NULL"

    queryStrRecv = "select distinct(amount_recv_dwh_token_id) \
        FROM {}.dwh_transaction \
        WHERE amount_recv_dwh_token_id is not NULL"

    params = []

    if chain_id:
        queryStrSend = queryStrSend + " AND chain_id=%s"
        queryStrRecv = queryStrRecv + " AND chain_id=%s"
        params.append(chain_id)

    if public_address:
        queryStrSend = queryStrSend + " AND public_address=%s"
        queryStrRecv = queryStrRecv + " AND public_address=%s"
        params.append(public_address)

    querySend = sql.SQL(queryStrSend).format(sql.Identifier(schema))
    queryRecv = sql.SQL(queryStrRecv).format(sql.Identifier(schema))

    resultSend = herokuDbAccess.fetchDataInDatabase(querySend, params, connection)    
    resultRecv = herokuDbAccess.fetchDataInDatabase(queryRecv, params, connection)    

    allResults = [*resultSend, *resultRecv]

    return allResults

def getUniqueAddress(connection, schema, chain_id:int=None):
    
    queryStr = "select distinct(public_address) id, public_address \
        FROM {}.dwh_address_account"

    params = []

    if chain_id:
        queryStr = queryStr + " WHERE chain_id=%s"
        params.append(chain_id)

    query = sql.SQL(queryStr).format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, params, connection)    
    return result

def getLatestTx(connection, schema, public_address, min_timestamp):
    
    queryStr = "SELECT tx_timestamp, tx_from, amount_fee_value, amount_fee_dwh_token_id,  \
                        amount_send_value, amount_send_dwh_token_id, \
                        amount_recv_value, amount_recv_dwh_token_id  \
                FROM {}.dwh_transaction \
                WHERE public_address = %s AND tx_timestamp > %s \
                ORDER BY tx_timestamp DESC"
  
    query = sql.SQL(queryStr).format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [public_address, min_timestamp], connection) 
    return result

def getTxSortedAsc(connection, schema, public_address_list):

    queryStr = "SELECT id, tx_hash, tx_failed, tx_type_no, tx_timestamp, tx_from, \
                        amount_fee_value, amount_fee_value_USD, amount_fee_dwh_token_id,  \
                        amount_send_value, amount_send_value_USD, amount_send_dwh_token_id, \
                        amount_recv_value, amount_recv_value_USD, amount_recv_dwh_token_id, \
                        chain_id, tx_to, created_at, modified_at \
                FROM {}.dwh_transaction \
                WHERE public_address IN " + public_address_list + " \
                ORDER BY tx_timestamp ASC"

    query = sql.SQL(queryStr).format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [], connection) 

    retData = []
    
    for tx in result:
        data = {
            'tx_id': tx[0]
            , 'tx_hash': tx[1]
            , 'tx_failed': tx[2]
            , 'tx_type_no': tx[3]
            , 'tx_datetime': tx[4]
            , 'tx_from': tx[5]
            , 'tx_fee_amount': tx[6]
            , 'tx_fee_amount_usd': tx[7]
            , 'tx_fee_token_id': tx[8]
            , 'tx_send_amount': tx[9]
            , 'tx_send_amount_usd': tx[10]
            , 'tx_send_token_id': tx[11]
            , 'tx_recv_amount': tx[12]
            , 'tx_recv_amount_usd': tx[13]
            , 'tx_recv_token_id': tx[14]
            , 'chain_id': tx[15]
            , 'tx_to': tx[16]
            , 'created_at': tx[17]
            , 'modified_at': tx[18]
        }
        retData.append(data.copy())

    return retData