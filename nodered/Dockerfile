FROM nodered/node-red
USER root
RUN apk update && apk update && apk add --no-cache eudev-dev
USER node-red

COPY settings.js /data/settings.js
COPY nodered-flows/flows.json /data/flows.json

WORKDIR /usr/src/node-red

RUN npm install --save node-red-dashboard node-red-contrib-postgresql node-red-contrib-boolean-logic node-red-configurable-ping @node-red-contrib-themes/theme-collection@v2.2
