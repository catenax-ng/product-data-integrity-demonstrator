FROM node:lts

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .
RUN npm run build

# TODO: separate build container and cleanup before copy to run container

# ENV HOST 0.0.0.0
ENV PORT 80

EXPOSE 80

CMD ["npm", "run", "start"]