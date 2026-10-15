import { getCustomers } from '#lib/features/customers/api/customers.api.ts';
import type {
	Customer,
	CustomerFilters,
	CustomerStatus
} from '#lib/features/customers/domain/customer.types.ts';

export async function loadCustomers(status: CustomerStatus | 'ALL' = 'ALL'): Promise<Customer[]> {
	return getCustomers({ status });
}

export function filterCustomers(customers: Customer[], filters: CustomerFilters): Customer[] {
	const search = filters.search.trim().toLowerCase();

	return customers.filter((customer) => {
		const matchesStatus = filters.status === 'ALL' || customer.status === filters.status;

		const matchesSearch =
			!search ||
			customer.name.toLowerCase().includes(search) ||
			customer.email.toLowerCase().includes(search);

		return matchesStatus && matchesSearch;
	});
}
