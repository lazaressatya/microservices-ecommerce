# =========================
# Stage 1: Dependencies
# =========================
FROM node:22-alpine AS dependencies

WORKDIR /app

COPY package*.json ./

RUN npm install


# =========================
# Stage 2: Production
# =========================
FROM node:22-alpine AS production

WORKDIR /app

ENV NODE_ENV=production

COPY --from=dependencies /app/node_modules ./node_modules

COPY package*.json ./
COPY server.js ./

EXPOSE 3001

CMD ["npm", "start"]    