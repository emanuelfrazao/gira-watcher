<script lang="ts">
	let { segments }: { segments: ReadonlyArray<{ label: string; href: string }> } = $props();
</script>

<nav aria-label="breadcrumb">
	<div>Breadcrumb — {segments.length} segments</div>
</nav>
