# Four App API : Number (Last Update : 23 October,2018)

## Number endpoints

| Endpoint name |  Link  | Method |  Purpose | DOC-CHECK |
|---|---|---|---|---|
|  Number | /numbers |POST | Create Number resource (superadmin) | OK |
|  Number | /numbers |GET | All number list | OK |
|  Number | /numbers/<e164:id> |GET | All number list | OK |
|  Number | /numbers/<e164:id> |PATCH | Update single number | OK |
|  Number | /numbers/<e164:id> |DELETE | Delete single number | OK |
|  AccountNumber | /accounts/<uuid:id>/numbers |POST | Creating AccountNumber resource that assigns a number to an account | OK |
|  AccountNumber | /accounts/<uuid:id>/numbers |GET | All number list for an account | OK |
|  AccountNumber | /accountnumbers/<uuid:accountnumber_id> |GET | Single account number information | OK |
|  AccountNumber | /accountnumbers/<uuid:accountnumber_id> |DELETE | Deleting Single accountnumber information | Not yet |
|  AccountNumber | /accountnumbers/<uuid:accountnumber_id>/lidb |PUT | Idempotent LIDB create | OK |
|  AccountNumber | /accountnumbers/<uuid:accountnumber_id>/lidb |GET | Getting all lidb for an account | OK |
|  E911 | /accountnumbers/<uuid:id>/e911 |PUT | Adding new e911 to accountnumber| OK |
|  E911 | /accountnumbers/<uuid:id>/e911 |GET | Getting all e911 to accountnumber| OK |

## Endpoint detail:


###HTTP REQUEST :  **POST  /numbers**

###### params
```json
{
    "e164": "7135551212",
    "status":"portedin"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| e164      | true | |
| status      | true | |

###### output

### possible response list:

1. HTTP_201_CREATED----- Created


``` json
{
    "id": "859c0be6-1a7d-461f-9348-b48b9bbcefb7",
    "e164": "7135551212",
    "status": "portedin"
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/numbers/7135551212"
        }
    }
}
```

###HTTP REQUEST :  **GET  /numbers**

###### params
```json
{
   "page": 1,
   "page_size": 20,
   "keyword": "73658995"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page      | false | |
| keyword    | false | for searching number | |
| limit      | false | Number of data per page |

###### output

### possible response list:

1. HTTP_200_OK----- Success


``` json
{
    "results": [
        {
            "id": "71985e90-c5b8-4349-85b9-82238f4ffd8d",
            "e164": "(346)338-0041",
            "status": "portedin",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/numbers/(346)338-0041"
                }
            }
        },
        {
            "id": "cca24292-b561-4455-a929-c25b0f238798",
            "e164": "(346)338-0023",
            "status": "portedin",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/numbers/(346)338-0023"
                }
            }
        },
        {
            "id": "37fb7f37-1b51-4dd4-9236-b9e610ec2e94",
            "e164": "(346)338-0016",
            "status": "portedin",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/numbers/(346)338-0016"
                }
            }
        },
        {
            "id": "3cf002ae-d7ce-48e1-9207-26feaa64d013",
            "e164": "(346)338-0053",
            "status": "portedin",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/numbers/(346)338-0053"
                }
            }
        },
        {
            "id": "2d1d715e-f99d-4d0d-818c-2ae41354b677",
            "e164": "(346)338-0042",
            "status": "portedin",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/numbers/(346)338-0042"
                }
            }
        }
    ],
    "next": "http://127.0.0.1:8000/api/v1/numbers?page=3&page_size=5",
    "count": 34,
    "limit": 20,
    "previous": "http://127.0.0.1:8000/api/v1/numbers?page_size=5"
}
```

###HTTP REQUEST :  **GET  /numbers/<e164:id>**

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_200_OK----- Success


``` json
{
    "id": "859c0be6-1a7d-461f-9348-b48b9bbcefb7",
    "e164": "7135551212",
    "status": "portedin"
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/numbers/7135551212"
        }
    }
}
```

## AccountNumber endpoints

###HTTP REQUEST :  **POST  /accounts/<uuid:id>/numbers**

###### params
```json
{
    "number": "http://127.0.0.1:8000/api/v1/numbers/7135551212"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| number      | true | number e164 |

###### output

### possible response list:

1. HTTP_201_CREATED----- Created


``` json
{
    "id": "859c0be6-1a7d-461f-9348-b48b9bbcefb7",
    "account": "http://127.0.0.1:8000/api/v1/accounts/3fh349f0-4hf093hf-f43hf3/",
    "number": "http://127.0.0.1:8000/api/v1/numbers/5423698719",
    "created_at": "2018-10-08T18:32:14.842080Z"
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/accountnumbers/859c0be6-1a7d-461f-9348-b48b9bbcefb7"
        },
        "lidb": {
            "href": "http://127.0.0.1:8000/api/v1/accountnumbers/859c0be6-1a7d-461f-9348-b48b9bbcefb7/lidb"
        }
    }
}
```


###HTTP REQUEST :  **GET  /accounts/<uuid:id>/numbers**

###### params
```json
{
   "page": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page      | false | |

###### output

### possible response list:

1. HTTP_200_OK----- Success


``` json
{
    "limit": 20,
    "previous": null,
    "results": [
        {
            "id": "2e73673e-bf62-463a-8947-6c44abdf18fd",
            "account": "http://127.0.0.1:8000/api/v1/accounts/391d2233-fe88-463f-a8f2-4ea6c3d9e2f8",
            "number": "http://127.0.0.1:8000/api/v1/numbers/3463380051",
            "created_at": "2019-04-18T20:49:44.440064Z",
            "_links": {
                "e911": {
                    "href": "http://127.0.0.1:8000/api/v1/accountnumbers/2e73673e-bf62-463a-8947-6c44abdf18fd/e911"
                },
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/accountnumbers/2e73673e-bf62-463a-8947-6c44abdf18fd"
                },
                "lidb": {
                    "href": "http://127.0.0.1:8000/api/v1/accountnumbers/2e73673e-bf62-463a-8947-6c44abdf18fd/lidb"
                }
            }
        } 
    ],
    "next": null,
    "count": 5
}
```


###HTTP REQUEST :  **GET  /accountnumbers/<uuid:acctnum_id>**

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

1. HTTP_200_OK----- Success


``` json
{
    "id": "1cb55b31-07fe-430a-a149-6e147224db3e",
    "account": "http://127.0.0.1:8000/api/v1/accounts/5aba16cb-04c4-4ebe-8236-d70e50842a32",
    "number": "http://127.0.0.1:8000/api/v1/numbers/7135551214",
    "created_at": "2018-10-19T19:10:44.296922Z",
    "_links": {
        "e911": {
            "href": "http://127.0.0.1:8000/api/v1/accountnumbers/1cb55b31-07fe-430a-a149-6e147224db3e/e911"
        },
        "lidb": {
            "href": "http://127.0.0.1:8000/api/v1/accountnumbers/1cb55b31-07fe-430a-a149-6e147224db3e/lidb"
        },
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/accountnumbers/1cb55b31-07fe-430a-a149-6e147224db3e"
        }
    }
}
 ```


###HTTP REQUEST :  **PUT  /accountnumbers/<uuid:accountnumber_id>/lidb**

###### params
```json
{

}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|    name    | true | |
|    kind    | true | |

###### output

### possible response list:

1. HTTP_200_OK----- Success


``` json
{
    "name": "Sample Lidb name",
    "kind": "residential",
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/accountnumbers/1cb55b31-07fe-430a-a149-6e147224db3e/lidb"
        }
    }
}

 ```


###HTTP REQUEST :  **GET  /accountnumbers/<uuid:accountnumber_id>/lidb**

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

1. HTTP_200_OK----- Success


``` json
{
    "total_count": 7,
    "data": [
        {
            "name": "Sample Lidb name",
            "kind": "residential",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/accountnumbers/1cb55b31-07fe-430a-a149-6e147224db3e/lidb"
                }
            }
        },
        {
            "name": "Sample Lidb name",
            "kind": "residential",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/accountnumbers/1cb55b31-07fe-430a-a149-6e147224db3e/lidb"
                }
            }
        }
    ],
    "page": 1
}

 ```
