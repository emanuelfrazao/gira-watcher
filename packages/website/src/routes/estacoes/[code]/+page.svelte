<script lang="ts">
	import StationHeader from '$lib/components/station/StationHeader.svelte';

	let { data } = $props();
</script>

<svelte:head>
	<title>{data.detail.station.name} — GIRA Watch</title>
</svelte:head>

<StationHeader station={data.detail.station} locale="pt" />
<p>Data quality: {(data.detail.dataQuality.observationCompleteness * 100).toFixed(1)}% complete</p>
