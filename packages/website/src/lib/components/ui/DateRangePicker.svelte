<script lang="ts">
	import type { Locale, TimeRangePreset } from '$lib/types/enums.js';
	import type { TimeRange } from '$lib/types/filters.js';

	let { value, locale }: {
		value: TimeRangePreset | TimeRange;
		locale: Locale;
	} = $props();
</script>

<div>DateRangePicker — {typeof value === 'string' ? value : 'custom'} ({locale})</div>
