<script lang="ts">
	import type { GlobalFilterState } from '$lib/types/filters.js';

	let { filters }: { filters: GlobalFilterState } = $props();
</script>

<div>FilterChips — {filters.zones.length} zones active</div>
