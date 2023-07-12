FROM node:18.12.1-slim AS builder

WORKDIR /app

# Enable PNPM
RUN corepack enable pnpm

# By using pnpm fetch, we only need the lock file. Thus avoiding any 
#   unnecessary cache invalidations when updating the package.json file
COPY pnpm-lock.yaml ./
RUN pnpm fetch --prod

ADD . ./
RUN pnpm install --offline --prod

RUN pnpm build

FROM node:18.12.1-slim as runner
WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

CMD node ./dist/server/entry.mjs
