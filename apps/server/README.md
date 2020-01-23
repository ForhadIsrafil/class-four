# Four App API (Last Update : 23 October,2018)

## Base url: http://157.7.242.91:8010/api/v1

By using the following endpoint, URL is formed by baseurl + endpoint and API communication is performed.

Application must use Authentication key in header like :

```json

```

Please use README file for database settings.
## Main endpoints

| Endpoint name |  Link  | Method |  Purpose | Dependency | Access | DOC-CHECK |
|---|---|---|---|---|---|---|
 
|  AccountRoute | /accounts/<uuid:id>/routes | POST | Create route with account | `Account` | | |
|  AccountRoute  | /accounts/<uuid:id>/routes | GET | Get `Route` objects for a specific `Account` | `Account` | | |
|  Route  | /routes/<int:id> | GET | Single route | | | |
|  Route  | /routes/<int:id> | PATCH | Single route update | | | |
|  Route  | /routes/<int:id> | DELETE | Delete Single route | | | |

|  RouteServer  | /routes/<int:id>/servers | POST | Create `Server` for `Route` | `Route` and `Account` | Authorize `Account`| |
|  RouteServer  | /routes/<int:id>/servers | GET | Get `Server` for `Route` | `Route` | Authorize `Account`| |

|  Server | /servers | GET | All Server infos | `Server` | | OK |

|  Server | /servers/<int:id> |GET | Single Server | `Route` | | OK |
|  Server | /servers/<int:id> |PATCH | Single Server update info | `Route` | | OK |
|  Server | /servers/<int:id> |DELETE | Delete Single Server info | `Route` | | OK |

##### Sample response list for Whole project:

1. HTTP_201_CREATED
2. HTTP_400_BAD_REQUEST
3. HTTP_401_UNAUTHORIZED
4. HTTP_403_FORBIDDEN
5. HTTP_415_UNSUPPORTED_MEDIA_TYPE
6. HTTP_409_CONFLICT
7. HTTP_404_NOT_FOUND
8. HTTP_204_NO_CONTENT
9. HTTP_500_INTERNAL_SERVER_ERROR
10. HTTP_200_OK

## Endpoint detail:


### 1. [Account Endpoints](apps/account/README.md)
### 2. [Number Endpoints](apps/number/README.md)


### HTTP REQUEST :  **POST  /accounts/<uuid:id>/routes**

###### params
```json
{
   "name": "Customer Gateways"
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| name      | true | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "id": 2,
    "name": "Customer Gateways",
    "account": "http://127.0.0.1:8000/api/v1/accounts/bab1ad20-e1f5-4b9e-a638-9093c9e7dd34",
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/routes/2"
        }
    }
}
```

### HTTP REQUEST :  **GET  /accounts/<uuid:id>/routes**

###### params
```json
{
  "page": 10,
  "limit": 20    
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page     | False | | 
| limit     | False | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success  
2. HTTP_401_UNAUTHORIZED ----- Token is invalid
3. HTTP_403_FORBIDDEN ----- No access to account

``` json
 {
    "page": 1,
    "data": [
        {
            "id": 2,
            "name": "Customer BD Gateways",
            "account": "http://127.0.0.1:8000/api/v1/accounts/bab1ad20-e1f5-4b9e-a638-9093c9e7dd34",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/routes/2"
                }
            }
        },
        {
            "id": 1,
            "name": "Customer USA Gateways",
            "account": "http://127.0.0.1:8000/api/v1/accounts/bab1ad20-e1f5-4b9e-a638-9093c9e7dd34",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/routes/1"
                }
            }
        }
    ],
    "total_count": 2
}
```


### HTTP REQUEST :  **GET  /routes/<int:id>**

###### params
```json
{
    
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |


###### output

### possible response list:

1. HTTP_200_OK ----- success  
2. HTTP_401_UNAUTHORIZED ----- Token is invalid
3. HTTP_403_FORBIDDEN ----- No access to account

``` json
 {
    "id": 2,
    "name": "Sample route1",
    "account": "http://127.0.0.1:8000/api/v1/accounts/bab1ad20-e1f5-4b9e-a638-9093c9e7dd34",
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/routes/2"
        }
    }
}
```


### HTTP REQUEST :  **PATCH  /routes/<int:id>**

###### params
```json
{
    "name":"Updated Gateway"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| name      | false | |


###### output

### possible response list:

1. HTTP_200_OK ----- success  
2. HTTP_401_UNAUTHORIZED ----- Token is invalid
3. HTTP_403_FORBIDDEN ----- No access to account

``` json
 {
    "id": 2,
    "name": "Updated Gateway",
    "account": "http://127.0.0.1:8000/api/v1/accounts/bab1ad20-e1f5-4b9e-a638-9093c9e7dd34",
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/routes/2"
        }
    }
}
```


### HTTP REQUEST :  **DELETE  /routes/<int:id>**

###### params
```json
{
     
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |


###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- deleted 

``` json
 {
 
 }
```

### HTTP REQUEST :  **POST  /routes/<int:id>/servers**

###### params
```json
{
   "uri": "sip:127.0.0.1:8002;transport=udp",
   "weight":54,
   "priority":100,
   "socket":"string",
   "state":"state",
   "attrs":"string",
   "algorithm":8,
   "kind":"str",
   "name":"SIP Server",
   "description":"Test description",
   "host":"127.0.0.1",
   "port":8002,
   "transport":"udp",
   "channels":33,
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| uri      | true | ex: sip:127.0.0.1:5060;transport=udp |
| weight      | false | optional (default=0) |
| priority      | false | optional (default=0) |
| socket      | false | not viewable by account |
| state      | false | not viewable by account |
| attrs      | true | not viewable by account |
| name      | true | |
| description      | false | optional |
| algorithm      | false | default = 8 |
| kind      | false | not viewable by account and forced to 'account' |
| host      | true | can be parsed from uri? (127.0.0.10 |
| port      | true | can be parsed from uri? (5060) |
| transport      | true | can be parsed from uri? (default = udp) |
| channels      | true | |
| enabled      | false | read-only - not viewable by account |


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
        "id": 4,
        "uri": "sip:127.0.0.1:8002;transport=udp",
        "weight": 54,
        "priority": 100,
        "algorithm": 8,
        "name": "SIP server",
        "description": "Test description",
        "kind": "account",
        "host": "127.0.0.1",
        "port": 8002,
        "transport": "udp",
        "channels": 33, 
        "route": "http://127.0.0.1:8000/api/v1/routes/3",
        "_links": {
            "self": {
                "href": "http://127.0.0.1:8000/api/v1/servers/4"
            }
        }
}
```

### HTTP REQUEST :  **GET  /routes/<int:id>/servers**

###### params
```json
{
"limit": 20,
"page": 2
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page     | False | | 
| limit     | False | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success  
2. HTTP_401_UNAUTHORIZED ----- Token is invalid
3. HTTP_403_FORBIDDEN ----- No access to account

``` json
 {
    "total_count": 2,
    "page": 1,
    "data": [
        {
            "id": 4,
            "uri": "sip:127.0.0.1:8002;transport=udp",
            "weight": 54,
            "priority": 100,
            "algorithm": 8,
            "name": "SIP server",
            "description": "Test description",
            "kind": "account",
            "host": "127.0.0.1",
            "port": 8002,
            "transport": "udp",
            "channels": 33, 
            "route": "http://127.0.0.1:8000/api/v1/routes/3",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/servers/4"
                }
            }
        },
        {
            "id": 3,
            "uri": "sip:172.16.21.1:5070;transport=udp",
            "weight": 54,
            "priority": 100,
            "algorithm": 8,
            "name": "SIP server 2",
            "description": "",
            "kind": "account",
            "host": "172.16.21.1",
            "port": 5060,
            "transport": "udp",
            "channels": 33, 
            "route": "http://127.0.0.1:8000/api/v1/routes/3",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/servers/5"
                }
            }
        }
    ],
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
    "total_count": 6,
    "page": 1,
    "data": [
        {
            "id": 9,
            "uri": "sip:127.0.0.1:8002;transport=udp2",
            "weight": 54,
            "priority": 4916,
            "algorithm": 24231,
            "name": "Test Server",
            "description": "Sample description",
            "host": "127.0.0.1",
            "port": 8026,
            "transport": "udp",
            "channels": 23,
            "route": "http://127.0.0.1:8000/api/v1/routes/3",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/servers/9"
                }
            }
        },
        {
            "id": 8,
            "uri": "sip:127.0.0.1:8002;transport=udp",
            "weight": 54,
            "priority": 4916,
            "algorithm": 24231,
            "name": "Test Server",
            "description": "Sample description",
            "host": "127.0.0.1",
            "port": 8026,
            "transport": "udp",
            "channels": 23,
            "route": "http://127.0.0.1:8000/api/v1/routes/3",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/servers/8"
                }
            }
        } 
    ]
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
 

### HTTP REQUEST :  **PATCH  /servers/<int:id>**

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
| uri      | false | |
| weight      | false | |
| priority      | false | |
| socket      | false | |
| state      | false | |
| attrs      | false | |
| name      | false | |
| description      | false | |
| algorithm      | false | |
| kind      | false | |
| host      | false | |
| port      | false | |
| transport      | false | |
| channels      | false | |
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
 
 

###HTTP REQUEST :  **DELETE  /servers/<int:id>**

###### params
```json
{

}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|        |  | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT----- Successfully deleted


``` json
{

}
```
