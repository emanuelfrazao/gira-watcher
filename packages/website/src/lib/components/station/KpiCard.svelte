<script lang="ts">
	import type { Locale, HealthLevel } from '$lib/types/enums.js';
	import type { MetricId, TimeSeriesPoint } from '$lib/types/metrics.js';

	let { metricId, label, value, delta, deltaPercent, healthLevel, sparklineData, locale }: {
		metricId: MetricId;
		label: string;
		value: number;
		delta: number;
		deltaPercent: number;
		healthLevel: HealthLevel;
		sparklineData: ReadonlyArray<TimeSeriesPoint>;
		locale: Locale;
	} = $props();
</script>

<div data-metric={metricId} data-health={healthLevel}>
	KpiCard — {label}: {value} ({delta >= 0 ? '+' : ''}{deltaPercent}%) [{sparklineData.length} pts] ({locale})
</div>
