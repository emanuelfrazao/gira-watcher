<script lang="ts">
	import '../app.css';
	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import type { Snippet } from 'svelte';

	let { data, children }: { data: { locale: 'pt'; lastScrapeAt: Date | null; lastRun: import('$lib/types/audit.js').ScrapeRun | null }; children: Snippet } = $props();
</script>

<Header locale={data.locale} lastScrapeAt={data.lastScrapeAt} />
<main>
	{@render children()}
</main>
<Footer locale={data.locale} lastRun={data.lastRun} />
