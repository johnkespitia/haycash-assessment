const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function httpGet<T>(path: string): Promise<T> {
	const response = await fetch(`${API_BASE_URL}${path}`);

	if (!response.ok) {
		throw new Error(`HTTP ${response.status}: ${response.statusText}`);
	}

	return (await response.json()) as T;
}

export async function httpPost<T>(path: string, body: unknown): Promise<T> {
	const response = await fetch(`${API_BASE_URL}${path}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	if (!response.ok) {
		throw new Error(`HTTP ${response.status}: ${response.statusText}`);
	}

	return (await response.json()) as T;
}

export async function httpPatch<T>(path: string, body: unknown): Promise<T> {
	const response = await fetch(`${API_BASE_URL}${path}`, {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	if (!response.ok) {
		throw new Error(`HTTP ${response.status}: ${response.statusText}`);
	}

	return (await response.json()) as T;
}

export async function httpDelete<T>(path: string): Promise<T> {
	const response = await fetch(`${API_BASE_URL}${path}`, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	if (!response.ok) {
		throw new Error(`HTTP ${response.status}: ${response.statusText}`);
	}

	return (await response.json()) as T;
}

export async function httpPut<T>(path: string, body: unknown): Promise<T> {
	const response = await fetch(`${API_BASE_URL}${path}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	if (!response.ok) {
		throw new Error(`HTTP ${response.status}: ${response.statusText}`);
	}

	return (await response.json()) as T;
}
