<script lang="ts">
	let { options, selected, placeholder = 'Search...' }: {
		options: ReadonlyArray<{ value: string; label: string }>;
		selected: ReadonlyArray<string>;
		placeholder?: string;
	} = $props();
</script>

<div>SearchableSelect — {selected.length}/{options.length} selected, "{placeholder}"</div>
