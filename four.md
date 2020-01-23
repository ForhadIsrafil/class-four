# Four App API (Last Update : 8 October,2018)

## Base url: http://157.7.242.91:8010/api/v1

By using the following endpoint, URL is formed by baseurl + endpoint and API communication is performed.

Application must use Authentication key in header like :

```json

```

Please use README file for database settings.
## Main endpoints

| Endpoint name |  Link  | Method |  Purpose | DOC-CHECK |
|---|---|---|---|---|
|  Account | /accounts |POST | Creating new account | OK |
|  Account | /accounts |GET | All account list | OK |
|  Account | /accounts/<uuid:id> |GET | Single account information | OK |
|  Account | /accounts/<uuid:id> |PATCH | Updating Single account information | OK |
|  Account | /accounts/<uuid:id> |DELETE | Deleting Single account information | OK |
|  AccountNumber | /accounts/<uuid:id>/numbers |POST | Creating AccountNumber resource that assigns a number to an account | OK |
|  AccountNumber | /accounts/<uuid:id>/numbers |GET | All number list for an account | OK |
|  AccountNumber | /accountnumbers/<uuid:accountnumber_id> |GET | Single account number information | OK |
|  AccountNumber | /accountnumbers/<uuid:accountnumber_id> |DELETE | Deleting Single accountnumber information | OK |
|  AccountNumber | /accountnumbers/<uuid:accountnumber_id>/lidb |PUT | Idempotent LIDB create | OK |
|  AccountNumber | /accountnumbers/<uuid:accountnumber_id>/e911 |PUT | Idempotent e911 entry| OK |
|  Number | /numbers |POST | Create Number resource (superadmin) | OK |
|  Number | /numbers |GET | All number list | OK |
|  Number | /numbers/<e164:id> |GET | All number list | OK |
|  Number | /numbers/<e164:id> |PATCH | Update single number | OK |
|  Number | /numbers/<e164:id> |DELETE | Delete single number | OK |
|  Server | /servers |POST | Creating server | OK |
|  Server | /servers |GET | All server  infos | OK |
|  Server | /servers/<int:id> |GET | Single Server | OK |
|  AccountServer | /accountservers/<uuid:id> |GET | Single AccountServer information | Not yet |
|  AccountServer | /accountservers/<uuid:id> |PATCH | Update single accountserver | Not yet |
|  AccountServer | /accountservers/<uuid:id> |DELETE | Delete single accountserver | Not yet |


##### Sample response list for Whole project:

1. HTTP_201_CREATED
2. HTTP_400_BAD_REQUEST
3. HTTP_401_UNAUTHORIZED
4. HTTP_415_UNSUPPORTED_MEDIA_TYPE
5. HTTP_409_CONFLICT
6. HTTP_404_NOT_FOUND
7. HTTP_204_NO_CONTENT
8. HTTP_500_INTERNAL_SERVER_ERROR
9. HTTP_200_OK




## Endpoint detail:


### 1. [Account Endpoints](apps/account/README.md)
### 2. [Number Endpoints](apps/number/README.md)

### HTTP REQUEST :  **POST  /servers**

###### params
```json
{
   "uri": "sip:127.0.0.1:8002;transport=udp",
   "weight":54,
   "priority":100,
   "socket":"0",
   "state":1,
   "attrs":"",
   "algorithm":8,
   "name":"SIP Server",
   "description":"Test description",
   "kind":"carrier",
   "host":"127.0.0.1",
   "port":8002,
   "transport":"udp",
   "channels":33,
   "enabled": true
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| uri      | true | |
| weight      | true | |
| priority      | true | |
| socket      | true | |
| state      | true | |
| attrs      | true | |
| name      | true | |
| description      | true | |
| algorithm      | true | |
| kind      | true | |
| host      | true | |
| port      | true | |
| transport      | true | |
| channels      | true | |
| enabled      | false | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given


``` json
{
   "id": 3,
   "uri": "sip:127.0.0.1:8002;transport=udp",
   "weight":54,
   "priority":100,
   "socket":"0",
   "state":1,
   "attrs":"",
   "algorithm":8,
   "name":"SIP Server",
   "description":"Test description",
   "kind":"carrier",
   "host":127.0.0.1,
   "port":8002,
   "transport":"udp",
   "channels":33,
   "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/servers/3"
        }
    }
}
```
 

### HTTP REQUEST :  **GET  /servers**

###### params
```json
{
    
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|      |  | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success  


``` json
 {
    "total_count": 5,
    "data": [
        {
            "id": 5,
            "uri": "http://www.pierobon.org/iis/review1.htm.html#one",
            "weight": 54,
            "priority": 4916,
            "socket": "32.213.170.129",
            "state": 212,
            "attrs": "Sample attrs",
            "algorithm": 24231,
            "name": "Test Server",
            "description": "Sample description",
            "kind": "Sample kind",
            "host": "127.0.0.1",
            "port": 8026,
            "transport": "udp",
            "channels": 23,
            "enabled": true,
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/servers/5"
                }
            }
        },
        {
            "id": 4,
            "uri": "http://www.pierobon.org/iis/review1.htm.html#one",
            "weight": 54,
            "priority": 4916,
            "socket": "32.213.170.129",
            "state": 212,
            "attrs": "Sample attrs",
            "algorithm": 24231,
            "name": "Test Server",
            "description": "Sample description",
            "kind": "Sample kind",
            "host": "127.0.0.1",
            "port": 8026,
            "transport": "udp",
            "channels": 23,
            "enabled": true,
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/servers/4"
                }
            }
        } 
    ],
    "page": 1
}
```
 


### HTTP REQUEST :  **GET  /servers/<int:id>**

###### params
```json
{
    
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|      |  | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 
2. Http404 ----- Not found


``` json
 {
    "id": 3,
    "uri": "http://www.pierobon.org/iis/review1.htm.html#one",
    "weight": 54,
    "priority": 4916,
    "socket": "32.213.170.129",
    "state": 212,
    "attrs": "Sample attrs",
    "algorithm": 24231,
    "name": "Test Server",
    "description": "Sample description",
    "kind": "Sample kind",
    "host": "127.0.0.1",
    "port": 8026,
    "transport": "udp",
    "channels": 23,
    "enabled": true,
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/servers/3"
        }
    }
}
```
 
