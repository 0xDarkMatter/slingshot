// REST API Worker Template
// This template provides a basic REST API with routing

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // CORS headers for browser requests
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle CORS preflight
    if (method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // API Routes
    try {
      // GET /api/hello
      if (path === '/api/hello' && method === 'GET') {
        return Response.json(
          { message: 'Hello, World!', timestamp: Date.now() },
          { headers: corsHeaders }
        );
      }

      // GET /api/status
      if (path === '/api/status' && method === 'GET') {
        return Response.json(
          { status: 'ok', version: '1.0.0' },
          { headers: corsHeaders }
        );
      }

      // POST /api/echo - Echo back the request body
      if (path === '/api/echo' && method === 'POST') {
        const body = await request.json();
        return Response.json(
          { received: body, timestamp: Date.now() },
          { headers: corsHeaders }
        );
      }

      // 404 for unknown routes
      return Response.json(
        { error: 'Not found', path },
        { status: 404, headers: corsHeaders }
      );
    } catch (error) {
      // Error handling
      return Response.json(
        { error: 'Internal server error', message: error.message },
        { status: 500, headers: corsHeaders }
      );
    }
  },
};
