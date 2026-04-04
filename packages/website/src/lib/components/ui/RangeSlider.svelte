<script lang="ts">
	let { min = 0, max = 23, from, to, label }: {
		min?: number;
		max?: number;
		from: number;
		to: number;
		label: string;
	} = $props();
</script>

<div>RangeSlider — {label}: {from}-{to} (range: {min}-{max})</div>
