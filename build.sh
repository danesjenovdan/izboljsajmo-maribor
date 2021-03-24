#!/bin/bash

sudo docker login rg.fr-par.scw.cloud/djnd -u nologin -p $SCW_SECRET_TOKEN

# BUILD AND PUBLISH BACKEND
sudo docker build -f backend/Dockerfile -t izboljsajmo-maribor-backend:latest backend
sudo docker tag izboljsajmo-maribor-backend:latest rg.fr-par.scw.cloud/djnd/izboljsajmo-maribor-backend:latest
sudo docker push rg.fr-par.scw.cloud/djnd/izboljsajmo-maribor-backend:latest

# BUILD AND PUBLISH FRONTEND
sudo docker build -f frontend/Dockerfile -t izboljsajmo-maribor-frontend:latest frontend
sudo docker tag izboljsajmo-maribor-frontend:latest rg.fr-par.scw.cloud/djnd/izboljsajmo-maribor-frontend:latest
sudo docker push rg.fr-par.scw.cloud/djnd/izboljsajmo-maribor-frontend:latest
