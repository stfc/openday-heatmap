import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import tailwind from "@astrojs/tailwind";
import markdoc from "@astrojs/markdoc";
import react from "@astrojs/react";

import node from "@astrojs/node";

// Seems better to use the experimental image feature - https://github.com/withastro/astro/issues/5008
//
// https://astro.build/config
export default defineConfig({
  experimental: {
    assets: true,
  },
  output: "server",
  site: "https://example.com",
  integrations: [mdx(), sitemap(), tailwind(), markdoc(), react()],
  adapter: node({
    mode: "standalone",
  }),
});
