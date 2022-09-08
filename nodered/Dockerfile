FROM nodered/node-red
USER root
RUN apk update && apk add --no-cache eudev-dev
USER node-red

WORKDIR /usr/src/node-red

RUN npm install --save  node-red-dashboard
RUN npm install --save  node-red-contrib-influxdb
RUN npm install --save  node-red-node-mysql
RUN npm install --save  node-red-contrib-boolean-logic
RUN npm install --save  node-red-configurable-ping
RUN npm install --save npm install @node-red-contrib-themes/theme-collection@v2.2