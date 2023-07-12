# Daresbury Openday Heatmap Website

## Tech Stack

- pnpm
- Typescript
- AstroJS

## Running

For development, use the `pnpm dev` command to start up an instance of the website with hot-reloading enabled.

To test production locally, use `pnpm astro build && pnpm astro preview` which will build the website for production and then setup a preview server - **do not use this approach for deployment purposes**. Instead for deployment purposes, the preferred method is to build the container image using the Dockerfile located in this directory.
