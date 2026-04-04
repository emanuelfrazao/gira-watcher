<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';
	import type { StationMapPoint } from '$lib/types/metrics.js';

	let { station, locale }: { station: StationMapPoint; locale: Locale } = $props();
</script>

<div>StationCard — {station.name}, {station.bikes} bikes ({locale})</div>
