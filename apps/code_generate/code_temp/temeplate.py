# # -*- coding: utf-8 -*-
# from xxx import BaseService
#
# __Author__ = 'fangshi.lb'
# __Date__ = '12-10-2'
#
#
# class NodeService(BaseService):
#     """
#     node servcie interface
#     """
#     def get_all_nodes(self):
#         """
#         查询所有node
#         """
#         sql = "select * from node t where t.deleted = 0;"
#         return self.db().query(sql)
#
#
#     def get_nodes(self,query):
#         """
#         获取node
#         """
#         if query:
#             sql = "select * from node n where n.deleted=0 order by n.created desc limit %s, %s;" % (query.start_row,query.end_row)
#             return self.db().query(sql)
#         else:
#             sql = "select * from node n where n.deleted=0 order by n.created desc limit %s, %s;" % (0,12)
#             return self.db().query(sql)
#
#
#     def create_node(self,title='', name='', header='', node_creater=0,node_avatar='',description=''):
#         """
#         创建node
#         """
#         sql = """insert into node(title,name,header,node_creater,node_avatar,description,deleted,created,updated=%s)
#                  values('%s','%s','%s','%s','%s','%s',0,now(),now());"""
#         self.db().execute_rowcount(sql)
#
#
#     def get_node_by_id(self,node_id):
#         """
#         根据node id 查询node
#         """
#         if node_id and node_id <= common_config.NODE_MAX_NUM:
#             sql = "select * from node n where n.id = %s" % node_id
#             return self.db().get(sql)
#
#
#     def get_node_count(self):
#         """
#         查询node个数
#         """
#         sql = "select count(id) from node;"
#         return self.db().query(sql)
#
#
#     def get_node_tribe(self,tribe_id):
#         """
#         查询某个部落下的node列表
#         """
#         if tribe_id and tribe_id >= 0:
#             sql = "select * from tribe t where t.id = %s;" % tribe_id
#             return self.db().query(sql)
#
#
#     def get_hot_node(self):
#         """
#         获取最热的节点
#         """
#         sql = 'select * from node LIMIT %s;' % common_config.hot_node_size
#         return self.db().query(sql)
#
#
#     def get_nodes_topic(self,node_id,query):
#         """
#         获取node下的topic列表
#         """
#         if node_id and query:
#             sql = """
#             select * from topic t where t.node_id = %s and t.deleted = 0 order by t.created desc limit %s,%s;
#             """ % (node_id,query.start_row,query.end_row)
#             return self.db().query(sql)
#         return None
#
#
#
#
#
#
#
