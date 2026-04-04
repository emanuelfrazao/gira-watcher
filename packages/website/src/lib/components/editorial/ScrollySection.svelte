<script lang="ts">
	import type { Snippet } from 'svelte';

	let { id, children }: { id?: string; children: Snippet } = $props();
</script>

<section {id}>
	{@render children()}
</section>
