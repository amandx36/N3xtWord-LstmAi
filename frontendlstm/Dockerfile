from node:22-alpine

WORKDIR /app

copy package*.json  ./

run npm install 

copy . . 

expose 3000 

cmd ["npm","run","dev"]