# izboljsajmo-maribor

### INSTALL ###

* docker-compose build
* docker-compose up
* docker-compose exec mb-api python manage.py migrate
* docker-compose exec mb-api python manage.py createsuperuser
* docker-compose exec mb-api python manage.py seed
* restart docker-compose


### RUN ###

* docker-compose up

###
* mb-api -> localhost:8000

## Deploy

There is a `kustomize` folder, have a look. Flux CD watches this repo, there is a
GitHub Actions yaml in `.github/workflows` that builds and uploads the image on
every **push** event.
