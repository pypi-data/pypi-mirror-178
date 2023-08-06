import copy 
from contextlib import contextmanager
from . import lib, dict_mutator, dict_query
from typing import Any, List


class KangoError(Exception): pass

class AdapterError(KangoError): pass
class CollectionNotFoundError(KangoError): pass
class CollectionExistsError(KangoError): pass
class ItemNotFoundError(KangoError):pass
class ItemExistsError(KangoError):pass
class NoResultsError(KangoError): pass
class ConstraintError(KangoError): pass
class UndeletableError(KangoError): pass
class MissingCommitterCallbackError(KangoError): pass
class MissingItemKeyError(KangoError): pass

def create_document_item(data:dict={}) -> dict:
    _key = data["_key"] if "_key" in data else lib.gen_key()
    ts = lib.get_datetime()

    return {
        **data,
        "_key": _key,
        "_created_at": ts,
        "_modified_at": None
    }


class Item_Impl(dict):
    NAMESPACE = None
 
    def _make_path(self, path):
        # if self.NAMESPACE:
        #     return "%s.%s" % (self.NAMESPACE, path)
        return path

    def _update(self, data):
        raise NotImplementedError()

    def get(self, path: str, default: Any = None) -> Any:
        """
        GET: Return a property by key/DotNotation

        ie: 
            #get("key.deep1.deep2.deep3")

        Params:
            path:str - the dotnotation path
            default:Any - default value 

        Returns:
            Any
        """
        path = self._make_path(path)
        return lib.dict_get(obj=dict(self), path=path, default=default)

    def set(self, path: str, value: Any):
        """
        SET: Set a property by key/DotNotation

        Params:
            path:str - the dotnotation path
            value:Any - The value

        Returns:
            Void
        """

        path = self._make_path(path)
        self._update({path: value})

    def len(self, path: str):
        """
        Get the length of the items in a str/list/dict
        Params:
            path:str - the dotnotation path
        Returns:
            data that was removed
        """
        path = self._make_path(path)
        v = self.get(path)
        return len(v) if v else 0

    def incr(self, path: str, incr=1):
        """
        INCR: increment a value by 1
        Args
            path:str - path
            incr:1 - value to inc by
        Returns:    
            int - the value that was incremented
        """
        op = "%s:$incr" % self._make_path(path)        
        oplog = self._update({op: incr})
        return oplog.get(op)

    def decr(self, path: str, decr=1):
        """
        DECR: decrement a value by 1
        Args
            path:str - path
            decr:1 - value to dec by
        Returns:    
            int - the value that was decremented
        """
        op = "%s:$decr" % self._make_path(path)

        oplog = self._update({op: decr})
        return oplog.get(op)

    def unset(self, path: str):
        """ 
        UNSET: Remove a property by key/DotNotation and return the value

        Params:
            path:str

        Returns:
            Any: the value that was removed
        """
        path = self._make_path(path)
        self._update({"%s:$unset" % path: True})

    def xadd(self, path: str, values):
        """
        LADD: Add *values if they don't exist yet

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xadd" % self._make_path(path)
        self._update({op: values})

    def xadd_many(self, path: str, *values: List[Any]):
        """
        LADD: Add *values if they don't exist yet

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xadd_many" % self._make_path(path)
        self._update({op: values})

    def xrem(self, path: str, values):
        """
        LREM: Remove items from a list

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xrem" % self._make_path(path)
        oplog = self._update({op: values})
        return oplog.get(op)

    def xrem_many(self, path: str, *values: List[Any]):
        """
        LREM: Remove items from a list

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xrem_many" % self._make_path(path)
        oplog = self._update({op: values})
        return oplog.get(op)

    def xpush(self, path: str, values: Any):
        """
        LPUSH: push item to the right of list. 

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xpush" % self._make_path(path)
        self._update({op: values})

    def xpush_many(self, path: str, *values: List[Any]):
        """
        LPUSH: push item to the right of list. 

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xpush_many" % self._make_path(path)
        self._update({op: values})

    def xpushl(self, path: str, values: Any):
        """
        LPUSH: push item to the right of list. 

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xpushl" % self._make_path(path)
        self._update({op: values})

    def xpushl_many(self, path: str, *values: List[Any]):
        """
        LPUSH: push item to the right of list. 

        Params:
            path:str - the dotnotation path
            *values: set of items
        Returns:
            list: updated data
        """
        op = "%s:$xpush_many" % self._make_path(path)
        self._update({op: values})

    def xpop(self, path: str):
        """
        Remove value at the end an array/list
        Params:
            path:str - the dotnotation path
        Returns:
            data that was removed

        """
        op = "%s:$xpop" % self._make_path(path)
        oplog = self._update({op: True})
        return oplog.get(op)

    def xpopl(self, path: str):
        """
        Remove value at the beginning an array/list
        Params:
            path:str - the dotnotation path
        Returns:
            data that was removed        
        """
        op = "%s:$xpopl" % self._make_path(path)
        oplog = self._update({op: True})
        return oplog.get(op)

    def datetime(self, path:str, value:Any=True):
        op = "%s:$datetime" % self._make_path(path)
        oplog = self._update({op: value})
        return oplog.get(op)        

    def template(self, path:str, value:str):
        op = "%s:$template" % self._make_path(path)
        oplog = self._update({op: value})
        return oplog.get(op)

    def uuid4(self, path:str):
        op = "%s:$uuid4" % self._make_path(path)
        oplog = self._update({op: True})
        return oplog.get(op)

    def update(self, data: dict, commit=False):
        """
        UPDATE: Update the active CollectionItem

        Returns:
            CollectionItem
        """
        self._update(data)


class CollectionItem(Item_Impl):
    """
    CollectionItem

    Every row is a document 
    """

    # item _key
    _key = None

    # items subcollections
    _subcollections = {}
    
    # immutable keys
    _immut_keys = []

    @classmethod
    def new(cls, data:dict, immut_keys:list=[], commiter=None):
      return cls(data=create_document_item(data), immut_keys=immut_keys, commiter=commiter)

    def __init__(self, data: dict, immut_keys:list=[], load_parser=None, commiter=None):
        if "_key" not in data:
            raise MissingItemKeyError()
        
        self._load_parser = load_parser
        self._commiter = commiter
        self._immut_keys = immut_keys
        self._cx = False
    
        data, _ = dict_mutator.mutate(mutations=data,  immuts=immut_keys)
        self._load(data)

    def to_dict(self):
        data = dict(self)
        if self._subcollections:
            data["/subcollections"] = self._subcollections
        return data 

    def set_immut_keys(self, immut_keys:list=[]):
        self._immut_keys = immut_keys

    @contextmanager
    def subcollection(self, name: str, constraints: list = None):
        """
        *Context Manager

        Select a subcollection and saves it any data upon exit

        Yield:
          SubCollection

        Example:

        with $parent.subcollection('name') as sc:
            sc...
        
        """
        sc = SubCollection(item=self, name=name)
        yield sc
        self.commit()

    def select_subcollection(self, name: str, constraints: list = None):
        """
        *Non Context Manager 

        Select a subcollection. When making changes, must use `commit` on parent

        Retuns:
          SubCollection

        Example:
            sc = $parent.select_subcollection()
            sc...
            sc...
            $parent.commit()

        """
        return SubCollection(item=self, name=name)
        

    @property
    def subcollections(self) -> list:
        """ List all collections """
        return list(self._subcollections.keys()) or []

    def drop_subcollection(self, name: str):
        try:
            if name in self._subcollections:
                del self._subcollections[name]
            self.set("/subcollections", self._subcollections)
        except KeyError as _:
            pass
        return True

    def _set_subcollection(self, name:str, data:Any):
        self._subcollections[name] = data
        self.set("/subcollections", self._subcollections)

    def save(self):
        """
        To commit the data when it's mutated outside.
            doc = CollectionItem()
            doc["xone"][1] = True
            doc.save()
        """
        data = dict(self)
        self._update(data)

    def commit(self):
        if not self._commiter:
            raise MissingCommitterCallbackError()
        data = self._commiter(self)
        if data:
            self._load(data)
        

    def _update(self, mutations: dict):
        """
        Return oplog
        """
        data = self.to_dict()
        doc, oplog = dict_mutator.mutate(mutations=mutations, init_data=data, immuts=self._immut_keys)
        self._load(doc)
        return oplog

    def _load(self, item: dict):
        """
        load the content into the document

        Params:
            row: dict
        """
        self._clear_self()
        
        if self._load_parser:
          item = self._load_parser(item)

        self._subcollections = {}
        if "/subcollections" in item:
            self._subcollections = item.pop("/subcollections") or {}

        if "_key" in item:
            self._key = item.get("_key")
        super().__init__(item)

    def _clear_self(self):
        """ clearout all properties """
        for _ in list(self.keys()):
            if _ in self:
                del self[_]


class SubCollection(object):
    _data = []
    _constraints = []
    _item = None
    _name = None 

    def __init__(self, item: CollectionItem, name: str, constraints:list=None):
        self._item = item
        self._name = name
        self._constraints = constraints
        self._load()

    def _load(self):
        self._data = self._item._subcollections.get(self._name) or []

    def _commit(self):
        self._item._set_subcollection(self._name, self._data)

    def _save(self, _key, data):
        _data = self._normalize_data()
        _data[_key] = data
        self._data = self._denormalize_data(_data)
        self._commit()        

    def _normalize_data(self) -> dict:
        return { d.get("_key"): d for d in self._data}

    def _denormalize_data(self, data:dict) -> list:
        return list(data.values())

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self.find())

    @property
    def items(self):
        """ 
        Returns an iterator of all documents

        Returns:
            Iterator
        """
        return self.find()

    def has(self, _key):
        return bool(self.find_one({"_key": _key}))

    def insert(self, data: dict, _key:str=None):
        """
        Insert document

        Params:
            data:dict
            _key: to insert with a _key
        """
        data, _ = dict_mutator.mutate(mutations=data.copy(), immuts=self._item._immut_keys)

        if self._constraints:
            for c in  self._constraints:
                if c in data:
                    if self.find_one({c: data[c]}):
                        raise ConstraintError("Key: %s" % c)

        if _key or "_key" in data:
            _key = _key or data["_key"]
            if self.has(_key):
                raise ItemExistsError()
            data["_key"] = _key
        item = data

        item = create_document_item(data)
        self._data.append(item)
        self._commit()
        return SubCollectionItem(self, item)

    def update(self, filters:dict, mutations: dict, upsert:bool=False):
        """
        Update by filter

        Params:
            filter:dict - filter document criteria
            mutations:dict - changes on the found documents
        """
        _data = self._normalize_data()
        res = self.find(filters)
        if res:
            for item in res:
                ts = lib.get_timestamp()
                _key = item.get("_key")
                _default = {  # ensuring we do some data can't be overwritten
                    "_key": _key,
                    # "_created_at": ts
                }
                upd, _ = dict_mutator.mutate(mutations=mutations, init_data=item, immuts=self._item._immut_keys)
                _data[_key] = {**upd, **_default}
            self._data = self._denormalize_data(_data)
            self._commit()

        elif upsert:
            self.add(mutations)
  
    def delete(self, filters: dict):
        """
        Delete documents based on filters

        Params:
            filters:dict
        """
        _data = self._normalize_data()
        for item in self.find(filters):
            del _data[item.get("_key")]
        self._data = self._denormalize_data(_data)
        self._commit()

    def find_one(self, filters:dict={}):
        """
        Return only one item by criteria

        Return:
            dict
        """
        if res := self.find(filters=filters, limit=1):
            return list(res)[0]
        return None 

    def get(self, _key:str):
        """
        Return a document from subcollection by id 

        Returns:
        """
        return self.find_one({"_key": _key})

    def find(self, filters: dict = {}, sorts: dict = {}, limit: int = 10, skip: int = 0) -> dict_query.Cursor:
        """
        Perform a query

        Params:
            filters:
            sorts:
            limit:
            skip:
        """
        sorts = _parse_sort_dict(sorts, False)
        data = [SubCollectionItem(self, d) for d in dict_query.query(data=self._data, filters=filters)]
        return dict_query.Cursor(data, sort=sorts, limit=limit, skip=skip)

    def filter(self, filters: dict = {}) -> dict_query.Cursor:
        """
        Alias to find() but makes it seems fluenty
        
        Returns:
            dict_query:Cursor
        """
        data = dict_query.query(data=self._data, filters=filters)
        return dict_query.Cursor([SubCollectionItem(self, d) for d in data])

class SubCollectionItem(Item_Impl):
    _key = None 

    def __init__(self, subCollection: SubCollection, data):
        self._subcollection = subCollection
        self._load(data)

    @property
    def parent(self):
        """
        Holds parent data
        """
        return self._subcollection._item

    def _update(self, mutations):
        data = dict(self)
        mutations = copy.deepcopy(mutations)
        doc, oplog = dict_mutator.mutate(mutations=mutations, init_data=data, immuts=self.parent._immut_keys)
        self._subcollection._save(self._key, doc)
        self._load(doc)
        return oplog

    def _load(self, data):
        self._key = data.get("_key")
        super().__init__(data)


def _parse_row(row: dict) -> dict:
    """
    Convert a result row to dict, by merging _json with the rest of the columns

    Params:
        row: dict

    Returns
        dict
    """
    row = row.copy()
    _json = lib.json_loads(row.pop("_json")) if "_json" in row else {}
    return {
        **row,  # ensure columns exists
        **_json
    }


def _ascdesc(v, as_str=True):
    if as_str:
        if isinstance(v, int):
            return "DESC" if v == -1 else "ASC"
    else:
        if isinstance(v, str):
            return -1 if v.upper() == "DESC" else 1
    return v


def _parse_sort_dict(sorts: dict, as_str=True):
    return [(k, _ascdesc(v, as_str)) for k, v in sorts.items()]
