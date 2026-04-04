<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { data, categoryField, valueFields, direction, locale }: {
		data: ReadonlyArray<Record<string, unknown>>;
		categoryField: string;
		valueFields: ReadonlyArray<{ field: string; label: string; color: string }>;
		direction: 'horizontal' | 'vertical';
		locale: Locale;
	} = $props();
</script>

<div>StackedBar — {data.length} rows, {valueFields.length} fields, {direction} ({locale}), cat: {categoryField}</div>
