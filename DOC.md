# Prototype L template

The goal of this project is to allow a fast prototype of any generic app that you have in mind. It is still far from ideal but ideally, almost every minor demo of a product should be only a day of work away. 
Idea is to have all the generic operations and features already onboarded while a lot of other feature pluggable easily. 

Two things 

1. I am not sure what all kind of apps I will have to make in future. I may be grossly specific. I would say it out clearly here - app that we are trying to make is one with a frontend that makes a call to backend which does bunch of computation at the back and directs data to persistence layer. 

2. Although ultimate goal is to make it all very easily configurable. Initially, it is just going to be a lot of manual work. We will slowly document everything along the way. This is why this document exists. 


## Offerings

1. db - PSQL db running in a docker with postgis extension
2. db_test_app - A toy app that can be used to make calls to database from outside docker environment. 
3. app-migrations - An django project with an app for db migrations. 
4. pdffer - In same django project, there is an app call pdffer to serve api requests for db


## Setup

### getting up our apps

1. Install docker
2. in a terminal, hit `docker-compose up --build`, see the db and pdffer get up. 

### test external connection to db 

1. **cd into db_test_app** and run `docker build . -t app && docker run --net=host app`. Now you can use this flask app as you wish for further testing and mockup

    ### Further nit-grits

- Add your migrations to **app/appmigrations** and run `docker-compose run --rm app python manage.py makemigrations` followed by `docker-compose run --rm app python manage.py migrate`. 
- In fact, for nitty commands on app. use 
    `docker-compose run --rm app <your command goes here>`
- To log into machines, run `docker ps` and get container Name (or id). e.g. 
    - run `docker exec -it pl_template_app_1 /bin/sh` for logging into app server. you may want to do this to get inside python environment that is used in our django app etc.
    - run `docker exec -it pl_template_db_1 /bin/sh` for logging into db server. you may want to do this to get inside psql server and play around. However you need to follow few more things **inside container**
        - run `su postgres`
        - run `psql` and you must be in. 

- to populate the db with dummy values, there is a script written in `app/appmigrations/fake_data.py` which is run by a django command `docker-compose run --rm app python manage.py populate_db`. change it, use it etc
- to check if model_ops.py is fine, run by a django command `docker-compose run --rm app python manage.py test_model_ops`. It runs the test file in app/pdffer/model_ops.py.
- **alert!!** - based on criticality of data, you may want to back up your data first. To delete all the data from tables, run `docker-compose run --rm app python manage.py flush`.
- **alert!!** - based on criticality of data, you may want to back up your data first. To delete all the table of this db, run `docker-compose run --rm app python manage.py delete_all_tables`. If you want to recreate table after deletion run `docker-compose run --rm app python manage.py delete_all_tables --recreate`  this is a custom command, just like populate_db. go check it out.  

- to add python dependency, you would have to change requirements.txt and re-run docker compose. 
- `docker-compose run --rm app python manage.py collectstatic` to collectstatic files in one place. you need to run it for production build.
- You can use bootstrap ui if you need. 

## Useful links

- make header and footer stick to the two ends of viewport and leaving rest of the space for middle component. - [solution](https://stackoverflow.com/questions/65696507/css-creating-fixed-header-and-footer-while-having-dynamic-context-using-flexbox)
