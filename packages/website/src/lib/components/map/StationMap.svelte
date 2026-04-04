<script lang="ts">
	import type { StationGeoJSON } from '$lib/types/chart-data.js';

	let { stations, height = 500 }: {
		stations: StationGeoJSON;
		height?: number;
	} = $props();
</script>

<div style="height: {height}px">StationMap — {stations.features.length} stations</div>
