<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';
	import type { KpiValue } from '$lib/types/metrics.js';

	let { kpis, locale }: {
		kpis: ReadonlyArray<KpiValue>;
		locale: Locale;
	} = $props();
</script>

<div>KpiStrip — {kpis.length} metrics ({locale})</div>
