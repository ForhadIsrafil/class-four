# Four App API : Account (Last Update : 16 October,2018)

## Account endpoints

| Endpoint name |  Link  | Method |  Purpose | DOC-CHECK |
|---|---|---|---|---|
|  Account | /check-familyname |GET | Check if the family name / account name is free to use | OK |
|  Account | /accounts |POST | Creating new account | OK |
|  Account | /accounts |GET | All account list | OK |
|  Account | /accounts/<uuid:id> |GET | Single account information | OK |
|  Account | /accounts/<uuid:id> |PATCH | Updating Single account information | OK |
|  Account | /accounts/<uuid:id> |DELETE | Deleting Single account information | OK |

|  OktaSignup | /signup |POST | Create user In okta domain | OK |
|  OktaSignin | /signin> |POST | User Signin | OK |
|  ActivateUserAccount | /logout |POST | Activate new created user  | OK |
|  OktaLogout | /active-account/<str:userid> |DELETE | Logout user | OK |





## Endpoint detail:



###HTTP REQUEST :  **GET  /check-familyname**

###### params
```json
{
	"family_name":"Web Account"
	
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| family_name      | true | |

###### output

### possible response list:

1. HTTP_200_OK----- Success


``` json
{
    "allow": true
}
```



### HTTP REQUEST :  **POST  /accounts**

###### params
```json
{
   "name": "Test Name",
   "description":"Test description"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| name      | true | |
| description      | false | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- New account creation
2. HTTP_400_BAD_REQUEST ----- Required fields not given
3. HTTP_401_UNAUTHORIZED ----- The request user has invalid permissions

``` json
{
    "id": "919b0c3d-d141-42fd-adff-651b620caccc",
    "name": "Test Name",
    "description": "Test description",
    "enabled": true,
    "created_at": "2018-10-11T02:07:20.468078Z",
    "_links": {
        "accountServers": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/919b0c3d-d141-42fd-adff-651b620caccc/servers"
        },
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/919b0c3d-d141-42fd-adff-651b620caccc"
        },
        "accountNumbers": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/919b0c3d-d141-42fd-adff-651b620caccc/numbers"
        }
    }
}
```


###HTTP REQUEST :  **GET  /accounts**

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
    "data": [
        {
            "id": "919b0c3d-d141-42fd-adff-651b620caccc",
            "name": "Test Name3",
            "description": "Test description3",
            "enabled": true,
            "created_at": "2018-10-11T02:07:20.468078Z",
            "_links": {
                "accountServers": {
                    "href": "http://127.0.0.1:8000/api/v1/accounts/919b0c3d-d141-42fd-adff-651b620caccc/servers"
                },
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/accounts/919b0c3d-d141-42fd-adff-651b620caccc"
                },
                "accountNumbers": {
                    "href": "http://127.0.0.1:8000/api/v1/accounts/919b0c3d-d141-42fd-adff-651b620caccc/numbers"
                }
            }
        },
        {
            "id": "1a2a874a-ad1d-46e7-9977-f4d55d00426f",
            "name": "Test Name3",
            "description": "Test description3",
            "enabled": true,
            "created_at": "2018-10-11T02:01:10.601878Z",
            "_links": {
                "accountServers": {
                    "href": "http://127.0.0.1:8000/api/v1/accounts/1a2a874a-ad1d-46e7-9977-f4d55d00426f/servers"
                },
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/accounts/1a2a874a-ad1d-46e7-9977-f4d55d00426f"
                },
                "accountNumbers": {
                    "href": "http://127.0.0.1:8000/api/v1/accounts/1a2a874a-ad1d-46e7-9977-f4d55d00426f/numbers"
                }
            }
        }
    ],
    "page": "1",
    "total_count": 2
}
```


###HTTP REQUEST :  **GET  /accounts/<uuid:id>**

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
    "id": "7464dd7f-fa53-4bb9-be84-76c21e6ad6c6",
    "name": "Test Name3",
    "description": "Test description3",
    "enabled": true,
    "created_at": "2018-10-08T18:32:14.842080Z",
    "_links": {
        "accountServers": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/7464dd7f-fa53-4bb9-be84-76c21e6ad6c6/servers"
        },
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/7464dd7f-fa53-4bb9-be84-76c21e6ad6c6"
        },
        "accountNumbers": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/7464dd7f-fa53-4bb9-be84-76c21e6ad6c6/numbers"
        }
    }
}
```


###HTTP REQUEST :  **PATCH  /accounts/<uuid:id>**

###### params
```json
{
    "name": "NEW Test Name",
   "description":"NEW Test description",
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| name      | false | |
| description      | false | |

###### output

### possible response list:

1. HTTP_200_OK----- Success


``` json
{
    "id": "7464dd7f-fa53-4bb9-be84-76c21e6ad6c6",
    "name": "NEW Test Name",
    "description": "NEW Test description",
    "enabled": true,
    "created_at": "2018-10-08T18:32:14.842080Z",
    "_links": {
        "accountServers": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/7464dd7f-fa53-4bb9-be84-76c21e6ad6c6/servers"
        },
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/7464dd7f-fa53-4bb9-be84-76c21e6ad6c6"
        },
        "accountNumbers": {
            "href": "http://127.0.0.1:8000/api/v1/accounts/7464dd7f-fa53-4bb9-be84-76c21e6ad6c6/numbers"
        }
    }
}
```


###HTTP REQUEST :  **DELETE  /accounts/<uuid:id>**

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



###HTTP REQUEST :  **PUT  /accountnumbers/<uuid:id>/e911**

###### params
```json
{
   "address1":"string",
   "address2":"string",
   "state":"jp",
   "city":"string",
   "zipcode":"1206",
   "zipcode2":"1203",
   "comment":"string"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|     address1   | true | |
|     address2   | true | |
|     state   | true | |
|     city   | true | |
|     zipcode   | true | |
|     zipcode2   | true | |
|     comment   | true | |

###### output

### possible response list:

1. HTTP_200_OK----- Successfully added


``` json
{
    "id": 8,
    "address1": "string",
    "address2": "string",
    "city": "string",
    "state": "ua",
    "zipcode": "1206",
    "zipcode2": "1204",
    "comment": "hahaha",
    "created_at": "2018-10-21T18:20:41.297634Z",
    "_links": {
        "self": {
            "href": "http://127.0.0.1:8000/api/v1/accountnumbers/c6a1c9ed-c62c-46ed-8c07-2ca16acc9250/e911"
        }
    }
}
```


###HTTP REQUEST :  **GET  /accountnumbers/<uuid:id>/e911**

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

1. HTTP_200_OK


``` json
{
    "page": 1,
    "total_count": 8,
    "data": [
        {
            "id": 1,
            "address1": "string",
            "address2": "string",
            "city": "string",
            "state": "ua",
            "zipcode": "1206",
            "zipcode2": null,
            "comment": "hahaha",
            "created_at": "2018-10-21T17:36:45.646649Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/accountnumbers/c6a1c9ed-c62c-46ed-8c07-2ca16acc9250/e911"
                }
            }
        },
        {
            "id": 2,
            "address1": "string",
            "address2": "string",
            "city": "string",
            "state": "ua",
            "zipcode": "1206",
            "zipcode2": null,
            "comment": "hahaha",
            "created_at": "2018-10-21T17:37:15.420344Z",
            "_links": {
                "self": {
                    "href": "http://127.0.0.1:8000/api/v1/accountnumbers/c6a1c9ed-c62c-46ed-8c07-2ca16acc9250/e911"
                }
            }
        }
    ]
}
```


###HTTP REQUEST :  **POST  /signup**

###### params
```json
{
	"firstname": "islando",
	"lastname": "cooper",
	"email": "gopu@quick-mail.online",
	"password": "Testoktauser2019"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
|     firstname   | true | |
|     lastname   | true | |
|     email   | true | |
|     password   | true | |

###### output

### possible response list:

1. HTTP_201 Created----- Successfully added


``` json
{
    "success": "Your account is successfully created!.Please check your email to activate your account."
}
```

###HTTP REQUEST :  **POST  /signin**

###### params
```json
{
	"email": "fukugalum@virtual-email.comm",
	"password": "Testoktauser2019"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| email   | true | |
| password   | true | |

###### output

### possible response list:

1. HTTP_201 Created----- Successfully added


``` json
{
    "status": "SUCCESS",
    "_embedded": {
        "user": {
            "passwordChanged": "2019-03-12T17:15:43.000Z",
            "id": "00ujpi19t60lJOIhX0h7",
            "profile": {
                "locale": "en",
                "timeZone": "America/Los_Angeles",
                "login": "common00003@gmail.com",
                "firstName": "Common",
                "lastName": "User"
            }
        }
    },
    "expiresAt": "2019-03-12T17:26:06.000Z",
    "sessionToken": "102wlYiM2zUTiO-63G39zUlAg"
}
```

###HTTP REQUEST :  **POST  /active-account/<str:userid>**

###### params
```json

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| email   | true | |
| password   | true | |

###### output

### possible response list:

1. HTTP_201 Created----- "success": "Your account is successfully activated!.


``` json
{
    "success": "Your account is successfully activated!."
}
```

###HTTP REQUEST :  **DELETE  /signout**

###### params
```json
{
  "Authorization": "Bearer 201110z4h4tPjcS2qaSFf6svpxVZaraI0ETfylr1J6gazqA9bnXZV7U"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| Authorization   | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT----- NO_CONTENT


``` json
{
    
}
```



###HTTP REQUEST :  **POST  /forget-password**

###### params
```json

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| email   | true | | 

###### output

### possible response list:

1. HTTP_201 Created----- Successfully added


``` json
{
    "success": "Please check your email to reset your password."
}
```



###HTTP REQUEST :  **POST  /reset-password**

###### params
```json

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| recovery_token   | true | | 
| new_password   | true | | 

###### output

### possible response list:

1. HTTP_201 Created----- Successfully added


``` json
{
'success': 'Password successfully reset.Please login again'
}
```