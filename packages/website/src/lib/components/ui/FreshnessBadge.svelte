<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { lastScrapeAt, locale }: { lastScrapeAt: Date; locale: Locale } = $props();
</script>

<div>FreshnessBadge — {lastScrapeAt.toISOString()} ({locale})</div>
