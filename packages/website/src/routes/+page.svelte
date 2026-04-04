<script lang="ts">
	import KpiStrip from '$lib/components/station/KpiStrip.svelte';

	let { data } = $props();
</script>

<svelte:head>
	<title>GIRA Watch</title>
</svelte:head>

<h1>GIRA Watch</h1>
<KpiStrip kpis={data.kpis} locale="pt" />
<p>System availability: {data.availability.length} data points</p>
