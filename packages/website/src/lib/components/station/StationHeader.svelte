<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';
	import type { Station } from '$lib/types/dimensions.js';

	let { station, locale }: { station: Station; locale: Locale } = $props();
</script>

<div>StationHeader — {station.name} ({station.stationCode}) [{locale}]</div>
