<script lang="ts">
	let { text, source }: { text: string; source?: string } = $props();
</script>

<aside>Annotation — {text}{source ? ` (${source})` : ''}</aside>
