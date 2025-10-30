// Edge Function Worker Template
// This template provides a simple serverless function

export default {
  async fetch(request, env, ctx) {
    // Get request information
    const url = new URL(request.url);
    const userAgent = request.headers.get('User-Agent') || 'Unknown';
    const cfProperties = request.cf || {};

    // Build response data
    const responseData = {
      message: 'Hello from the edge!',
      timestamp: new Date().toISOString(),
      request: {
        method: request.method,
        url: url.href,
        path: url.pathname,
        query: Object.fromEntries(url.searchParams),
      },
      edge: {
        colo: cfProperties.colo || 'Unknown',
        country: cfProperties.country || 'Unknown',
        city: cfProperties.city || 'Unknown',
      },
      userAgent,
    };

    // Return JSON response
    return Response.json(responseData, {
      headers: {
        'Cache-Control': 'no-cache',
      },
    });
  },
};
