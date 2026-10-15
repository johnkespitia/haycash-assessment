import { describe, expect, it } from 'vitest';

import { filterCustomers } from './customers.service';
import type { Customer, CustomerFilters } from '#lib/features/customers/domain/customer.types.ts';

const customers: Customer[] = [
	{
		id: 'customer-1',
		name: 'John Espitia',
		email: 'john@example.com',
		status: 'ACTIVE',
		created_at: '2026-10-15T04:03:14.223711Z'
	},
	{
		id: 'customer-2',
		name: 'Ana García',
		email: 'ana@example.com',
		status: 'PENDING',
		created_at: '2026-10-14T10:00:00Z'
	},
	{
		id: 'customer-3',
		name: 'Carlos López',
		email: 'carlos@example.com',
		status: 'BLOCKED',
		created_at: '2026-10-13T10:00:00Z'
	}
];

const defaultFilters: CustomerFilters = {
	search: '',
	status: 'ALL'
};

describe('filterCustomers', () => {
	it('returns all customers when no filters are applied', () => {
		expect(filterCustomers(customers, defaultFilters)).toEqual(customers);
	});

	it('filters by name without case sensitivity', () => {
		const result = filterCustomers(customers, {
			...defaultFilters,
			search: 'JOHN'
		});

		expect(result).toHaveLength(1);
		expect(result[0].id).toBe('customer-1');
	});

	it('filters by email', () => {
		const result = filterCustomers(customers, {
			...defaultFilters,
			search: 'ANA@EXAMPLE.COM'
		});

		expect(result).toHaveLength(1);
		expect(result[0].id).toBe('customer-2');
	});

	it('filters by status', () => {
		const result = filterCustomers(customers, {
			...defaultFilters,
			status: 'PENDING'
		});

		expect(result).toHaveLength(1);
		expect(result[0].status).toBe('PENDING');
	});

	it('combines search and status filters', () => {
		const result = filterCustomers(customers, {
			search: 'example.com',
			status: 'ACTIVE'
		});

		expect(result).toHaveLength(1);
		expect(result[0].id).toBe('customer-1');
	});

	it('returns an empty array when there are no matches', () => {
		const result = filterCustomers(customers, {
			...defaultFilters,
			search: 'nonexistent'
		});

		expect(result).toEqual([]);
	});

	it('trims whitespace from the search term', () => {
		const result = filterCustomers(customers, {
			...defaultFilters,
			search: '  John  '
		});

		expect(result).toHaveLength(1);
		expect(result[0].id).toBe('customer-1');
	});

	it('does not mutate the original customer array', () => {
		const original = [...customers];

		filterCustomers(customers, {
			search: 'John',
			status: 'ALL'
		});

		expect(customers).toEqual(original);
	});
});
