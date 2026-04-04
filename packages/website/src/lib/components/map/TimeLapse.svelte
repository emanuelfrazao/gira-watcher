<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';
	import type { StationGeoJSON } from '$lib/types/chart-data.js';

	let { frames, locale }: {
		frames: ReadonlyArray<{ timestamp: Date; stations: StationGeoJSON }>;
		locale: Locale;
	} = $props();
</script>

<div>TimeLapse — {frames.length} frames ({locale})</div>
