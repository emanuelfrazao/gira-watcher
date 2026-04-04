<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { selected, max = 4, locale }: {
		selected: ReadonlyArray<string>;
		max?: number;
		locale: Locale;
	} = $props();
</script>

<div>ComparisonSelector — {selected.length}/{max} stations ({locale})</div>
