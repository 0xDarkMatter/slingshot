// Static Site Worker Template
// This template serves static HTML content from the edge

const HTML = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Cloudflare Worker Site</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem;
      line-height: 1.6;
      color: #333;
    }
    h1 {
      color: #f38020;
      border-bottom: 2px solid #f38020;
      padding-bottom: 0.5rem;
    }
    .info {
      background: #f5f5f5;
      padding: 1rem;
      border-radius: 4px;
      margin: 1rem 0;
    }
    code {
      background: #e0e0e0;
      padding: 0.2rem 0.4rem;
      border-radius: 3px;
      font-family: 'Courier New', monospace;
    }
  </style>
</head>
<body>
  <h1>Hello from Cloudflare Workers!</h1>

  <div class="info">
    <p><strong>This is a static site served from the edge.</strong></p>
    <p>Your content is delivered from Cloudflare's global network, ensuring fast load times anywhere in the world.</p>
  </div>

  <h2>Features</h2>
  <ul>
    <li>Ultra-fast edge delivery</li>
    <li>Zero cold starts</li>
    <li>Global availability</li>
    <li>Built-in DDoS protection</li>
  </ul>

  <h2>Next Steps</h2>
  <ol>
    <li>Edit <code>worker.js</code> to customize your site</li>
    <li>Add more pages and routing logic</li>
    <li>Deploy with <code>cfworker deploy</code></li>
  </ol>

  <footer style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #ddd; color: #666;">
    <p>Powered by Cloudflare Workers</p>
  </footer>
</body>
</html>
`;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Simple routing - you can extend this
    if (path === '/' || path === '/index.html') {
      return new Response(HTML, {
        headers: {
          'Content-Type': 'text/html;charset=UTF-8',
          'Cache-Control': 'public, max-age=3600',
        },
      });
    }

    // Add more routes as needed
    // Example: serve different pages
    if (path === '/about') {
      return new Response('<h1>About Page</h1>', {
        headers: { 'Content-Type': 'text/html' },
      });
    }

    // 404 for unknown routes
    return new Response('404 Not Found', {
      status: 404,
      headers: { 'Content-Type': 'text/plain' },
    });
  },
};
