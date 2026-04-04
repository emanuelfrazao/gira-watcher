<script lang="ts">
	let { checked = false, label }: { checked?: boolean; label: string } = $props();
</script>

<div>Toggle — {label}: {checked ? 'on' : 'off'}</div>
