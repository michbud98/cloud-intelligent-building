FROM nodered/node-red
USER root
RUN apk update && apk update && apk add --no-cache eudev-dev
USER node-red

WORKDIR /usr/src/node-red

RUN npm install --save  node-red-dashboard node-red-contrib-influxdb node-red-node-mysql \
node-red-contrib-boolean-logic node-red-configurable-ping @node-red-contrib-themes/theme-collection@v2.2
