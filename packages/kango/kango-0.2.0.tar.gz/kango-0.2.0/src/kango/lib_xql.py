import re
from slugify import slugify
from . import lib

# === AQL Functions
# ---------------------------

# AQL UTILITIES
AQL_FILTER_OPERATORS = {
    "$EQ": "==",  # equal
    "$NE": "!=",  # not equal
    "$GT": ">",  # greater than
    "$GTE": ">=",  # greater than or equal
    "$LT": "<",  # lesser than
    "$LTE": "<=",  # lesser than or equal
    "$IN": "IN",  # left hand in right hand array -> field.value IN [values]
    # left hand not in right hand array -> field.value NOT IN [values]
    "$XIN": "NOT IN",
    # right hand in left hand array -> values IN [field.value]
    "$INCLUDES": "IN",
    # right hand not in left hand array -> values NOT IN [field.value]
    "$XINCLUDES": "NOT IN",
    "$LIKE": "LIKE",  # search
    "$XLIKE": "NOT LIKE"  # ,
    # "xgt": "" no greater
    # "xlt" no lesser
}
# reverse operator, where the right hand will point to left hand
# ie: cities:$includes:'charlotte' -> 'charlotte' IN cities
_rev_ops_order = ['$INCLUDES', '$XINCLUDES']


AQL_FILTER_LOGIC = {
    "$AND": " AND ",
    "$OR": " OR ",
    "$NOT": " NOT ",
    "$NOR": " NOR "
}


def aql_sort_builder(sorts: list, propkey: str) -> str:
    """
    Create a SORT clause

    Params
        sorts: list
            ["name:desc", "id:asc", "some.deep.path:desc"]
            alternative to list, it can be string
                sorts: "name:desc"
                sorts: "name" // will be ASC by default
        propkey:str
            the property key from the parent query
    Returns
        str
    """
    if not sorts:
        return ""

    # you can pass it as string
    # sorts: "name"
    if isinstance(sorts, str):
        sorts = [sorts]
    # make compatible with previous implementations.
    # sorts must now be a list, not dict.
    elif isinstance(sorts, dict):
        sorts = ["%s:%s" % (k, v) for k, v in sorts.items()]

    aql = ["%s.%s %s" % (propkey, s.split(":")[0], s.split(
        ":")[1] if len(s.split(":")) > 1 else "ASC") for s in sorts]
    return " SORT " + ", ".join(aql) + " "


def xql_collects_builder(collects: list, propkey: str) -> str:
    if not collects:
        return ""
    # TODO
    return ""


def _parse_filter_row(k, value, propkey):

    operator = "$EQ"  # default operator
    # extract the key and the operator
    # ie -> "name:$eq" or "city:$in"
    # link#, especially in join: "'name': '#parent.key'"

    if ":" in k:
        k, operator = k.split(":", 2)
        operator = operator.upper()

    # literal values starts with `#`
    # it indicates the value should not be converted, but rather return as is without `#`
    # ie:
    # - {k: "#parent.key"} -> k == parent.key
    # - {k: '#@params_value'} -> k == @params_value
    #
    dlit = isinstance(value, str) and value.startswith("#")

    # gen a unique number to make sure values generated are unique
    num_ = lib.gen_number(6)
    ukey = slugify("%s_%s" % (k, num_), separator="_")
    stmt = ""
    params = {}

    if dlit:
        value = value.replace("#", "")
        if operator in _rev_ops_order:  # reverse order
            stmt = " {value} {operator} {propkey}.{key}"
        else:
            stmt = " {propkey}.{key} {operator} {value}"
    else:
        params = {
            ukey: value
        }
        if operator in _rev_ops_order:  # reverse order
            stmt = " @{ukey} {operator} {propkey}.{key}"
        else:
            stmt = " {propkey}.{key} {operator} @{ukey}"

    aql = stmt.format(
        value=value,
        propkey=propkey,
        key=k,
        operator=AQL_FILTER_OPERATORS[operator],
        ukey=ukey)

    return aql, params


def aql_filter_builder(filters: dict, propkey: str) -> tuple:
    """
    Create a FILTER clause

    Params:
        filter: dict
            {
                'name': 'something',
                'age:$gt': 18,
                'cities:$in': ['charlotte', 'Concord'],
                '$or': [{
                       "cities:$in": [],
                       "_perms.read:$in":[] 
                 }]
                ]
            }
        propkey:str
            the property key from the parent query

    Returns
        tuple(aql:str, params:dict)

    """
    params = {}
    aql = ""
    for k in filters:

        if k.startswith("$"):
            k_ = k.upper()
            # operation
            if k_ in AQL_FILTER_LOGIC.keys() and isinstance(filters[k], (dict, list)):
                fk = filters[k]
                if isinstance(fk, dict):
                    fk = [fk]
                for k0 in fk:
                    tmp_aql = []
                    for k2 in k0:
                        _aql, _params = _parse_filter_row(k2, k0[k2], propkey)
                        tmp_aql.append(_aql)
                        params.update(_params)
                    aql += "FILTER (%s)\n" % AQL_FILTER_LOGIC[k_].join(tmp_aql)
            else:
                raise Exception("Invalid logic: %s" % k)
        else:
            _aql, _params = _parse_filter_row(k, filters[k], propkey)
            aql += "FILTER (%s)\n" % _aql
            params.update(_params)
        #value = filters[k]
        # operator = "$EQ"  # default operator

        # # extract the key and the operator
        # # ie -> "name:$eq" or "city:$in"
        # if ":" in k:
        #     k, operator = k.split(":", 2)
        #     operator = operator.upper()

        # # gen a unique number to make sure values generated are unique
        # num_ = lib.gen_number(6)
        # ukey = "%s_%s" % (k, num_)
        # aql += " FILTER {propkey}.{key} {operator} @{ukey} \n".format(
        #     propkey=propkey,
        #     key=k,
        #     operator=AQL_FILTER_OPERATORS[operator],
        #     ukey=ukey)
        #params[ukey] = value
    return aql, params



def prepare_xql(xql: dict) -> dict:
    _defaults = {
        "FROM": None,
        "ON": None,
        "AS": "doc__",
        "FILTER": {},
        "SORT": None,
        "SKIP": None,
        "COUNT_AS": None,
        "TAKE": 10,
        "PAGE": 1,
        "JOIN": [],
        "RETURN": "doc__",
        "RETURN_WITH": None,
        **xql
    }
    return {k.upper():v for k, v in _defaults.items()}


xql_format = prepare_xql


def xql_take_skip_page(xql: dict, max_limit=100) -> tuple:
    """
    Returns:
        type: tuple(TAKE:int, SKIP:int, PAGE:1)
            - TAKE: limit/per_page
            - SKIP: offset
            - PAGE: page #
    """
    xql = prepare_xql(xql)
    SKIP = xql.get("SKIP")
    TAKE = xql.get("TAKE") or 10
    PAGE = xql.get("PAGE") or 1

    if SKIP is None:
        page = PAGE or 1
        per_page = TAKE
        if per_page > max_limit:
            per_page = max_limit
        SKIP = lib.calc_pagination_offset(page=page, per_page=per_page)
        TAKE = per_page
    if TAKE > max_limit:
        TAKE = max_limit

    return TAKE, SKIP, PAGE

class XQLDEFINITION:
    """
    XQL Schema Definition:
        FROM: str = the collection name
        AS: str = alias
        FILTER: dict = filters
        SORT: list/str = sort 
        SKIP: int = the offset of the limit, default=0
        TAKE: int = the limit of result, default=10
        PAGE: int = help calculate the skip by using a page number. 
        JOIN: list[XQL]
        ON: str = when using join, it links the primary _key 
        COUNT_AS: str =  To count all the document, and return the value. Alias to `COLLECT WITH COUNT INTO`
        RETURN: str = string representation
        MERGE: str = on JOIN, to merge the data.
            ie: MERGE: "{__profile: profile}" 
            Can be done manually with RETURN MERGE(doc, {data})
    
    """
    FROM:str = None
    AS:str = None 
    FILTER:dict = {}
    SORT:list = []
    SKIP:int = 0
    TAKE:int = 10
    PAGE:int = 1
    JOIN:list = []
    ON:str = None
    COUNT_AS:str = None 
    RETURN:str = None
    MERGE:str = None


def xql_to_aql(xql: dict, vars: dict = {}, max_limit=100, parser=None):
    """
    XQL:=
    Xtensible Query Language to query data in ArangoDB 

    Params:
        xql: 
            type: dict = the XQL schema
        max_limit:
            type: int = a max number
        parser:
            type: function
        vars:
            type: dict - Variables for FILTER and FILTER_WHEN

    Returns:
        tuple(AQL:string, BIND_VARS:dict)

    ===
    XQL Schema Definition:
        FROM: str = the collection name
        AS: str = alias
        FILTER: dict = filters
        SORT: list/str = sort 
        SKIP: int = the offset of the limit, default=0
        TAKE: int = the limit of result, default=10
        PAGE: int = help calculate the skip by using a page number. 
        JOIN: list[XQL]
        ON: str = when using join, it links the primary _key 
        COUNT_AS: str =  To count all the document, and return the value. Alias to `COLLECT WITH COUNT INTO`
        RETURN: str = string representation
        MERGE: str = on JOIN, to merge the data.
            ie: MERGE: "{__profile: profile}" 
            Can be done manually with RETURN MERGE(doc, {data})


        #TODO
        - WHEN: ? = a conditional to evaluate before running
        - FILTER_WHEN: add additional filters when a condition is true

    === 
    schema example:
        FROM: collection
        AS: alias1
        FILTER:
            x:y
            "z:$gt": 5
        SORT: name:desc
        JOIN:
            FROM: collection2
            AS: c2
            FILTER:
                d: "#alias1.d"
            TAKE: 5
            PAGE: 2
            RETURN: c2
        TAKE: 10
        SKIP: 2
        RETURN 
            d
            c2


        === code example
        q = {
            "FROM": "job_posts",
            "AS": "post",
            "FILTER": {
                "a": "b",
                "c:$gt": 5
            },
            "SORT": ["id:desc"],
            "TAKE": 10,
            "SKIP": 47,
            "JOIN": [
                {
                    "AS": "app",
                    "FROM": "application",
                    "FILTER": {
                        "a": "b",
                        "c": "d",
                        "d": "#job.v_d"
                    },
                    "JOIN": [        {
                        "AS": "J_loco",
                        "FROM": "bam",
                        "FILTER": {
                            "a": "b",
                            "c": "d",
                            "d": "#app.v_d"
                        }
                    }]
                },
                {
                    "FROM": "loco",
                    "AS": "bam",
                    "FILTER": {
                        "a": "b",
                        "c": "d",
                        "d": "#app.v_d"
                    }
                }
            ],
            "RETURN": "MERGE(post, {__account: loco})"
    """

    xql = prepare_xql(xql)

    if not xql.get("AS"):
        xql["AS"] = "doc__"

    ALIAS = xql.get("AS") or "doc__"

    xql = parser(xql)
    COLLECTION = xql.get("FROM")
    FILTERS = xql.get("FILTER") or {}
    SORTS = xql.get("SORT")
    SKIP = xql.get("SKIP")
    TAKE = xql.get("TAKE") or 10
    PAGE = xql.get("PAGE") or 1
    JOINS = xql.get("JOIN") or []
    COUNT_AS = xql.get("COUNT_AS")
    COLLECTS = xql.get("COLLECT") or []
    RETURN = xql.get("RETURN") or ALIAS

    # work with take/skip
    if SKIP is None:
        page = PAGE or 1
        per_page = TAKE
        if per_page > max_limit:
            per_page = max_limit
        SKIP = lib.calc_pagination_offset(page=page, per_page=per_page)
        TAKE = per_page
    if TAKE > max_limit:
        TAKE = max_limit

    # unique num to give each field to prevent name collision
    num_ = lib.gen_number(6)

    aql_filter, filter_vars = aql_filter_builder(FILTERS, propkey=ALIAS)
    aql_sorting = aql_sort_builder(SORTS, propkey=ALIAS)
    aql_collects = xql_collects_builder(COLLECTS, propkey=ALIAS)
    if COUNT_AS:
        aql_collects += " COLLECT WITH COUNT INTO %s " % COUNT_AS

    bind_vars = {}

    # SUBQUERY/JOINS
    subquery = ""
    for xql2 in JOINS:
        xql2 = prepare_xql(xql2)
        X = xql_to_aql(xql=xql2, parser=parser, max_limit=max_limit)
        subquery += "\nLET %s = (%s) \n" % (xql2.get("AS"), X[0])
        bind_vars.update(X[1])

    # Query
    query = "FOR {alias} IN @@collection_{num_} ".format(
        alias=ALIAS, num_=num_)
    query += aql_filter
    query += subquery
    query += aql_collects
    query += " LIMIT @skip_%s, @limit_%s " % (num_, num_)
    query += aql_sorting
    query += "RETURN UNSET_RECURSIVE(%s, ['_id', '_rev', '_old_rev'])" % RETURN

    bind_vars.update({
        **filter_vars,
        "skip_%s" % num_: SKIP,
        "limit_%s" % num_: TAKE,
        "@collection_%s" % num_: COLLECTION
    })

    return query, bind_vars


def xql_extract_collections(xql: dict) -> list:
    """
    Extract all the collection names. 
    This can help with testing collection name

    Args:
        xql: dict

    Returns: 
        dict
    """
    xql = prepare_xql(xql)
    JOINS = xql.get("JOIN") or []
    collections = []
    for xql2 in JOINS:
        collections.extend(xql_extract_collections(xql2))
    collections.append(xql.get("FROM"))
    return list(set(collections))


def aql_detect_modifier_operations(aql: str) -> bool:
    """
    Detect if an AQL has retricted modifier operators.
    Use if we expect AQL to Query and not modify entries

    Params:
      @aql:
          type:str

    Returns
      bool

    """
    operators = ["REMOVE", "UPDATE", "REPLACE", "INSERT", "UPSERT"]
    return len([r for r in aql.split() if r.upper() in operators]) > 0



def aql_get_filter_keys(filters: dict) -> list:
    """
    Return all keys that are used for the filters
    """
    keys = set()
    for k in filters:
        if k.startswith("$"):
            k_ = k.upper()
            # operation
            if k_ in AQL_FILTER_LOGIC.keys() and isinstance(filters[k], (dict, list)):
                fk = filters[k]
                if isinstance(fk, dict):
                    fk = [fk]
                for k0 in fk:
                    for k2 in k0:
                        if ":" in k2:
                            _ = k2.split(":", 2)
                            keys.add(_[0])
                        else:
                            keys.add(k2)
            else:
                raise Exception("Invalid logic: %s" % k)
        else:
            if ":" in k:
                _ = k.split(":", 2)
                keys.add(_[0])
            else:
                keys.add(k)
    return list(keys)


#
class XQLDSLError(Exception):
    pass



def extract_dsl_directives(matching:dict) -> dict:
    return {k:v for k, v in matching.items() if k.startswith("@") }

def extract_dsl_non_directives(matching:dict) -> dict:
    return {k:v for k, v in matching.items() if not k.startswith("@") }

def extract_valid_dsl_slice(slicing:dict) -> dict:
    valids = ["page", "per_page", "limit", "skip", "take"]
    return {k:v for k, v in slicing.items() if k in valids}

DSL_COLLECTION_METHODS = ["get", "put", "delete", "search", "archive", "unarchive"]

def parse_action_dsl(action):
    """
    Convert action DSL to XQL


    # methods:
        - get
        - put
        - delete
        - search
        - archive
        - unarchive

    # schema

    :+: collection

        "[method]/[collection]": {
            @matching: {
                _key:str|[str]
                k_v:props,
                ...

                @payload: {...},

                @slicing: {
                  page:int
                  per_page:int
                  limit:int                  
                },

                @sorting: str|list -> ["_key:asc", ...],

                @options: {
                    acl_grant_read
                    acl_grant_readwrite
                    acl_revoke
                    acl_revoke_all 
                    visibility: private|public,
                    searchable: bool,
                    ttl?
                },
                @change_user_key: {

                }
            },
            @insert: {
                @payload: {...},
                @otions
            }
        }
    
    :+: generic

        "[action]/[method]": {
            k_v: dict
        }

    """

    # contains an action propert
    if "action" in action:
        return action

    new_action = {}
    for k, val in action.items():

        # 
        if "/" in k:

            action_name, action_method = k.split("/", 1)

            # *[method]/[collection] specific
            # *(get|put|delete|search|archive|unarchive)/[collection_name]
            if action_name in DSL_COLLECTION_METHODS:
                method = action_name
                _method = action_name
                collection_name = action_method
                new_action["collection"] = collection_name
                
                _matching = val.pop("@matching") if "@matching" in val else None
                _insert = val.pop("@insert") if "@insert" in val else None
                _properties = val.pop("@properties") if "@properties" in val else None
                
                _matching_payload = _matching.pop("@payload", None) if _matching and "@payload" in _matching else None
                _insert_payload = _insert.pop("@payload", None) if _insert and "@payload" in _insert else None
                _matching_options = _matching.pop("@options", None) if _matching and "@options" in _matching else None
                _insert_options = _insert.pop("@options", None) if _insert and "@options" in _insert else None

                if _properties:
                    new_action["properties"] = _properties

                # [get] dual method: [get|find]
                if method == "get":
                    """
                      [get]/[collection]: {
                          @matching: {
                                _key - for single entry -> {}

                                k/v:dict - for multiple -> [{},...],

                                @slicing: {
                                    page:int
                                    per_page:int
                                    limit:int
                                },

                                @sorting: str|list,

                                @options: {
                                    ...
                                }                                 
                          },                         
                      }
                    """
                    if not _matching:
                        raise XQLDSLError("MISSING: @matching")

                    _slicing = _matching.pop("@slicing", None)
                    if _slicing and isinstance(_slicing, dict):
                        new_action.update(extract_valid_dsl_slice(_slicing))

                    if _matching_options:
                        new_action["options"] = _matching_options

                    _sorting = _matching.pop("@sorting", None)
                    if _sorting:
                        new_action["sort"] = _sorting

                    if "_key" in _matching:
                        if not _matching.get("_key"):
                            raise XQLDSLError("MISSING: '_key'")
                        else:
                            _method = "get"
                            new_action["_key"] = _matching.get("_key")
                    else:
                        _method = "find"
                        new_action["filter"] = _matching



                # [delete|archive|unarchive]
                elif method in ["delete", "archive", "unarchive"]:
                    """
                      [delelete|archive|unarchive]/[collection]: {
                        @matching: {
                          _key:str|[str], # required or must have filters
                          k:v-filters # any other k/v pair
                        }
                      }
                    """
                    if not _matching:
                        raise XQLDSLError("MISSING: @matching")

                    if _matching_options:
                        new_action["options"] = _matching_options

                    _key = _matching.pop("_key", None)
                    if _key:
                        new_action["_key"] = _key
                    else:  # filters
                        if not _matching:
                            raise XQLDSLError("MISSING: @matching")
                        new_action["filter"] = _matching


                # [search]
                elif method == "search":
                    """
                      [search]/[collection]: {
                          @matching: {
                            query:str,

                            @slicing: {
                                page:int
                                limit:int
                                per_page:int
                            }
                          },
                      }
                    """
                    if not _matching:
                        raise XQLDSLError("MISSING: @matching")
                    query = _matching.pop("query", None)
                    if query:
                        new_action["query"] = query

                        _slicing = _matching.pop("@slicing", None)
                        if _slicing and isinstance(_slicing, dict):
                            new_action.update(extract_valid_dsl_slice(_slicing))

                    else:
                      raise XQLDSLError("MISSING: @matching")

                # [put] - handles create|update|upsert
                elif method == "put":
                    """

                      !insert
                      [put]/[collection]: {
                         @insert: {
                            @payload
                            @properties
                         }
                      }

                      !update
                      [put]/[collection]: {
                          @matching: {
                              _key
                              k/v...
                              @payload: {

                              }
                              @properties
                          }
                      }

                      !upsert
                      [put]/[collection]: {
                          @matching: {
                              _key: str
                              k_v: dict
                              @payload: {
                                ...
                              },
                              @options
                          },
                          @insert: {
                              @payload: {
                                ...
                              }
                              @options
                          }
                      }                    
                    """
                    if _matching and (_matching_payload or _matching_options):
                        _method = "update"
                        _key = _matching.pop("_key", None)
                        _filters = extract_dsl_non_directives(matching=_matching)

                        new_action["data"] = {}
                        if _matching_payload:
                            new_action["data"] = _matching_payload
                        
                        if _key and _filters:
                            raise XQLDSLError("CONFLICT: _key & filters")

                        # one key can be updated without filter
                        elif _key:
                            new_action["data"]["_key"] = _key
                        
                        # only with filters you can do upsert
                        elif _filters:
                            new_action["filter"] = _filters
                            if _insert_payload:
                                # data to update on filter
                                new_action["partial"] = _matching_payload
                                # new data to insert
                                new_action["data"] = _insert_payload
                                new_action["upsert"] = True
                        else:
                            raise XQLDSLError("MISSING: Invalid query")

                    # insert 
                    elif _insert_payload:
                        _method = "create"
                        new_action["data"] = _insert_payload

                    else:
                        raise XQLDSLError("MISSING: @matching|@insert")

                    if _matching_options or _insert_options:
                        new_action["options"] = _matching_options or _insert_options

                new_action["action"] = "collection.%s" % _method
            
            # *[action]/[method]
            else:
                """
                [path]/[endpoint]: {
                    k_v:dict
                }
                """
                new_action.update(val)
                new_action["action"] = "%s.%s" % (action_name, action_method)

    return new_action
