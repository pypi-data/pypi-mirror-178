from RupineHeroku.rupine_db import herokuDbAccess
from psycopg2 import sql
from datetime import datetime
import pytz

def postTaxTransaction(connection, schema, data):

    query = sql.SQL("INSERT INTO {}.tax_transaction (tx_no,chain_id,chain,location,location_type,public_address,timestamp,block_number,transaction_hash,interacted_with_contract,category_mapping_id,from_public_address,to_public_address,token,amount,usd_value,eur_value,fee_token,fee_amount,fee_usd_value,fee_eur_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))
    params = (
        data['tx_no'],
        data['chain_id'],
        data['chain'],
        data['location'],
        data['location_type'],
        data['public_address'],
        data['timestamp'],
        data['block_number'],
        data['transaction_hash'],
        data['interacted_with_contract'],
        data['category_mapping_id'],
        data['from_public_address'],
        data['to_public_address'],
        data['token'],
        data['amount'],
        data['usd_value'],
        data['eur_value'],
        data['fee_token'],
        data['fee_amount'],
        data['fee_usd_value'],
        data['fee_eur_value'])
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def getTaxTransactionRewards(connection, schema, addresses:list=None, chain=None, chain_id=None, token:str=None, timestamp:int=0, posNegAll:str='all'):
    '''
    Parameters:
        - address: relevant public keys (optional)
        - chain/chain_id: either choose a specifier (necessary)
        - token: String of Token, e.g. URHT, DUSD-URTH, etc. Default is None
        - timestamp: all data with timestamp gte. Default is 0
        - posNegAll: "positive", "negative" or "all". is Amount gte 0, lt 0 or everything. Default is 'all'
    '''
    conditions = ""
    params = []
    if chain is None and chain_id is None:
        return []
    elif chain is not None:
        conditions = conditions + " AND t.chain = %s"
        params.append(chain)
    elif chain_id is not None:
        conditions = conditions + " AND t.chain_id = %s"
        params.append(chain_id)
    
    if addresses is not None:
        vars = ["%s"]*len(addresses)
        conditions = conditions + " AND t.public_address IN ({})".format(','.join(vars))
        params.extend(addresses)

    if token != None:
        conditions = conditions + " AND t.token = %s"
        params.append(token)
    
    if posNegAll == 'positive':
        conditions = conditions + " AND t.amount >= 0"
    elif posNegAll == 'negative':
        conditions = conditions + " AND t.amount < 0"

    query = sql.SQL("SELECT basis.* FROM ( \
                        SELECT t.id,t.chain_id,t.chain,t.public_address,t.timestamp,t.block_number,t.transaction_hash,t.interacted_with_contract,c.category,t.token,t.amount,t.usd_value,t.eur_value,t.fee_usd_value,t.fee_eur_value, \
                        CASE WHEN c.sort_no IS NULL THEN '999' ELSE c.sort_no END AS sort_no \
                        FROM {0}.tax_transaction t LEFT JOIN {0}.tax_category_mapping cm ON t.category_mapping_id = cm.id \
                        LEFT JOIN {0}.tax_category c ON cm.category_no = c.category_no \
                        WHERE 1=1 AND t.timestamp >= %%s %s \
                            UNION ALL	\
                        SELECT t.id,t.chain_id,t.chain,t.public_address,t.timestamp,NULL AS block_number,NULL AS transaction_hash,NULL AS interacted_with_contract,c.category,t.token,t.amount,t.usd_value,t.eur_value,NULL AS fee_usd_value,NULL AS fee_eur_value, \
                        CASE WHEN c.sort_no IS NULL THEN '999' ELSE c.sort_no END AS sort_no \
                        FROM {0}.tax_reward t LEFT JOIN {0}.tax_category_mapping cm ON t.category_mapping_id = cm.id \
                        LEFT JOIN {0}.tax_category c ON cm.category_no = c.category_no \
                        WHERE 1=1 AND t.timestamp >= %%s %s \
                    ) basis ORDER BY basis.timestamp ASC, basis.sort_no ASC" % (conditions,conditions)).format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [timestamp,*params,timestamp,*params], connection)    
       
    return result

def getTaxTokens(connection, schema, addresses:list=None, chain=None, chain_id=None):
    '''
    Parameters:
        - address: relevant public keys (optional)
        - chain/chain_id: either choose a specifier (necessary)
        - token: String of Token, e.g. URHT, DUSD-URTH, etc. Default is None
        - timestamp: all data with timestamp gte. Default is 0
        - posNegAll: "positive", "negative" or "all". is Amount gte 0, lt 0 or everything. Default is 'all'
    '''
    conditions = ""
    params = []
    if chain is None and chain_id is None:
        return []
    elif chain is not None:
        conditions = conditions + " AND t.chain = %s"
        params.append(chain)
    elif chain_id is not None:
        conditions = conditions + " AND t.chain_id = %s"
        params.append(chain_id)
    
    if addresses is not None:
        vars = ["%s"]*len(addresses)
        conditions = conditions + " AND t.public_address IN ({})".format(','.join(vars))
        params.extend(addresses)

    query = sql.SQL("SELECT DISTINCT t.token from {0}.tax_transaction t \
                    WHERE 1=1 %s \
                    UNION \
                    SELECT DISTINCT t.token from {0}.tax_reward t \
                    WHERE 1=1 %s" % (conditions,conditions)).format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [*params,*params], connection)  
    return result

def getLatestWarehouseTxDate(connection, schema, token:str, account:str, chain=None, chain_id=None):
    conditions = ""
    params = []
    if chain is None and chain_id is None:
        return []
    elif chain is not None:
        conditions = conditions + " AND chain = %s"
        params.append(chain)
    elif chain_id is not None:
        conditions = conditions + " AND chain_id = %s"
        params.append(chain_id)

    query = sql.SQL("SELECT t.timestamp,b.latest_rest_tx_no,b.latest_rest_amount FROM {0}.tax_transaction t RIGHT JOIN ( \
                    SELECT DISTINCT FIRST_VALUE(rest_tx_no) OVER (ORDER BY day DESC) as latest_rest_tx_no,FIRST_VALUE(rest_amount) OVER (ORDER BY day desc) as latest_rest_amount FROM {0}.tax_warehouse WHERE 1=1 AND account = %%s AND token = %%s %s) b \
                    ON b.latest_rest_tx_no = t.tx_no \
                    UNION \
                    SELECT t.timestamp,b.latest_rest_tx_no,b.latest_rest_amount FROM {0}.tax_reward t RIGHT JOIN ( \
                    SELECT DISTINCT FIRST_VALUE(rest_tx_no) OVER (ORDER BY day DESC) as latest_rest_tx_no,FIRST_VALUE(rest_amount) OVER (ORDER BY day desc) as latest_rest_amount FROM {0}.tax_warehouse WHERE 1=1 AND account = %%s AND token = %%s %s) b \
                    ON b.latest_rest_tx_no = t.tx_no" % (conditions,conditions)).format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [account,token,*params,account,token,*params], connection)  
    if len(result) == 0 or result[0][0] is None:
        return (0,None,None)
        #return datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
        
    #d = result[0][0]
    return result[0]
    #return datetime(d.year,d.month,d.day, 0, 0, 0, tzinfo=pytz.timezone('UTC'))

def getLatestTransactionRewardBlock(connection, schema, address:str, chain=None, chain_id=None):
    conditions = ""
    params = []
    if chain is None and chain_id is None:
        return []
    elif chain is not None:
        conditions = conditions + " AND chain = %s"
        params.append(chain)
    elif chain_id is not None:
        conditions = conditions + " AND chain_id = %s"
        params.append(chain_id)

    query = sql.SQL("SELECT 'tax_transaction' AS table, MAX(block_number) as latest_block_number FROM {0}.tax_transaction \
                    WHERE 1=1 AND public_address = %%s %s \
                    UNION ALL \
                    SELECT 'tax_reward' AS table, MAX(latest_block_number) as latest_block_number FROM {0}.tax_reward \
                    WHERE 1=1 AND public_address = %%s %s" % (conditions,conditions)).format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [address,*params,address,*params], connection)  
    return result

def getLatestWarehouseDate(connection, schema, token:str, account:str, chain=None, chain_id=None):
    conditions = ""
    params = []
    if chain is None and chain_id is None:
        return []
    elif chain is not None:
        conditions = conditions + " AND chain = %s"
        params.append(chain)
    elif chain_id is not None:
        conditions = conditions + " AND chain_id = %s"
        params.append(chain_id)

    query = sql.SQL("SELECT MAX(day) as latest_day FROM {0}.tax_warehouse WHERE 1=1 AND account = %%s AND token = %%s %s" % (conditions)).format(sql.Identifier(schema))

    result = herokuDbAccess.fetchDataInDatabase(query, [account,token,*params], connection)  
    if result[0][0] is None:
        return datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
        
    d = result[0][0]
    return datetime(d.year,d.month,d.day, 0, 0, 0, tzinfo=pytz.timezone('UTC'))

def postTaxReward(connection, schema, data):
    query = sql.SQL("INSERT INTO {}.tax_reward (tx_no,chain_id,chain,location,location_type,public_address,timestamp,latest_block_number,category_mapping_id,token,amount,usd_value,eur_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))   
    params = (
        data['tx_no'],
        data['chain_id'],
        data['chain'],
        data['location'],
        data['location_type'],
        data['public_address'],
        data['timestamp'],
        data['latest_block_number'],
        data['category_mapping_id'],
        data['token'],
        data['amount'],
        data['usd_value'],
        data['eur_value']
    )

    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def postTaxWarehouse(connection, schema, data):
    query = sql.SQL("INSERT INTO {}.tax_warehouse (chain_id,chain,account,day,token,amount,amount_usd,amount_eur,amount_in,amount_in_usd,amount_in_eur,amount_out,amount_out_usd,amount_out_eur,profit_amount_usd,profit_amount_eur,fee_amount_usd,fee_amount_eur,rest_tx_no,rest_amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))   
    params = (
        data['chain_id'],
        data['chain'],
        data['account'],
        data['day'],
        data['token'],
        data['amount'],
        data['amount_usd'],
        data['amount_eur'],
        data['amount_in'],
        data['amount_in_usd'],
        data['amount_in_eur'],
        data['amount_out'],
        data['amount_out_usd'],
        data['amount_out_eur'],
        data['profit_amount_usd'],
        data['profit_amount_eur'],
        data['fee_amount_usd'],
        data['fee_amount_eur'],
        data['rest_tx_no'],
        data['rest_amount']
    )

    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def postTaxTrade(connection, schema, data):
    query = sql.SQL("INSERT INTO {}.tax_trades (chain_id,chain,account,address,token,buy_timestamp,buy_price,buy_transaction_hashes,sell_timestamp,sell_price,sell_transaction_hashes,amount,fee_amount_usd,fee_amount_eur) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))   
    params = (
        data['chain_id'],
        data['chain'],
        data['account'],
        data['address'],
        data['token'],
        data['buy_timestamp'],
        data['buy_price'],
        data['buy_transaction_hashes'],
        data['sell_timestamp'],
        data['sell_price'],
        data['sell_transaction_hashes'],
        data['amount'],
        data['fee_amount_usd'],
        data['fee_amount_eur']
    )

    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def postCategoryMapping(connection, schema, category):
    query = sql.SQL("SELECT id FROM {}.tax_category_mapping WHERE category_raw = %s;").format(sql.Identifier(schema))
    params = [category]
    result = herokuDbAccess.fetchDataInDatabase(query, params, connection)  

    if len(result) > 0:
        return result[0][0]

    query = sql.SQL("INSERT INTO {}.tax_category_mapping (category_raw, category_no, is_edited) VALUES (%s,%s,%s) ON CONFLICT (category_raw) DO NOTHING RETURNING id;").format(sql.Identifier(schema))
    params = [category,'-1','N']
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)
    if result is not None:    
        return result[0][0]
    return result

# import os
# from dotenv import load_dotenv
# import herokuDbAccess as db
# from datetime import datetime
# load_dotenv()

# if __name__ == '__main__':
#     connection = db.connect(
#         os.environ.get("HEROKU_DB_USER"),
#         os.environ.get("HEROKU_DB_PW"),
#         os.environ.get("HEROKU_DB_HOST"),
#         os.environ.get("HEROKU_DB_PORT"),
#         os.environ.get("HEROKU_DB_DATABASE")
#      )

#     print(postCategoryMapping(connection,'dbdev','Exit staking wallet'))
#     print(getLatestTransactionRewardBlock(connection,'stage','DFI','df1qgssyvcqld7cwxzvnajyt3xlqae67muxrqh06ct','DeFiChain'))
    # data = {
    #     'chain_id':1,
    #     'chain':'ETH',
    #     'account':'MYACC',
    #     'day':datetime.strptime('2022-12-01','%Y-%m-%d'),
    #     'token':'BLUE1',
    #     'amount':12.2,
    #     'amount_usd':120.1,
    #     'amount_eur':110.23,
    #     'amount_in':1.3,
    #     'amount_in_usd':1.4,
    #     'amount_in_eur':1.5,
    #     'amount_out':1.6,
    #     'amount_out_usd':1.7,
    #     'amount_out_eur':1.8,
    #     'tax_amount_usd':1.9,
    #     'tax_amount_eur':2.0
    # }
    # data = {
    #     'chain_id':1,
    #     'chain':'ETH',
    #     'account':'MYACC',
    #     'address':'dfi1',
    #     'token':'BLUE1',
    #     'buy_timestamp':127897934,
    #     'buy_price':12.4,
    #     'buy_transaction_hashes':'sjdlfjskljdfklsj,jhghjhghj',
    #     'sell_timestamp':893434,
    #     'sell_price':34.35,
    #     'sell_transaction_hashes':'shdsdfjkhsdjkf2,sdjfklj',
    #     'amount':12.2
    # }
    #res = getTaxTransactionRewards(connection,'stage',['dfi1','df1qgssyvcqld7cwxzvnajyt3xlqae67muxrqh06ct'],'DeFiChain',None,'DFI',0)
    #res = getTaxTokens(connection,'stage',['dfi1','df1qgssyvcqld7cwxzvnajyt3xlqae67muxrqh06ct'],'DeFiChain',None)
    # res = getLatestWarehouseDate(connection,'stage','BLUE12','MYACC','Defi',None)
    # print(res)