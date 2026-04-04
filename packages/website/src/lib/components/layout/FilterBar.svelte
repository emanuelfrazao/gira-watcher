<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';
	import type { GlobalFilterState } from '$lib/types/filters.js';

	let { filters, locale }: { filters: GlobalFilterState; locale: Locale } = $props();
</script>

<div>FilterBar — {filters.stationCodes.length} stations selected ({locale})</div>
