/// <reference path="../.astro/types.d.ts" />
/// <reference types="@astrojs/client-image" />

interface ImportMetaEnv {
  // Base URL for the heatmap API
  readonly HEATMAP_API_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
