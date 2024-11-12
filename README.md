This api is integrated with Doordash drive's api, which offers delivery services to businesses. Any front-end can use this api to create userId, getting quote for deliveries, accept it and get updates of it.

#TODO:
1. Add Documentation.
2. CORS configuration in django settings.
3. Profilling and error handling.
4. Authentication.


A a rough Documentaion of how to use it.
How to use?
/api/auth : Enter information to create a user in the database.
		{first_name, 
		Last_name,
		Address,
		Phone_number,
		Username,
		Password}

/api/getQuote: Get Quote for the delivery.
		{Authorization: Bearer JWT-token}

/api/userinfo: Get information of the user.
		{Authorization: Bearer JWT-token}

/api/accept: Accept the given Quote.
		{Authorization: Bearer JWT-token}
/api/status: Get status of your delivery.
		{Authorization: Bearer JWT-token}


/api/token: Get refresh and access token.
		{username,
		Password}
/api/token/refresh: Get access token when it expires.
		{Refresh Token}
