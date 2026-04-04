<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';
	import type { StationRankingRow } from '$lib/types/metrics.js';

	let { rows, locale }: {
		rows: ReadonlyArray<StationRankingRow>;
		locale: Locale;
	} = $props();
</script>

<div>RankedTable — {rows.length} rows ({locale})</div>
