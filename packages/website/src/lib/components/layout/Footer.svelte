<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';
	import type { ScrapeRun } from '$lib/types/audit.js';

	let { locale, lastRun }: { locale: Locale; lastRun: ScrapeRun | null } = $props();
</script>

<footer>
	<div>GIRA Watch — Footer ({locale}, run: {lastRun?.runId ?? 'none'})</div>
</footer>
