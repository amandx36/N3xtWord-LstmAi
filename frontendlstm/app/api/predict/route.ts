export async function POST(request: Request) {
  try {
    const backendUrl = (process.env.N3xtharBackendUrl || 'http://127.0.0.1:8000').replace(/\/$/, '');
    const body = await request.json();

    const backendResponse = await fetch(`${backendUrl}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      cache: 'no-store',
    });

    const responseBody = await backendResponse.text();
    return new Response(responseBody, {
      status: backendResponse.status,
      headers: { 'Content-Type': backendResponse.headers.get('content-type') ?? 'application/json' },
    });
  } catch {
    return Response.json(
      { error: 'Could not reach the prediction API. Check that the backend is running.' },
      { status: 502 },
    );
  }
}
