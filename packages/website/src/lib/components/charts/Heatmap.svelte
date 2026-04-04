<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { cells, xLabel, yLabel, colorScale, locale }: {
		cells: ReadonlyArray<{ x: string | number | Date; y: string | number; value: number }>;
		xLabel: string;
		yLabel: string;
		colorScale: 'YlGn' | 'RdYlGn' | 'RdGy';
		locale: Locale;
	} = $props();
</script>

<div>Heatmap — {cells.length} cells, {colorScale} scale ({locale}), {xLabel} x {yLabel}</div>
