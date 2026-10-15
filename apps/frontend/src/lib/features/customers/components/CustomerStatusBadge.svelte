<script lang="ts">
	import type { CustomerStatus } from '#lib/features/customers/domain/customer.types.ts';

	let { status }: { status: CustomerStatus } = $props();

	const statusLabels: Record<CustomerStatus, string> = {
		ACTIVE: 'Activo',
		PENDING: 'Pendiente',
		BLOCKED: 'Bloqueado'
	};

	const statusStyles: Record<CustomerStatus, string> = {
		ACTIVE: 'bg-green-100 text-green-800',
		PENDING: 'bg-amber-100 text-amber-800',
		BLOCKED: 'bg-red-100 text-red-800'
	};
</script>

<span
	class={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${statusStyles[status]}`}
>
	{statusLabels[status]}
</span>
