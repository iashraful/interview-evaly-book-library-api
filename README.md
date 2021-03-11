## Library Management System's API

**API Documentation is <a target="_blank" href="/docs/">here</a>**

### How to run? (Docker)
* Copy `.env.example` and save to `.env`. For now you don't need to update anything
* Run `docker-compose up --build -d`
* If anything goes wrong(db is not ready) then, run the following command,
```
docker-compose up api_server -d
```
### Traditional Approch
* Create a virtualenv with python 3.8+
* Copy `.env.example` and save to `.env`
* Update host, secret key and other necessary option available on `.env` file
* Active the virtualenv.
* Run `pip install -r requirements.txt`
* Run `python manage.py migrate`
* Run `python manage.py init_data` (Not mandatory. Just for creating some dummy data.)

### Features Added
* Two types of user role. Admin and Member.
* Admin can CRUD Books, Authors.
* Admin can Accept/Reject Book loans.
* Admin can update book loan when book returned.
* Admin can
* Admin can
* 
* 
* 
* Token Based Authentication (Auto expire in 30 min)
* Profile picture upload through API
