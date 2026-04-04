<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { groups, yLabel, locale }: {
		groups: ReadonlyArray<{ label: string; values: ReadonlyArray<number> }>;
		yLabel: string;
		locale: Locale;
	} = $props();
</script>

<div>BoxPlot — {groups.length} groups, y: {yLabel} ({locale})</div>
