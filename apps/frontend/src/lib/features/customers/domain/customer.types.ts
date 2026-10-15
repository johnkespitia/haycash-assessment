export const CUSTOMER_STATUSES = ['ACTIVE', 'PENDING', 'BLOCKED'] as const;

export type CustomerStatus = (typeof CUSTOMER_STATUSES)[number];

export interface Customer {
	id: string;
	name: string;
	email: string;
	status: CustomerStatus;
	created_at: string;
}

export interface CustomerFilters {
	search: string;
	status: CustomerStatus | 'ALL';
}
