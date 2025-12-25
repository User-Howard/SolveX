FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

ARG API_URL=http://backend:8000
ENV API_URL=$API_URL

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
