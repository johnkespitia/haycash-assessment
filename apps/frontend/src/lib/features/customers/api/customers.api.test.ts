import { afterEach, describe, expect, it, vi } from 'vitest';

import { getCustomerById, getCustomers } from './customers.api';

afterEach(() => {
	vi.restoreAllMocks();
});

describe('getCustomers', () => {
	it('requests all customers without query parameters', async () => {
		const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
			new Response(JSON.stringify([]), {
				status: 200,
				headers: { 'Content-Type': 'application/json' }
			})
		);

		await getCustomers();

		expect(fetchMock).toHaveBeenCalledOnce();
		expect(String(fetchMock.mock.calls[0][0])).toContain('/customers');
		expect(String(fetchMock.mock.calls[0][0])).not.toContain('?');
	});

	it('sends the selected status as a query parameter', async () => {
		const fetchMock = vi
			.spyOn(globalThis, 'fetch')
			.mockResolvedValue(new Response(JSON.stringify([]), { status: 200 }));

		await getCustomers({ status: 'ACTIVE' });

		expect(String(fetchMock.mock.calls[0][0])).toContain('status=ACTIVE');
	});

	it('does not send ALL as a status parameter', async () => {
		const fetchMock = vi
			.spyOn(globalThis, 'fetch')
			.mockResolvedValue(new Response(JSON.stringify([]), { status: 200 }));

		await getCustomers({ status: 'ALL' });

		expect(String(fetchMock.mock.calls[0][0])).not.toContain('status=');
	});

	it('trims and encodes the search parameter', async () => {
		const fetchMock = vi
			.spyOn(globalThis, 'fetch')
			.mockResolvedValue(new Response(JSON.stringify([]), { status: 200 }));

		await getCustomers({ search: '  John Espitia  ' });

		const url = String(fetchMock.mock.calls[0][0]);
		expect(url).toContain('search=John+Espitia');
	});

	it('propagates HTTP errors', async () => {
		vi.spyOn(globalThis, 'fetch').mockResolvedValue(
			new Response('Internal Server Error', {
				status: 500,
				statusText: 'Internal Server Error'
			})
		);

		await expect(getCustomers()).rejects.toThrow();
	});
});

describe('getCustomerById', () => {
	it('requests the customer by ID', async () => {
		const customer = {
			id: 'customer-1',
			name: 'John Espitia',
			email: 'john@example.com',
			status: 'ACTIVE',
			created_at: '2026-10-15T04:03:14.223711Z'
		};

		const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
			new Response(JSON.stringify(customer), {
				status: 200,
				headers: { 'Content-Type': 'application/json' }
			})
		);

		const result = await getCustomerById('customer-1');

		expect(String(fetchMock.mock.calls[0][0])).toContain('/customers/customer-1');
		expect(result).toEqual(customer);
	});

	it('encodes special characters in the customer ID', async () => {
		const fetchMock = vi
			.spyOn(globalThis, 'fetch')
			.mockResolvedValue(new Response(JSON.stringify({}), { status: 200 }));

		await getCustomerById('customer/123');

		expect(String(fetchMock.mock.calls[0][0])).toContain('customer%2F123');
	});
});
