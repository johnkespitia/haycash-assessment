<script lang="ts">
	import type { Customer } from '#lib/features/customers/domain/customer.types.ts';
	import CustomerStatusBadge from '#lib/features/customers/components/CustomerStatusBadge.svelte';

	let {
		customers,
		onViewDetails
	}: {
		customers: Customer[];
		onViewDetails: (customerId: string) => void;
	} = $props();
</script>

{#if customers.length === 0}
	<div class="rounded-lg border border-dashed border-gray-300 px-6 py-12 text-center">
		<h2 class="text-base font-semibold text-gray-900">No se encontraron clientes</h2>
		<p class="mt-1 text-sm text-gray-500">Prueba cambiando los filtros de búsqueda.</p>
	</div>
{:else}
	<div class="overflow-hidden rounded-lg border border-gray-200 bg-white">
		<div class="overflow-x-auto">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th
							scope="col"
							class="px-4 py-3 text-left text-xs font-semibold tracking-wide text-gray-500 uppercase"
						>
							Cliente
						</th>
						<th
							scope="col"
							class="px-4 py-3 text-left text-xs font-semibold tracking-wide text-gray-500 uppercase"
						>
							Estado
						</th>
						<th
							scope="col"
							class="px-4 py-3 text-right text-xs font-semibold tracking-wide text-gray-500 uppercase"
						>
							Acciones
						</th>
					</tr>
				</thead>

				<tbody class="divide-y divide-gray-200 bg-white">
					{#each customers as customer (customer.id)}
						<tr class="hover:bg-gray-50">
							<td class="px-4 py-4 font-medium text-gray-900">
								{customer.name}
							</td>

							<td class="px-4 py-4">
								<CustomerStatusBadge status={customer.status} />
							</td>

							<td class="px-4 py-4 text-right">
								<button
									type="button"
									onclick={() => onViewDetails(customer.id)}
									class="rounded-md px-3 py-2 text-sm font-medium text-indigo-600 hover:bg-indigo-50 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-none"
									aria-label={`Ver detalle de ${customer.name}`}
								>
									Ver detalle
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
{/if}
