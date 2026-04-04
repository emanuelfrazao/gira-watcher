<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { locale }: { locale: Locale } = $props();
</script>

<a href="/metodologia">MethodologyLink ({locale})</a>
