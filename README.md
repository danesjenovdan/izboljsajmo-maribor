# DEPRECATION WARNING

This code is here only as an archive. It is not deployed at [Danes je nov dan](https://danesjenovdan.si) anymore. The kustomize folder remains, but it is not applied. You can use it if you want to run this on your own cluster, but it might make more sense for you to run it in a different way. For any questions, feel free to contact us. Good luck!

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
