import type { TimeRange } from '$lib/types/filters.js';
import type { TimeRangePreset } from '$lib/types/enums.js';

/** Project data collection start date (earliest possible "from" for 'all' preset) */
const PROJECT_START = new Date('2026-01-01T00:00:00Z');

const PRESET_DURATIONS: Record<Exclude<TimeRangePreset, 'all'>, number> = {
	'24h': 24 * 60 * 60 * 1000,
	'7d': 7 * 24 * 60 * 60 * 1000,
	'30d': 30 * 24 * 60 * 60 * 1000,
	'90d': 90 * 24 * 60 * 60 * 1000
};

/**
 * Resolves a TimeRangePreset string into a concrete TimeRange with from/to dates.
 * The `to` date is always the current time. The `from` date is computed by
 * subtracting the preset duration.
 */
export function resolvePreset(preset: TimeRangePreset): TimeRange {
	const to = new Date();

	if (preset === 'all') {
		return { from: PROJECT_START, to };
	}

	const duration = PRESET_DURATIONS[preset];
	const from = new Date(to.getTime() - duration);
	return { from, to };
}
