import { httpGet } from '#lib/shared/api/http-client.ts';
import type { Customer } from '#lib/features/customers/domain/customer.types.ts';

export interface GetCustomersParams {
	search?: string;
	status?: Customer['status'] | 'ALL';
}

export function getCustomers(params: GetCustomersParams = {}): Promise<Customer[]> {
	const query = new URLSearchParams();

	if (params.search?.trim()) {
		query.set('search', params.search.trim());
	}

	if (params.status && params.status !== 'ALL') {
		query.set('status', params.status);
	}

	const queryString = query.toString();
	const path = queryString ? `/customers?${queryString}` : '/customers';

	return httpGet<Customer[]>(path);
}

export function getCustomerById(id: string): Promise<Customer> {
	return httpGet<Customer>(`/customers/${encodeURIComponent(id)}`);
}
