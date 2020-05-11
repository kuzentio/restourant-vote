# Restourant rating application
## Summary
This prototype is designed for showing my proggraming skils. I focused more on Backend development, but that did not stop me from adding React as frontend framework.

Technology stack and responsibilities:

* `Django` - serve `/build/index.html/` where React application collect builded.

* `django-rest-framework` - serve API with next schema:
  * `api/restaurant/all/`[GET, POST]
  * `api/restaurant/<int:pk>/`[GET, PUT, DELETE]
  * `api/user-rating/`[POST]
  * `api/user-rating/<int:restaurant>/`[GET]
  
* `React` - react application is stores in `/frontend` folder, and during provision it starts `npm run build`, so after provision is finishes you could find `/frontend/build` folder with `index.html`

### Design tables: ###

In presented project we have 3 tables:
`Restaurant`
`RestaurantRating` - which is OnoToOne relatin to Restaurant, so we can think about it like continuation of Restaurant table.
`UserRating` - unique collection of user and restaurant, where we store rating itself.

### Data flow: ###

Each time user posts new rating, or updates existing user rating for restaurant we are updating RestaurantRating for this restaurant.

# Setup
## Requirements:
* Docker:2.2.0
* docker-compose:1.25.4
* opened 8000 port

## Instalation
To start installation proccess you can easelly run by:

`make start`

Please be patient because instalation will take a while. Docker should install all Backend dependencies as  well as install and build Frondend.

You can also run application is silent mode by:

`make start-in-deamon`

***Please note that apploication is not starting until frontend finish the build.***


After dependencies will be installed you can navigate to `http://localhost:8000/` an see admin login screen.
For creating superuser you can use make command for it:

`make create-superuser`

For filling database with demo data you could run:

`make initDB`

Then navigate to `http://localhost:8000/` and playaround with application.

As application runns in Docker I added some shortcuts for managing application:

`make test` - for runnign django unit tests inside docker container.

`make bash` - for navigatin to bash inside `web` container.

`make stop` - for stops docker-compose containers

`make destroy` - for compleatly remove all stuff related to this application from docker.
