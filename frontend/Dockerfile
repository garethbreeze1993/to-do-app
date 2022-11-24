FROM node:16.18-alpine
WORKDIR /usr/src/todo-app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
