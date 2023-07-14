# Docker best practices wasn't working :'(
FROM node:18.12.1-slim
WORKDIR /app

# Enable PNPM
RUN corepack enable pnpm

COPY . .

RUN pnpm install
RUN pnpm build

ENV HOST=0.0.0.0
ENV PORT=3000
EXPOSE 3000
CMD node ./dist/server/entry.mjs
