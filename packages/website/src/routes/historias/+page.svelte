<script lang="ts">
	let { data } = $props();
</script>

<svelte:head>
	<title>Historias — GIRA Watch</title>
</svelte:head>

<h1>Historias com Dados</h1>
<p>{data.stories.length} stories published</p>
