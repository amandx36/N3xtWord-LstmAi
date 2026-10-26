const backendUrl = () =>
  (process.env.N3xtharBackendUrl || 'http://127.0.0.1:8000').replace(/\/$/, '');

export async function GET() {
  try {
    const backendResponse = await fetch(`${backendUrl()}/health`, {
      method: 'GET',
      cache: 'no-store',
    });

    return new Response(backendResponse.body, {
      status: backendResponse.status,
      headers: {
        'Content-Type': backendResponse.headers.get('content-type') ?? 'application/json',
        'Cache-Control': 'no-store',
      },
    });
  } catch {
    return Response.json(
      { error: 'Could not reach the backend health check. Check that the backend is running.' },
      { status: 502, headers: { 'Cache-Control': 'no-store' } },
    );
  }
}
