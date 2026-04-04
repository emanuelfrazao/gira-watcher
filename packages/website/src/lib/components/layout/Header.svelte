<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { locale, lastScrapeAt }: { locale: Locale; lastScrapeAt: Date | null } = $props();
</script>

<header>
	<div>GIRA Watch — Header ({locale}, last scrape: {lastScrapeAt?.toISOString() ?? 'unknown'})</div>
</header>
