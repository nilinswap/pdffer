# pdffer
a pdf generation tool

## Set up db
1. install docker
2. in one terminal, run `docker-compose up --build`. This gets the db up and running. 
3. In another terminal, run `docker-compose run --rm app python manage.py migrate`. In fact use this command to run anything adhoc. 
4. now cd into db_test_app and run `docker build . -t app && docker run --net=host app`.  

### Adhoc commands

docker-compose run --rm app python manage.py startapp pdffer

docker-compose run --rm app python manage.py populate_db

## Set up application

1.  `docker-compose up --build` and go to http://localhost:8000/api

## pdf

### wkHtmltopdf docker
Apart from puppdf, took lessons from [this article](https://sasablagojevic.com/setting-up-wkhtmltopdf-on-docker-alpine-linux)

- [email sending](https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151)

## TODO

### Registration

- use next_url redirection for logout and signup

- it needs csrf check


### General
- make auth a library
- make emailS a library




apis 

X Identify Code Decouple
- Code Decouple
- Tests
- Documentation
- make ui to consume all of above. 
- Think credits, billing, pricing.

Read 

Email Verification
Cost analysis per pdf
Payments integration
Look at all test cases around auth


email verify


Next stage todo
1. review areas for security flaws like 
    - verification email should not give away so much.
    - people can hit and try verification link etc.

2. get secret from kms or something. right now one has to go into docker container and add password manually for email

3. add multi-level logs


## Hooks

- Write a documentation explaining everything in auth. 
- Learn auth from supertoken. 
- Learn nextjs react
- learn [nextjs examples.](https://nextjs.org/docs/basic-features/pages#static-generation-recommended)



