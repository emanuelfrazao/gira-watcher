<script lang="ts">
	import type { Locale } from '$lib/types/enums.js';

	let { locale }: { locale: Locale } = $props();
</script>

<div>LanguageSwitcher — current: {locale}</div>
