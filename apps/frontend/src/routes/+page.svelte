<script lang="ts">
	import { onMount } from 'svelte';

	import { createCustomersController } from '#lib/features/customers/controllers/customers.controller.svelte.ts';

	import CustomerFilters from '#lib/features/customers/components/CustomerFilters.svelte';
	import CustomerTable from '#lib/features/customers/components/CustomerTable.svelte';
	import CustomerDetailModal from '#lib/features/customers/components/CustomerDetailModal.svelte';

	const controller = createCustomersController();

	onMount(() => {
		void controller.initialize();
	});
</script>

<svelte:head>
	<title>Clientes | Dashboard</title>
	<meta name="description" content="Consulta y filtra los clientes registrados." />
</svelte:head>

<main class="min-h-screen bg-gray-50 px-4 py-8 sm:px-6 lg:px-8">
	<div class="mx-auto max-w-6xl space-y-6">
		<header>
			<h1 class="text-2xl font-bold tracking-tight text-gray-900">Clientes</h1>
			<p class="mt-1 text-sm text-gray-600">Consulta la información de los clientes.</p>
		</header>

		<CustomerFilters filters={controller.filters} onFiltersChange={controller.updateFilters} />

		{#if controller.loading}
			<div
				class="rounded-lg border border-gray-200 bg-white px-6 py-12 text-center text-sm text-gray-500"
				role="status"
			>
				Cargando clientes...
			</div>
		{:else if controller.error}
			<div class="rounded-lg border border-red-200 bg-white p-6" role="alert">
				<p class="text-sm text-red-700">{controller.error}</p>
				<button
					type="button"
					onclick={controller.retryCustomers}
					class="mt-3 rounded-md bg-red-50 px-3 py-2 text-sm font-medium text-red-700 hover:bg-red-100"
				>
					Reintentar
				</button>
			</div>
		{:else if controller.filteredCustomers.length === 0}
			<div class="rounded-lg border border-gray-200 bg-white px-6 py-12 text-center" role="status">
				<h2 class="text-base font-semibold text-gray-900">
					{controller.customers.length === 0
						? 'No hay clientes registrados'
						: 'No se encontraron clientes'}
				</h2>
				<p class="mt-1 text-sm text-gray-500">
					{controller.customers.length === 0
						? 'Los clientes aparecerán aquí cuando estén disponibles.'
						: 'Prueba con otro nombre, correo o estado.'}
				</p>
			</div>
		{:else}
			<p class="text-sm text-gray-600">
				{controller.filteredCustomers.length}
				{controller.filteredCustomers.length === 1 ? 'cliente' : 'clientes'}
			</p>

			<CustomerTable
				customers={controller.filteredCustomers}
				onViewDetails={controller.openCustomerDetails}
			/>
		{/if}
	</div>
</main>

{#if controller.isDetailOpen}
	<CustomerDetailModal
		customer={controller.selectedCustomer}
		loading={controller.detailLoading}
		error={controller.detailError}
		onClose={controller.closeCustomerDetails}
	/>
{/if}
