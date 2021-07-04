## Library Management System's API

**API Documentation is <a target="_blank" href="/docs/">here</a>**

### How to run? (Docker)
* Copy `.env.example` and save to `.env`. For now you don't need to update anything
* Run `docker-compose up --build -d`
* If anything goes wrong(db is not ready) then, run the following command,
```
docker-compose up api_server -d
```
* Login to container shell. `docker-compose exec api_server sh`
* Run `python manage.py init_data`

### Traditional Approach
* Create a virtualenv with python 3.8+
* Copy `.env.example` and save to `.env`
* Update host, secret key and other necessary option available on `.env` file
* Active the virtualenv.
* Run `pip install -r requirements.txt`
* Run `python manage.py migrate`
* Run `python manage.py init_data` (Not mandatory. Just for creating some dummy data.)

### How the API could be useful?
As we already ran the `init_data` command. So, our test/fake data are ready. I assume that your project is running.
So, browse the at **/docs/**. .

**Admin Users**  
* Username: 'admin', Password: '1234'   
* Username: 'ashraful', Password: '1234'    

**Member Users**  
* Username: 'clark', Password: '1234'   
* Username: 'john', Password: '1234'   

**Author Users**  
* Username: 'test_author', Password: '1234'   
* Username: 'ahamed', Password: '1234'   

#### How to make a request?
* Get the token from `/api/jwt-token/` with your username and password
* Add the token to the http request header like following,
```
'Authorization': 'JWT <TOKEN HERE>'
```
* Hope you will get you data from the requested API.
* Default I set the token expire 30 minutes. You can change the value from settings and rerun the project.
* Before the token signature expired you can refresh the token from `/api/jwt-refresh/`. For more details see the browsable API doc.

#### How you can run the unittest?
The tests is already written for all the APIs with every role users. You can simply run the unittest by following command. 
Don't forget that all the commands must be run inside the container.  
```
python manage.py test 
```

Thank you :)
