<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { title, items, locale }: {
		title: string;
		items: ReadonlyArray<{ color: string; label: string }>;
		locale: Locale;
	} = $props();
</script>

<div>MapLegend — {title}, {items.length} items ({locale})</div>
