# Four App API (Last Update : 10 November,2018)

Please use README file for database settings.

## Order endpoints

| Endpoint name |  Link  | Method |  Purpose | Dependency | Access | DOC-CHECK |
|---|---|---|---|---|
|  Order Port | /accounts/<uuid:id>/orderports | POST | Create orderports with account | Account | | |
|  Single Order Port | /orderports/<uuid:id> | GET | Get single order port | | | |
|  Order Numbers  | /accounts/<uuid:id>/ordernumbers | POST | Create ordernumber with account | `Account`, `Number` | | |
|  Single Order Number  | /ordernumbers/<int:id> | GET | Get single order number | `Account` ,  `Number`| | |
|  Order Files   | /orders/<uuid:id>/files | POST | Upload files to attach to orders | `Order` | | |
|  Order Files   | /orders/<uuid:id>/files | GET | All Orderfiles for an order | `Order`, `Account` | | |
|  Order Files   | /orderfiles/<uuid:id>   | GET  | Get single order file descriptions | `OrderFile` | | |
|  Orders       | /accounts/<uuid:id>/orders | GET | Get all orders for an `Account` | `Account` | | |
|  Orders       | /orders | GET | Get all orders | | SUPER ADMIN | |
|  Orders       | /orders/<uuid:id>| GET | Get single order | | SUPER ADMIN | |
|  Order Comments      | /orders/<uuid:id>/comments | POST | Create comments on order | | | |
|  Order Comments      | /orders/<uuid:id>/comments | GET | Get all comments for order | | | | 

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


### HTTP REQUEST :  **POST  /orders/<uuid:id>/files**
***MULTIPART FILE UPLOAD***
###### params
```MULTIPART FILE UPLOAD
{
   "description": "this is a signed letter",
   "file": "<file data>",
   "kind": "bill",

}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| description      | false | |
| file      | true | |
| kind      | true | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "id": "859c0be6-1a7d-461f-9348-b48b9bbcefb7",
    "description": "this is a signed letter",
    "kind": "bill",
    "url": "https://<file location/bill.pdf",

    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/orderfiles/859c0be6-1a7d-461f-9348-b48b9bbcefb7",
        }
        "order": {
            "href": "http://127.0.0.1:8000/api/v1/orders/4930294032-4329049320-430294",
        }
    }
}
```


### HTTP REQUEST :  **GET  /orders/<uuid:id>/files**

###### params
```MULTIPART FILE UPLOAD
{
   "page":1,
   "limit" : 5
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page      | false | | 
| limit      | false | |

###### output

### possible response list:

1. HTTP_200_OK ----- New account creation 
2. HTTP_401_UNAUTHORIZED ----- Token is invalid
3. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "total_count": 4,
    "page": 1,
    "data": [
        {
            "id": "934bcd43-376b-4666-9128-4cb0979ec172",
            "description": "Sample description1",
            "kind": "bill",
            "url": "http://127.0.0.1:8000/api/v1/media/file/d7df0254-3215-4e30-875c-ee41b927f95a.pdf",
            "created_at": "2018-11-18T16:55:50.774712Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/orderfiles/934bcd43-376b-4666-9128-4cb0979ec172"
                },
                "order": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/2edce1a8-17a9-4b72-8727-b3213839927f"
                }
            }
        },
        {
            "id": "dd709902-1a2a-42c2-a702-77ed004160e2",
            "description": "Sample description5",
            "kind": "bill",
            "url": "http://127.0.0.1:8000/api/v1/media/file/3a743a3d-b750-4d81-a2cd-0c4aa9d18693.pdf",
            "created_at": "2018-11-18T16:55:46.102332Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/orderfiles/dd709902-1a2a-42c2-a702-77ed004160e2"
                },
                "order": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/2edce1a8-17a9-4b72-8727-b3213839927f"
                }
            }
        } 
    ]
}
```

### HTTP REQUEST :  **POST  /accounts/<uuid:id>/ordernumbers**

###### params
```json
{
   "number": "http://127.0.0.1:8000/api/v1/numbers/17135551212"
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| number      | true | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "id": 3,
    "number": "http://127.0.0.1:8000/api/v1/numbers/7135551214",
    "account": "http://127.0.0.1:8000/api/v1/accounts/46be2b6f-0d84-4fc4-a969-c03d14e02525",
    "created_at": "2018-11-15T17:48:28.545957Z",
    "status": "pending",
    "kind": "number",
    "_links": {
        "files": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7/files"
        },
        "comments": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7/comments"
        },
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/ordernumbers/3"
        },
        "order": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7"
        }
    }
}
```
 

### HTTP REQUEST :  **GET  /ordernumbers/<int:id>**

###### params
```json
{
   
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|       |  | |


###### output

### possible response list:

1. HTTP_200_OK -----  Success
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "id": 3,
    "number": "http://127.0.0.1:8000/api/v1/numbers/7135551214",
    "account": "http://127.0.0.1:8000/api/v1/accounts/46be2b6f-0d84-4fc4-a969-c03d14e02525",
    "created_at": "2018-11-15T17:48:28.545957Z",
    "status": "pending",
    "kind": "number",
    "_links": {
        "files": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7/files"
        },
        "comments": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7/comments"
        },
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/ordernumbers/3"
        },
        "order": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7"
        }
    }
}
```

### HTTP REQUEST :  **POST  /accounts/<uuid:id>/orderports**

###### params
```json
{
   "e164": "17135551212",
   "kind": "business",   (business, residential, toll free)
   "port_type": "partial", (partial, full)
   "ddd": "<date / time>",
   "btn": "17135551212",
   "name": "Company Name",
   "authorizer": "Jim Jones",
   "address1": "1132 Street",
   "address2": "Apt 1",
   "city": "Houston",
   "state": "Texas",
   "zip": "93402"
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| e164      | true | this is a number a customer wants to move |
| kind      | true | (business, residential, or tollfree) |
| port_type | true | (partial, full) |
| ddd | true | "desired due date" full date/time |
| btn | true | "billing telephone number" |
| name | true | company or individual name |
| authorizer | true | individual's name |
| address1 | true | |
| address2 | true | |
| city | true | |
| state | true | |
| zip | true | |
| state | false | (pending, foc, rejected) |

###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "id": 3,
    "account": "http://127.0.0.1:8000/api/v1/accounts/46be2b6f-0d84-4fc4-a969-c03d14e02525",
    "created_at": "2018-11-15T17:48:28.545957Z",
    "status": "pending",
    "kind": "business",
    "ddd": "2018-01-01T09:00:00",
    "btn": "17135551212",
    ...
    "_links": {
        "files": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7/files"
        },
        "comments": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7/comments"
        },
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/orderports/3"
        },
        "order": {
            "href": "http://127.0.0.1:8000/api/v1/orders/fdce10e0-541b-4e1a-b87d-dab66c48b0a7"
        }
    }
}
```

### HTTP REQUEST :  **GET  /orders**

###### params
```
{
    
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|       |  | | 


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "page": 1,
    "data": [
        {
            "id": "6c2b5c50-6264-47f8-93ab-e0dc332d00c1",
            "status": "pending",
            "kind": "number",
            "account": "http://127.0.0.1:8000/api/v1/accounts/b0e35727-416d-4be5-a4a2-5f1f77adb7fe",
            "created_at": "2018-11-06T13:56:59.603200Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/6c2b5c50-6264-47f8-93ab-e0dc332d00c1"
                },
                "account": {
                    "href": "http://127.0.0.1:8000/api/v1/accounts/b0e35727-416d-4be5-a4a2-5f1f77adb7fe"
                }
            }
        },
        {
            "id": "8035a893-179f-4f90-a545-faec87abd0ec",
            "status": "pending",
            "kind": "number",
            "account": "http://127.0.0.1:8000/api/v1/accounts/b0e35727-416d-4be5-a4a2-5f1f77adb7fe",
            "created_at": "2018-11-06T13:25:10.127112Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/8035a893-179f-4f90-a545-faec87abd0ec"
                },
                "account": {
                    "href": "http://127.0.0.1:8000/api/v1/accounts/b0e35727-416d-4be5-a4a2-5f1f77adb7fe"
                }
            }
        } 
    ],
    "total_count": 4
}
```



### HTTP REQUEST :  **GET  /orders/<uuid:id>**

###### params
```
{
    
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|       |  | | 


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "id": "6c2b5c50-6264-47f8-93ab-e0dc332d00c1",
    "status": "pending",
    "kind": "number",
    "account": "http://127.0.0.1:8000/api/v1/accounts/b0e35727-416d-4be5-a4a2-5f1f77adb7fe",
    "created_at": "2018-11-06T13:56:59.603200Z",
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/orders/6c2b5c50-6264-47f8-93ab-e0dc332d00c1"
        },
        "account": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/b0e35727-416d-4be5-a4a2-5f1f77adb7fe"
        }
    }
}
```



### HTTP REQUEST :  **POST  /orders/<uuid:id>/comments**

###### params
``` 
{
   "text": "Sample comment text" 
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| text      | True | | 


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "id": 4,
    "text": "I am comment3",
    "created_at": "2018-11-15T18:07:13.697962Z",
    "_links": {
        "ordercomments": {
            "href": "http://127.0.0.1:8000/api/v1/orders/9f3f8436-d8ea-48d2-9ed3-5f1b3fa95065/comments"
        }
    }
}

```



### HTTP REQUEST :  **GET  /orders/<uuid:id>/comments**

###### params
```
{
    
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|       |  | | 


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "data": [
        {
            "id": 1,
            "text": "I am comment3",
            "created_at": "2018-11-15T18:04:22.576546Z",
            "_links": {
                "ordercomments": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/9f3f8436-d8ea-48d2-9ed3-5f1b3fa95065/comments"
                }
            }
        },
        {
            "id": 2,
            "text": "I am comment3",
            "created_at": "2018-11-15T18:04:26.465463Z",
            "_links": {
                "ordercomments": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/9f3f8436-d8ea-48d2-9ed3-5f1b3fa95065/comments"
                }
            }
        },
        {
            "id": 3,
            "text": "I am comment3",
            "created_at": "2018-11-15T18:05:59.301227Z",
            "_links": {
                "ordercomments": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/9f3f8436-d8ea-48d2-9ed3-5f1b3fa95065/comments"
                }
            }
        },
        {
            "id": 4,
            "text": "I am comment3",
            "created_at": "2018-11-15T18:07:13.697962Z",
            "_links": {
                "ordercomments": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/9f3f8436-d8ea-48d2-9ed3-5f1b3fa95065/comments"
                }
            }
        }
    ],
    "page": 1,
    "total_count": 4
}
```
 
### HTTP REQUEST :  **GET  /orderfiles/<uuid:id>**

###### params
```
{
    
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|       |  | | 


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "data": [
        {
            "id": "f5f18541-b698-4462-adf5-a2dcd9d46787",
            "description": " description 1",
            "kind": "pdf",
            "url": "http://127.0.0.1:8000/api/v1/media/file/47d5d74d-40fd-450d-9a8e-9b8bc1498d52.pdf",
            "created_at": "2018-11-11T15:47:36.906565Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/orderfiles/f5f18541-b698-4462-adf5-a2dcd9d46787"
                },
                "order": {
                    "href": "http://127.0.0.1:8000/api/v1/orders/fa0ab799-5637-430e-b3aa-88930a53b185"
                }
            }
        }
    ],
}
```

### HTTP REQUEST :  **GET  /accounts/<uuid:id>/orders**

###### params
```
{

'limit':20,
'page':2    
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|    page   | false | | 
|    limit   | false | | 


###### output

### possible response list:

1. HTTP_200_OK ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- Token is invalid
4. HTTP_403_FORBIDDEN ----- No access to account

``` json
{
    "page": 1,
    "data": [
        {
            "id": "b8351186-6e87-4cf7-b694-c6a4e2c69ef1",
            "status": "pending",
            "kind": "staring4",
            "account": "http://127.0.0.1:8001/api/v1/accounts/ccb22d00-a286-432d-9ecf-228c169faec9",
            "created_at": "2018-12-20T21:32:03.251789Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8001/api/v1/orders/b8351186-6e87-4cf7-b694-c6a4e2c69ef1"
                },
                "account": {
                    "href": "http://127.0.0.1:8001/api/v1/accounts/ccb22d00-a286-432d-9ecf-228c169faec9"
                }
            }
        },
        {
            "id": "9be32a3a-1bc1-4422-8c66-adb412bccb61",
            "status": "pending",
            "kind": "core23",
            "account": "http://127.0.0.1:8001/api/v1/accounts/ccb22d00-a286-432d-9ecf-228c169faec9",
            "created_at": "2018-12-20T21:21:06.744476Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8001/api/v1/orders/9be32a3a-1bc1-4422-8c66-adb412bccb61"
                },
                "account": {
                    "href": "http://127.0.0.1:8001/api/v1/accounts/ccb22d00-a286-432d-9ecf-228c169faec9"
                }
            }
        },
        {
            "id": "efe1a7ea-684d-44a2-bbf8-3efaf2c97fb4",
            "status": "pending",
            "kind": "core2",
            "account": "http://127.0.0.1:8001/api/v1/accounts/ccb22d00-a286-432d-9ecf-228c169faec9",
            "created_at": "2018-12-20T21:15:33.647910Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8001/api/v1/orders/efe1a7ea-684d-44a2-bbf8-3efaf2c97fb4"
                },
                "account": {
                    "href": "http://127.0.0.1:8001/api/v1/accounts/ccb22d00-a286-432d-9ecf-228c169faec9"
                }
            }
        } 
    ],
    "total_count": 8
}
```
