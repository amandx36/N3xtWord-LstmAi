export async function GET() {
  try {
    const apiUrl = process.env.N3xtharBackendUrl;

    if (!apiUrl) {
      return Response.json(
        { error: 'Backend URL is not configured.' },
        { status: 500 }
      );
    }

    const response = await fetch(`${apiUrl}/health`, {
      method: 'GET',
      cache: 'no-store',
    });

    return new Response(response.body, {
      status: response.status,
      headers: {
        'Content-Type':
          response.headers.get('content-type') ?? 'application/json',
        'Cache-Control': 'no-store',
      },
    });
  } catch {
    return Response.json(
      { error: 'Unable to connect to the prediction api   backend.' },
      { status: 502 }
    );
  }
}