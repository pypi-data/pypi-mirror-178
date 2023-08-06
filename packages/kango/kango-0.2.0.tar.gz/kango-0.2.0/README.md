# Kango


## API

### Connection

```
import kango

#--- connect
db = kango.db(hosts="http://host:8529", username="root", password:str)

#--- select collection
coll = db.select_collection('test')

#--- insert item
coll.insert({k:v, ...})

#--- insert item with custom _key
coll.insert({k:v,...}, _key='awesome')





```

