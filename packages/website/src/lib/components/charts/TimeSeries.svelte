<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';
	import type { TimeSeriesPoint } from '$lib/types/metrics.js';

	let { series, yLabel, locale }: {
		series: ReadonlyArray<{ label: string; data: ReadonlyArray<TimeSeriesPoint>; color?: string }>;
		yLabel: string;
		locale: Locale;
	} = $props();
</script>

<div>TimeSeries — {series.length} series, y: {yLabel} ({locale})</div>
