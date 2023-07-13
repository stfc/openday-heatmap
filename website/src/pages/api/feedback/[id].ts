import type { APIRoute } from "astro";
import { z } from "astro:content";

const schema = z.object({
  QRID: z.number(),
  EmojiRating: z.string(),
  Thoughts: z.string(),
  Improvements: z.string(),
});

export const post: APIRoute = async ({ params, request }) => {
  const { id } = params;
  if (!id) {
    return new Response("Missing User ID", { status: 404 });
  }

  const requestBody = await request.json();
  const result = schema.safeParse(requestBody);

  if (!result.success) {
    return new Response(JSON.stringify(result.error.issues), { status: 422 });
  }

  // TODO: Handle errors
  await fetch(
    `${import.meta.env.HEATMAP_API_URL}/users/${id}/feedback`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(result.data),
    }
  );

  return new Response(null, { status: 200 });
};
