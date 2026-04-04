<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { bars, yLabel, locale }: {
		bars: ReadonlyArray<{ label: string; from: Date; to: Date; value: number }>;
		yLabel: string;
		locale: Locale;
	} = $props();
</script>

<div>GanttTimeline — {bars.length} bars, y: {yLabel} ({locale})</div>
