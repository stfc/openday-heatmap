import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import tailwind from "@astrojs/tailwind";
import image from "@astrojs/image";
import markdoc from "@astrojs/markdoc";
import react from "@astrojs/react";

import node from "@astrojs/node";

// https://astro.build/config
export default defineConfig({
  output: "hybrid",
  site: "https://example.com",
  integrations: [mdx(), sitemap(), tailwind(), image(), markdoc(), react()],
  adapter: node({
    mode: "standalone"
  })
});
