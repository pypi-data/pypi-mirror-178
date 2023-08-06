# Angola

**Angola**

## API

## Connection

```
import angola

#--- connect
db = angola.db(hosts="http://host:8529", username="root", password:str)

#--- select collection
coll = db.select_collection('test')

#--- insert item
coll.insert({k:v, ...})

#--- insert item with custom _key
coll.insert({k:v,...}, _key='awesome')


```

### Query 

### Insert

### Update

### Delete

### Collection

### SubCollection


### Operators


### Custom Operators


