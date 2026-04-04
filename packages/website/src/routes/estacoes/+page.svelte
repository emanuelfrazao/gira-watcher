<script lang="ts">
	let { data } = $props();
</script>

<svelte:head>
	<title>Estacoes — GIRA Watch</title>
</svelte:head>

<h1>Explorador de Estacoes</h1>
<p>{data.mapData.length} stations on map, {data.ranking.length} in ranking</p>
