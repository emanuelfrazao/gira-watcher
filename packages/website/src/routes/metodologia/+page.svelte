<script lang="ts">
	let { data } = $props();
</script>

<svelte:head>
	<title>Metodologia — GIRA Watch</title>
</svelte:head>

<h1>Metodologia e Transparencia</h1>
<p>{data.auditTrail.length} audit trail entries, {data.completeness.length} completeness records</p>
