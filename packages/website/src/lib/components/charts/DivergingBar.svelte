<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { data, categoryField, positiveField, negativeField, locale }: {
		data: ReadonlyArray<Record<string, unknown>>;
		categoryField: string;
		positiveField: string;
		negativeField: string;
		locale: Locale;
	} = $props();
</script>

<div>DivergingBar — {data.length} rows, {categoryField}, +{positiveField}/-{negativeField} ({locale})</div>
