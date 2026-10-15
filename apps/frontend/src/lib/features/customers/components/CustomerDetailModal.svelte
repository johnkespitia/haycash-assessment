<script lang="ts">
	import type { Customer } from '#lib/features/customers/domain/customer.types.ts';
	import CustomerStatusBadge from '#lib/features/customers/components/CustomerStatusBadge.svelte';

	let {
		customer,
		loading = false,
		error = null,
		onClose
	}: {
		customer: Customer | null;
		loading?: boolean;
		error?: string | null;
		onClose: () => void;
	} = $props();

	const dateFormatter = new Intl.DateTimeFormat('es-MX', {
		dateStyle: 'medium',
		timeStyle: 'short'
	});

	function formatDate(value: string): string {
		const date = new Date(value);

		return Number.isNaN(date.getTime()) ? 'Fecha no disponible' : dateFormatter.format(date);
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			onClose();
		}
	}
</script>

<svelte:window onkeydown={handleKeydown} />

<div
	class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
	role="presentation"
	onclick={(event) => {
		if (event.target === event.currentTarget) onClose();
	}}
>
	<dialog
		open
		aria-labelledby="customer-detail-title"
		class="m-auto w-full max-w-lg rounded-xl bg-white p-6 shadow-xl"
	>
		<header class="flex items-start justify-between gap-4">
			<div>
				<h2 id="customer-detail-title" class="text-lg font-semibold text-gray-900">
					Detalle del cliente
				</h2>
				<p class="mt-1 text-sm text-gray-500">Información del cliente seleccionado</p>
			</div>

			<button
				type="button"
				onclick={onClose}
				aria-label="Cerrar detalle"
				class="rounded-md px-3 py-1 text-xl text-gray-500 hover:bg-gray-100"
			>
				&times;
			</button>
		</header>

		{#if loading}
			<div class="py-10 text-center text-sm text-gray-500" role="status">
				Cargando información del cliente...
			</div>
		{:else if error}
			<div class="mt-6 rounded-md bg-red-50 p-4 text-sm text-red-700" role="alert">
				{error}
			</div>
		{:else if customer}
			<dl class="mt-6 space-y-5">
				<div>
					<dt class="text-sm text-gray-500">Nombre</dt>
					<dd class="mt-1 font-medium text-gray-900">{customer.name}</dd>
				</div>

				<div>
					<dt class="text-sm text-gray-500">Correo electrónico</dt>
					<dd class="mt-1 break-all text-gray-900">{customer.email}</dd>
				</div>

				<div>
					<dt class="text-sm text-gray-500">Estado</dt>
					<dd class="mt-1">
						<CustomerStatusBadge status={customer.status} />
					</dd>
				</div>

				<div>
					<dt class="text-sm text-gray-500">Fecha de registro</dt>
					<dd class="mt-1 text-gray-900">
						{formatDate(customer.created_at)}
					</dd>
				</div>

				<div>
					<dt class="text-sm text-gray-500">ID</dt>
					<dd class="mt-1 font-mono text-xs break-all text-gray-600">
						{customer.id}
					</dd>
				</div>
			</dl>
		{/if}

		<footer class="mt-8 flex justify-end">
			<button
				type="button"
				onclick={onClose}
				class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
			>
				Cerrar
			</button>
		</footer>
	</dialog>
</div>
