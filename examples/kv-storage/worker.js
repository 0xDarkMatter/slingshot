// KV Storage Example
// Demonstrates using Cloudflare KV for data persistence

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // GET /get?key=mykey - Retrieve value from KV
    if (path === '/get' && request.method === 'GET') {
      const key = url.searchParams.get('key');
      if (!key) {
        return Response.json({ error: 'Missing key parameter' }, { status: 400 });
      }

      const value = await env.MY_KV.get(key);
      if (value === null) {
        return Response.json({ error: 'Key not found' }, { status: 404 });
      }

      return Response.json({ key, value });
    }

    // POST /set - Store value in KV
    // Body: { "key": "mykey", "value": "myvalue", "ttl": 3600 }
    if (path === '/set' && request.method === 'POST') {
      const body = await request.json();
      const { key, value, ttl } = body;

      if (!key || !value) {
        return Response.json({ error: 'Missing key or value' }, { status: 400 });
      }

      const options = ttl ? { expirationTtl: ttl } : {};
      await env.MY_KV.put(key, value, options);

      return Response.json({ success: true, key });
    }

    // DELETE /delete?key=mykey - Delete value from KV
    if (path === '/delete' && request.method === 'DELETE') {
      const key = url.searchParams.get('key');
      if (!key) {
        return Response.json({ error: 'Missing key parameter' }, { status: 400 });
      }

      await env.MY_KV.delete(key);
      return Response.json({ success: true, key });
    }

    return Response.json({ error: 'Not found' }, { status: 404 });
  },
};
