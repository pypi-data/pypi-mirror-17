# -*- coding: utf8 -*-

from example_config import *
from ots2 import *
import time

table_name = 'OTSBatchWriteRowSimpleExample'

def create_table(ots_client):
    schema_of_primary_key = [('gid', 'INTEGER'), ('uid', 'INTEGER')]
    table_meta = TableMeta(table_name, schema_of_primary_key)
    reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
    ots_client.create_table(table_meta, reserved_throughput)
    print 'Table has been created.'

def delete_table(ots_client):
    ots_client.delete_table(table_name)
    print 'Table \'%s\' has been deleted.' % table_name

def batch_write_row(ots_client):
    # batch put 10 rows and update 10 rows on exist table, delete 10 rows on a not-exist table.
    put_row_items = []
    for i in range(0, 10):
        primary_key = {'gid':i, 'uid':i+1}
        attribute_columns = {'name':'somebody'+str(i), 'address':'somewhere'+str(i), 'age':i}
        condition = Condition(RowExistenceExpectation.IGNORE)
        item = PutRowItem(condition, primary_key, attribute_columns)
        put_row_items.append(item)

    update_row_items = []
    for i in range(10, 20):
        primary_key = {'gid':i, 'uid':i+1}
        attribute_columns = {'put': {'name':'somebody'+str(i), 'address':'somewhere'+str(i), 'age':i}}
        condition = Condition(RowExistenceExpectation.IGNORE, RelationCondition("age", i, ComparatorType.EQUAL))
        item = UpdateRowItem(condition, primary_key, attribute_columns)
        update_row_items.append(item)

    delete_row_items = []
    for i in range(10, 20):
        primary_key = {'gid':i, 'uid':i+1}
        condition = Condition(RowExistenceExpectation.IGNORE)
        item = DeleteRowItem(condition, primary_key)
        delete_row_items.append(item)

    request = MultiTableInBatchWriteRowItem()
    request.add(TableInBatchWriteRowItem(table_name, put=put_row_items, update=update_row_items))
    request.add(TableInBatchWriteRowItem('notExistTable', delete=delete_row_items))
    result = ots_client.batch_write_row(request)

    print 'Result status: %s'%(result.is_all_succeed())
    print 'check first table\'s put results:'
    succ, fail = result.get_put()
    for item in succ:
        print 'Put succeed, consume %s write cu.' % item.consumed.write
    for item in fail:
       print 'Put failed, error code: %s, error message: %s' % (item.error_code, item.error_message)

    print 'check first table\'s update results:'
    succ, fail = result.get_update()
    for item in succ:
        print 'Update succeed, consume %s write cu.' % item.consumed.write
    for item in fail:
       print 'Update failed, error code: %s, error message: %s' % (item.error_code, item.error_message)

    print 'check second table\'s delete results:'
    succ, fail = result.get_delete()
    for item in succ:
        print 'Delete succeed, consume %s write cu.' % item.consumed.write
    for item in fail:
       print 'Delete failed, error code: %s, error message: %s' % (item.error_code, item.error_message)

if __name__ == '__main__':
    ots_client = OTSClient(OTS_ENDPOINT, OTS_ID, OTS_SECRET, OTS_INSTANCE)
    try:
        delete_table(ots_client)
    except:
        pass
    create_table(ots_client)

    time.sleep(3) # wait for table ready
    batch_write_row(ots_client)
    delete_table(ots_client)

