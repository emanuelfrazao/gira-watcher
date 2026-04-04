<script lang="ts">
	let { data } = $props();
</script>

<svelte:head>
	<title>Analise — GIRA Watch</title>
</svelte:head>

<h1>Analise de Padroes</h1>
<p>{data.rateCurves.length} rate curve points, {data.heatmap.length} heatmap cells</p>
