<script lang="ts">
	import type { Snippet } from 'svelte';

	let { title, description, height = 400, children }: {
		title: string;
		description?: string;
		height?: number;
		children: Snippet;
	} = $props();
</script>

<figure>
	<figcaption>{title}{description ? ` — ${description}` : ''}</figcaption>
	<div style="height: {height}px">
		{@render children()}
	</div>
</figure>
