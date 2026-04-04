<script lang="ts">
	let { data } = $props();
</script>

<svelte:head>
	<title>{data.title} — GIRA Watch</title>
</svelte:head>

<article>
	<h1>{data.title}</h1>
	<time datetime={data.publishedAt.toISOString()}>{data.publishedAt.toLocaleDateString('pt-PT')}</time>
	<p>{data.content}</p>
</article>
