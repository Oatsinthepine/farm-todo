# syntax=docker/dockerfile:1


################################################################################
ARG NODE_VERSION=24.1.0

# Use node image for building
FROM node:${NODE_VERSION}-alpine as build

# Set working directory for all build stages.
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json from the local directory into the conatiner set working directory.
COPY package*.json ./
# Run the clean build using the copied package.json and package-lock.json.
RUN npm ci

# Then copy the rest of the files into the container. e.g: src/, public/, vite.config.js etc.
COPY . .
# Build the application.
RUN npm run build

################################################################################
# final stage with ngix to serve the app
FROM nginx:alpine

COPY --from=build /usr/src/app/dist /usr/share/nginx/html

# Expose the port that the application listens on.
EXPOSE 80

# Run the application.
CMD ["nginx", "-g", "daemon off;"]
