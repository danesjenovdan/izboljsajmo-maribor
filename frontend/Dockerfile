# start with the nodejs image, calling it 'build'
FROM node:alpine as build
RUN apk add python make g++

# install node modules
# COPY package.json yarn.lock /
COPY package.json /
RUN yarn

# build assets
COPY . .
EXPOSE 3000

RUN yarn build

CMD ["yarn", "start"]

# # change base image
# FROM nginx:alpine

# # copy built files from the 'build' container into the nginx container
# COPY --from=build assets /usr/share/nginx/html/assets
# COPY --from=build dist /usr/share/nginx/html/dist
# COPY --from=build index.html /usr/share/nginx/html
