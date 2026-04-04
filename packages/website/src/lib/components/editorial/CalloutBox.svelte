<script lang="ts">
	import type { Snippet } from 'svelte';

	let { variant = 'info', children }: {
		variant?: 'info' | 'warning' | 'critical';
		children: Snippet;
	} = $props();
</script>

<div data-variant={variant}>
	{@render children()}
</div>
