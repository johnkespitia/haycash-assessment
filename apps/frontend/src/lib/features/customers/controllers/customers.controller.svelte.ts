import { onDestroy } from 'svelte';

import type {
	Customer,
	CustomerFilters,
	CustomerStatus
} from '#lib/features/customers/domain/customer.types.ts';

import { getCustomerById } from '#lib/features/customers/api/customers.api.ts';
import {
	filterCustomers,
	loadCustomers
} from '#lib/features/customers/services/customers.service.ts';

export function createCustomersController() {
	let customers = $state<Customer[]>([]);
	let filters = $state<CustomerFilters>({
		search: '',
		status: 'ALL'
	});

	let loading = $state(false);
	let error = $state<string | null>(null);

	let selectedCustomer = $state<Customer | null>(null);
	let isDetailOpen = $state(false);
	let detailLoading = $state(false);
	let detailError = $state<string | null>(null);

	let requestId = 0;
	let detailRequestId = 0;

	const filteredCustomers = $derived(filterCustomers(customers, filters));

	async function refreshCustomers(status: CustomerStatus | 'ALL' = filters.status) {
		const currentRequest = ++requestId;

		loading = true;
		error = null;

		try {
			const result = await loadCustomers(status);

			if (currentRequest === requestId) {
				customers = result;
			}
		} catch {
			if (currentRequest === requestId) {
				error = 'No fue posible cargar los clientes. Intenta nuevamente.';
			}
		} finally {
			if (currentRequest === requestId) {
				loading = false;
			}
		}
	}

	function updateFilters(nextFilters: CustomerFilters) {
		const statusChanged = filters.status !== nextFilters.status;

		filters = nextFilters;

		if (statusChanged) {
			void refreshCustomers(nextFilters.status);
		}
	}

	async function openCustomerDetails(customerId: string) {
		const currentRequest = ++detailRequestId;

		isDetailOpen = true;
		detailLoading = true;
		detailError = null;
		selectedCustomer = null;

		try {
			const customer = await getCustomerById(customerId);

			if (currentRequest === detailRequestId) {
				selectedCustomer = customer;
			}
		} catch {
			if (currentRequest === detailRequestId) {
				detailError = 'No fue posible cargar el detalle del cliente.';
			}
		} finally {
			if (currentRequest === detailRequestId) {
				detailLoading = false;
			}
		}
	}

	function closeCustomerDetails() {
		detailRequestId++;

		isDetailOpen = false;
		selectedCustomer = null;
		detailLoading = false;
		detailError = null;
	}

	function retryCustomers() {
		return refreshCustomers();
	}

	function initialize() {
		return refreshCustomers();
	}

	onDestroy(() => {
		requestId++;
		detailRequestId++;
	});

	return {
		get customers() {
			return customers;
		},
		get filters() {
			return filters;
		},
		get loading() {
			return loading;
		},
		get error() {
			return error;
		},
		get filteredCustomers() {
			return filteredCustomers;
		},
		get selectedCustomer() {
			return selectedCustomer;
		},
		get isDetailOpen() {
			return isDetailOpen;
		},
		get detailLoading() {
			return detailLoading;
		},
		get detailError() {
			return detailError;
		},
		updateFilters,
		openCustomerDetails,
		closeCustomerDetails,
		retryCustomers,
		initialize
	};
}
