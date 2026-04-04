<script lang="ts">
	import type { TimeSeriesPoint } from '$lib/types/metrics.js';

	let { data, width = 80, height = 24, color }: {
		data: ReadonlyArray<TimeSeriesPoint>;
		width?: number;
		height?: number;
		color?: string;
	} = $props();
</script>

<div>Sparkline — {data.length} points, {width}x{height}{color ? `, ${color}` : ''}</div>
