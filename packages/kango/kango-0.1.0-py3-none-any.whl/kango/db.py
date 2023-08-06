#-----------------------------
# -- kango --
#-----------------------------


from . import lib_collection, lib, lib_xql
from arango import ArangoClient
from arango.exceptions import ArangoError

class QueryResult(object):
    def __init__(self, cursor, pager):
        self.cursor = cursor
        stats = cursor.statistics()
        self.pagination = lib.gen_pagination(total_count=stats["fullCount"],
                                            count=cursor.count(),
                                            page=pager[0],
                                            per_page=pager[1])

    def __iter__(self):
        for item in self.cursor:
            yield item

class Database(object):
    """
    Database
    Source: ArangoDB
    """

    def __init__(self,
                 hosts:str=None,
                 username:str="root",
                 password:str=None, 
                 dbname: str = "_system", 
                 client:"Database"= None, 
                 default_document_indexes:dict={},
                 query_max_limit=100):
        """
        
        Params:
            host:str|list
            username:str
            password
            dbname
            client:Database
            default_document_indexes:dict
            query_max_limit
        
        """

        self.client = client
        self.username = username
        self.password = password
        self.db = None
        self.dbname = dbname
        self.default_document_indexes = default_document_indexes
        self.query_max_limit = query_max_limit

        if not self.client:
            self.client = ArangoClient(hosts=hosts, serializer=lib.json_ext.dumps, deserializer=lib.json_ext.loads)

        if self.dbname:
            self.db = self.client.db(name=self.dbname, username=self.username, password=self.password)

    @property
    def aql(self):
        return self.db.aql

    def has_db(self, dbname:str=None) -> bool:
        """
        Check if the system has a database

        Params:
            dbname:str|None - The dbname to check or the current self.dbname

        Returns: 
            bool
        """
        _dbname = dbname or self.dbname
        sys_db = self.use_db("_system")
        return sys_db.db.has_database(_dbname)

    def create_db(self, dbname:str=None) -> "Database":
        """
        Create a database if doesn't exists
        Params:
            dbname:str|None - The dbname to check or the current self.dbname

        Returns:
            Database
        """
        _dbname = dbname or self.dbname
        sys_db = self.use_db("_system")
        if not sys_db.db.has_database(_dbname):
            sys_db.db.create_database(_dbname)
        return self.select_db(_dbname)

    def select_db(self, dbname:str) -> "Database":
        """
        Select a different DB using the same connection

        Params:
            dbname:str - The dbname to check
        Returns: 
            Database

        """
        return Database(client=self.client, dbname=dbname, username=self.username, password=self.password, scope=self.scope)

    def has_collection(self, collection_name) -> bool:
        """
        Test if collection exists in the current db

        Params:
            collection_name:str - the collection name 

        Returns:
            bool
        """
        return self.db.has_collection(collection_name)


    def select_collection(self, collection_name, indexes=None, immut_keys=None, user_defined=False) -> "Collection":
        """
        To select a collection

        Params:
            collection_name:str - collectioin name 
            indexes:List[dict] - the indexes to use
            immut_keys:list - immutable keys. Keys that can't be updated once created

        Return:
            Collection

        """

        if self.has_collection(collection_name):
            col = self.db.collection(collection_name)
        else:
            col = self.db.create_collection(collection_name)
            if not indexes and user_defined is True and self.default_document_indexes:
                indexes = self.default_document_indexes
            # Add index
            if indexes:
                for index in indexes:
                    col._add_index(index) 

        return Collection(collection=col, immut_keys=immut_keys)


    def execute_aql(self, query:str, bind_vars:dict={}, *a, **kw):
        """ 
        Execute AQL 
        Params:
            query:str - the AQL to execute 
            bind_vars: dict - the variables to pass in the query
        Return aql cursor
        """
        return self.aql.execute(query=query, bind_vars=bind_vars, *a, **kw)


    def xql_parser(self, xql):
        """
        xql_parser to parse the XQL before it returns the AQL
        """

        # !custom implementation... need to be revised
        # collection_map = {
        #     "@/USERID": "__auth",
        #     "@/STORAGE": "__storage"
        # }

        # 
        # @/USERID
        #
        # Retrieve the basic info
        #
        #   - _key
        #   - display_name
        #   - photo_url
        #
        # if xql["FROM"] == "@/USERID":
        #     avatars_url = config.AVATARS_API_URL
        #     avatars_style = config.AVATARS_DEFAULT_STYLE

        #     if "ON" not in xql:
        #         raise Exception("MISSING XQL property 'ON' for @/USERID")
        #     xql["FILTER"] = {"$or": { "_key": xql["ON"] , "_key:$in": xql["ON"] } }
        #     _return = """{
        #             _key: %(alias)s._key, 
        #             display_name: %(alias)s.display_name, 
        #             photo_url: %(alias)s.photo_url ? %(alias)s.photo_url :  CONCAT('%(avatar_u)s/%(avatar_s)s/', %(alias)s._key ,'.svg')
        #         }""" % {"alias": xql["AS"], "avatar_u": avatars_url, "avatar_s": avatars_style }
        #     # MERGE
        #     # Only with the presence of merge, we will merge the data with other results
        #     # otherwise just return the AUTH account data
        #     if "MERGE" in xql:
        #         xql["RETURN"] = "MERGE(%s, %s)" % (_return, xql["MERGE"])
        #     else:
        #         xql["RETURN"] = _return
            
        # # get the name of the collection 
        # if xql["FROM"] in collection_map:
        #     xql["FROM"] = collection_map[xql["FROM"]]  

        return xql

    def query(self, xql:lib_xql.XQLDEFINITION, data:dict={}, kvmap:dict={}) -> QueryResult:
        """
        XQL query  a collection based on filters

        It will return the cursor:ArangoCursor and a pagination for the current state
        
        Params:
            xql:lib_xql.XQLDEFINITION
            data:dict
            kvmap:dict

        Returns
            tuple(cursor:ArangoCursor, pagination:dict)
        """
        aql, bind_vars, pager = self.build_query(xql=xql, data=data, kvmap=kvmap)
        cursor = self.execute_aql(aql, bind_vars=bind_vars, count=True, full_count=True)            

        # Add pagination for #find
        stats = cursor.statistics()
        pagination = lib.gen_pagination(total_count=stats["fullCount"],
                                        count=cursor.count(),
                                        page=pager[0],
                                        per_page=pager[1])
        return QueryResult(cursor=cursor, pager=page)

    def build_query(self, xql:lib_xql.XQLDEFINITION, data:dict={}, kvmap:dict={}):
        """
        Build a query from XQL

        Return tuple:
            - aql:str
            - bind_vars:dict
            - pagination:tuple 
                -> tuple(page, per_page)
        """        
        xql = lib_xql.prepare_xql(xql)
        # replace the kvmap
        xql["FILTER"] = lib.dict_find_replace(xql["FILTER"], kvmap)

        # pagination
        if "page" in data:
            xql["PAGE"] = data.get("page") or 1
            del data["page"]
        if "take" in data:
            xql["TAKE"] = data.get("take") or 10
            del data["take"]

        _per_page, _, _page = lib_xql.xql_take_skip_page(xql=xql, max_limit=self.query_max_limit)
        aql, bind_vars = lib_xql.xql_to_aql(xql, vars=data, parser=self.xql_parser, max_limit=self.query_max_limit)
        bind_vars.update(data)
        return aql, bind_vars, (_page, _per_page)

    def collections(self) -> list:
        """
        All collections in the db

        Returns:
            list
        """
        return self.db.collections()
    
    def rename_collection(self, collection_name:str, new_name:str):
        """
        Rename collection
        """
        if self.has(collection_name) and not self.has(new_name):
            coll = self.select(collection_name)
            coll.rename(new_name)
            return self.select(new_name)
    
    def drop_collection(self, collection_name:str):
        if self.has(collection_name):
            self.db.delete_collection(collection_name)

    def add_index(self, collection_name, data:dict):
        """
        Args:
            - collection, the collection name
            - data: dict of 
                    {
                        "type": "persistent",
                        "fields": [] # list of fields
                        "unique": False # bool - Whether the index is unique
                        "sparse": False # bool,
                        "name": "" # str - Optional name for the index
                        "inBackground": False # bool - Do not hold the collection lock
                    }
        """
        col = self.db.collection(collection_name)
        col._add_index(data)
      
    def delete_index(self, collection_name:str, id):
        """
        Delete Index

        Args:
            - collection, the collection name
            - id: the index id
        """
        col = self.db.collection(collection_name)
        col.delete_index(id, ignore_missing=True)

class Collection(object):

    def __init__(self, collection,  immut_keys:list=[]):
        self.collection = collection
        self._immut_keys = immut_keys

    def item(self, data:dict) -> lib_collection.CollectionItem:
        """
        Load data as item

        Returns:
            lib_collection.CollectionItem
        """
        if not isinstance(data, lib_collection.CollectionItem):
            if "_key" not in data:
                return lib_collection.CollectionItem.new(data, commiter=self._commit, immut_keys=self._immut_keys)               
        return lib_collection.CollectionItem(data, commiter=self._commit, immut_keys=self._immut_keys)


    def _commit(self, item:lib_collection.CollectionItem):
        """
        Save the item in the db
        """
        if not item._key:
            raise lib_collection.MissingItemKeyError()
        return self.collection.update(item.to_dict(), return_new=True)["new"]

    @property
    def name(self) -> str:
        """
        Returns the collection name
        """
        return self.collection.name

    def has(self, _key) -> bool: 
        """
        
        Check if a collection has _key

        Args:
            _key

        Returns: 
            Bool
        """
        return self.collection.has(_key)

    def get(self, _key) -> lib_collection.CollectionItem:
        """ 
        Get a document from the collection and returns a collectionItem
        Returns:
            lib_collection.CollectionItem
        """

        if data:= self.collection.get(_key):
            return self.item(data)
        return None

    def new_item(self, data:dict={}) -> lib_collection.CollectionItem:
        """
        To create a new Item without inserting in the collection

        *Must use #item.commit() to save data

        Returns:
            lib_collection.CollectionItem
        """
        return lib_collection.CollectionItem.new(data, commiter=self._commit)

    def insert(self, data:dict, _key=None, return_item:bool=True) -> lib_collection.CollectionItem:
        """
        To insert and commit a new item


        Returns:
            lib_collection.CollectionItem
        """
        if _key or "_key" in data:
            _key = _key or data["_key"]
            if self.has(_key):
                raise lib.ItemExistsError()
            data["_key"] = _key
        item = data
        if not isinstance(data, lib_collection.CollectionItem):
            item = lib_collection.CollectionItem.new(data)
        self.collection.insert(item.to_dict(), silent=True)
        if return_item:
            return self.get(item._key) 
        return None

    def update(self, _key:str, data:dict, return_item:bool=True) -> lib_collection.CollectionItem:
        """
        Save document data by _key
        """
        item = self.item({**data, "_key": _key})
        self._commit(item)  
        if return_item:
            return self.get(item._key) 
        return None

    def delete(self, _key):
        """
        Delete a document by _key
        """
        self.collection.delete(_key)

    def find(self, filters:dict, skip=None, limit=None):
        """
        Perform a find in the collections

        Returns
            Generator[lib_collection.CollectionItem]
        """
        for data in self.collection.find(filters=filters, skip=skip, limit=limit):
            yield self.item(data)

