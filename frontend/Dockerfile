# Сборка фронтенда
FROM node:20 as build
WORKDIR /app
COPY frontend/ /app/
RUN npm install && npm run build

# Сервер для статики
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"] 