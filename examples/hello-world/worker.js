// Hello World Example
// The simplest possible Cloudflare Worker

export default {
  async fetch(request, env, ctx) {
    return new Response('Hello, World!');
  },
};
