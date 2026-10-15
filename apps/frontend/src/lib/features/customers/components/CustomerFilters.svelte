<script lang="ts">
	import type {
		CustomerFilters as CustomerFiltersType,
		CustomerStatus
	} from '#lib/features/customers/domain/customer.types.ts';

	let {
		filters,
		onFiltersChange
	}: {
		filters: CustomerFiltersType;
		onFiltersChange: (filters: CustomerFiltersType) => void;
	} = $props();

	let debounceTimer: ReturnType<typeof setTimeout> | undefined;

	const MIN_SEARCH_LENGTH = 3;
	const DEBOUNCE_DELAY = 300;

	const statusOptions: {
		value: CustomerStatus | 'ALL';
		label: string;
	}[] = [
		{ value: 'ALL', label: 'Todos los estados' },
		{ value: 'ACTIVE', label: 'Activo' },
		{ value: 'PENDING', label: 'Pendiente' },
		{ value: 'BLOCKED', label: 'Bloqueado' }
	];

	function clearDebounce() {
		if (debounceTimer !== undefined) {
			clearTimeout(debounceTimer);
			debounceTimer = undefined;
		}
	}

	function updateSearch(value: string) {
		clearDebounce();

		const search = value.trim();

		if (search.length < MIN_SEARCH_LENGTH) {
			if (filters.search !== '') {
				onFiltersChange({ ...filters, search: '' });
			}
			return;
		}

		debounceTimer = setTimeout(() => {
			onFiltersChange({ ...filters, search });
			debounceTimer = undefined;
		}, DEBOUNCE_DELAY);
	}

	function updateStatus(status: CustomerStatus | 'ALL') {
		onFiltersChange({ ...filters, status });
	}
</script>

<section aria-label="Filtros de clientes" class="flex flex-col gap-3 sm:flex-row sm:items-center">
	<div class="flex-1">
		<label for="customer-search" class="mb-1 block text-sm font-medium text-gray-700">
			Buscar clientes
		</label>

		<input
			id="customer-search"
			type="search"
			value={filters.search}
			oninput={(event) => updateSearch((event.currentTarget as HTMLInputElement).value)}
			placeholder="Nombre o correo electrónico"
			class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
		/>
	</div>

	<div class="sm:w-56">
		<label for="customer-status" class="mb-1 block text-sm font-medium text-gray-700">
			Estado
		</label>

		<select
			id="customer-status"
			value={filters.status}
			onchange={(event) =>
				updateStatus((event.currentTarget as HTMLSelectElement).value as CustomerStatus | 'ALL')}
			class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
		>
			{#each statusOptions as option (option.value)}
				<option value={option.value}>{option.label}</option>
			{/each}
		</select>
	</div>
</section>
