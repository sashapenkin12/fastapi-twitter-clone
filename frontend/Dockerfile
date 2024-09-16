FROM node:15.8-alpine3.11 AS build
WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm build

FROM nginx:stable-alpine

COPY --from=build /app/frontend/dist /app/frontend/static
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
