# Class 4 API

## Resources

### Accounts
##### Description: Primary top-level end-user resource (all resources scoped to an account)
1. Endpoints
  - `/accounts`
    - GET : returns a paginated collection of authorized resources
    - POST : creates an account (required site-administrator privileges)
      - Root-level resource (no dependencies)
  - `/accounts/<uuid>`
    - GET : returns a single account item
    - PATCH : update one or more fields
    - DELETE : deletes an account
  - `/accounts/<uuid>/numbers`
    - GET : paginated collection of `AccountNumber` resources
    - POST : creates an `AccountNumber` resource (/accountnumbers/<uuid>)
      - Dependencies : `Number`
  - `/accounts/<uuid>/servers`
    - GET : paginated collection of `AccountServer` resources
    - POST : creates an `AccountServer` resource (/accountservers/<uuid>)
             and a `Server` with the type set to `account`
      - Dependencies : `Server`
  - `/accounts/<uuid>/orders`
    - GET : paginated collection of `AccountOrder` resources
    - POST : creates an `AccountOrder` resource (/accountorders/<uuid>)

2. Schema
    - `name` - string
    - `description` - string
    - `enabled` - boolean

#### AccountNumbers
* Relationship model
1. Endpoints
  - /accountnumbers/<uuid>
    - GET : returns the resource object
    - DELETE : deletes the object
  - /accountnumbers/<`Number:e164`>/lidb/
    - GET : returns the single resource
    - PATCH : updates an item
    - DELETE : deletes the object
  - /accountnumbers/<`Number:e164`>/e911/
    - GET : returns the single resource
    - PATCH : updates an item
    - DELETE : deletes the object

2. Schema
 - `account` - ForeignKey(`Account`)
 - `number` - ForeignKey(`Number`)
 - `route` - (null = true)
 - `created_at` - datetime(utc)
 - `created_by` - uuid

3. AccountNumberLIDB Schema
 - `account_type` - string (choices=(residential, business))
 - `listed_name` - string (max_length=15)
 - `accountnumber` - ForeignKey(`AccountNumber`) OneToOne

4. AccountNumberE911 Schema
 - `created_at` - datetime(utc)
 - `provisioned_at` - datetime(utc)
 - `created_by` - uuid
 - `address1` - string
 - `address2` - string
 - `city` - string
 - `state` - string
 - `zipcode` - string
 - `comment` - string
 - `accountnumber` - ForeignKey(`AccountNumber`) OneToOne

#### AccountServers
* Relationship model (manytomany through=)


2. Schema
 - `account` - ForeignKey(`Account`)
 - `server` - ForeignKey(`Server`)
 - `created_at` - datetime(utc)
 - `created_by` - uuid


### Numbers
1. Endpoints
  - /numbers/
    - GET : paginated collection
    - POST : creates a number (required site-administrator privileges)
    - PATCH : updates the schema
    - PUT : idempotent create

2. Schema
 - `e164` - string (max_length 16) unique
 - `carrier` - ForeignKey (`route`)
 - `status` - string (choices=(portedin, portedout, portingin, portingout, disabled)
 - `ratecenter` - string (null=True) (automatically set)
 - `city` - string (null=True) (automatically set)
 - `state` - string (null=True) (automatically set)
 - `lata` - string (null=True) (automatically set)
 - `created_at` - datetime(utc)
 - `created_by` - uuid (external reference)

### Servers
1. Endpoints
  - /servers/
    - GET : paginated collection
    - POST : creates a server (required site-administrator privileges)
    - PATCH : updates the schema
    - PUT : idempotent create

2. Schema
```
class Server(models.Model):
    """ Yea, you should have used the id as the servergroup
        we'll change it later
    """

    # OpenSIPS dispatcher columns
    uri = models.TextField() # destination_col (sip:<ip|host>:port)
    weight = models.PositiveIntegerField(default=0) # OpenSIPS weight_col
    priority = models.PositiveIntegerField(default=0) # OpenSIPS priority_col
    socket = models.CharField(max_length=128) # OpenSIPS socket_col
    state = models.IntegerField(default=0) # OpenSIPS state_col (2=ping)
    attrs = models.CharField(max_length=128) # OpenSIPS attrs_col
    algorithm = models.PositiveIntegerField(default=8) #dispatcher alg
#    servergroup = models.ForeignKey(ServerGroup) # OpenSIPS setid

    # Descriptive
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    kind = models.TextField() # core,edge,carrier,account
    host = models.TextField(blank=True, null=True) # built from uri?
    port = models.PositiveIntegerField(default=5060)
    transport = models.TextField(default="udp")
    channels    = models.PositiveIntegerField(default=0)
    enabled     = models.BooleanField(default=True)

    class Meta:
        db_table = 'server'
```

### Routes
Provide container for multiple servers
1. Endpoints
  - /routes/
    - GET : paginated collection
    - POST : creates a number (required site-administrator privileges)
    - PATCH : updates the schema
    - PUT : idempotent create
  - /routes/<uuid>

2. Schema
  - name - string
  - description - string
  - created_at
  - created_by

#### RouteServers
relationship model (manytomany through=routeservers)
1. Endpoints
  - /routeservers/
    - GET / POST / PATCH / DELETE
  - /routeservers/<uuid>
    - GET / POST / PATCH / DELETE

2. Schema

### Orders
1. Endpoints
 - /orders
   - GET : only site-administrators will be able to fetch orders directly
   - NO OTHER METHODS FOR THIS RESOURCE
 - /orders/<uuid>/
   - GET : only site-administrators will be able to fetch orders directly
   - NO OTHER METHODS FOR THIS RESOURCE
   - *show the child order data based on the `kind` field*

 - /orders/<uuid>/files
   - GET : paginated collection of `OrderFiles` objects
   - POST: creates an `OrderFiles` resource (/orderfiles/<uuid>)
 - /orders/<uuid>/comments
   - GET : paginated collection of `OrderComments` objects
   - POST: creates an `OrderComments` resource (/ordercomments/<uuid>)

2. Schema
  - `uuid` - uuid
  - `kind` - string (this is set when the child resource is created)
  - `status` - string (choices=())
  - `account` - ForeignKey(`Account`)
  - `created_at` - datetime(utc)
  - `created_by` - uuid (external reference)

#### OrderFiles
1. Endpoints
 - /orderfiles/<uuid>
   - GET : returns the resource object

2. Schema
 - `order` - ForeignKey(`Order`)
 - `uri` - string (url to s3 file)
 - `created_at` - datetime(utc)
 - `created_by` - uuid

#### OrderComments
1. Endpoints
 - /ordercomments/<uuid>
   - GET : returns the resource object

2. Schema
 - `order` - ForeignKey(`Order`)
 - `text` - string (url to s3 file)
 - `created_at` - datetime(utc)
 - `created_by` - uuid

#### NumberOrder
Type of Order that is a OneToOne child
1. Endpoints
 - /numberorders/<uuid>
   - GET : returns the resource object
   - POST : creates a `NumberOrder` object (and the parent `Order`)

2. Schema
 - `number` - ForeignKey(`Number`)
 - `order` - ForeignKey(`Order`)
 - `created_at` - datetime(utc)
 - `created_by` - uuid

####
