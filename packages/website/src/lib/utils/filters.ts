import { DEFAULT_FILTER_STATE } from '$lib/types/filters.js';
import type { GlobalFilterState, HourBand, TimeRange } from '$lib/types/filters.js';
import type { DayType, StationType, TimeRangePreset } from '$lib/types/enums.js';

const TIME_RANGE_PRESETS: ReadonlyArray<string> = ['24h', '7d', '30d', '90d', 'all'];

/**
 * Parses URL search params into a GlobalFilterState.
 * Missing params are filled from DEFAULT_FILTER_STATE.
 *
 * Encoding:
 *   ?range=7d  OR  ?from=2026-03-01&to=2026-04-01
 *   &station=S001&station=S002
 *   &zone=Z1&zone=Z2
 *   &type=A
 *   &dayType=weekday
 *   &hourFrom=7&hourTo=10
 */
export function parseFilters(params: URLSearchParams): GlobalFilterState {
	const timeRange = parseTimeRange(params);
	const stationCodes = params.getAll('station');
	const zones = params.getAll('zone');

	const typeParam = params.get('type');
	const stationType: StationType | 'all' =
		typeParam === 'A' || typeParam === 'B' ? typeParam : 'all';

	const dayTypeParam = params.get('dayType');
	const dayType: DayType =
		dayTypeParam === 'weekday' || dayTypeParam === 'weekend' ? dayTypeParam : 'all';

	const hourBand = parseHourBand(params);

	return {
		timeRange,
		stationCodes: stationCodes.length > 0 ? stationCodes : DEFAULT_FILTER_STATE.stationCodes,
		zones: zones.length > 0 ? zones : DEFAULT_FILTER_STATE.zones,
		stationType,
		dayType,
		hourBand
	};
}

/**
 * Serializes a GlobalFilterState into URLSearchParams.
 * Default values are omitted to keep URLs clean.
 */
export function serializeFilters(state: GlobalFilterState): URLSearchParams {
	const params = new URLSearchParams();

	// Time range
	if (typeof state.timeRange === 'string') {
		if (state.timeRange !== DEFAULT_FILTER_STATE.timeRange) {
			params.set('range', state.timeRange);
		}
	} else {
		params.set('from', state.timeRange.from.toISOString().split('T')[0]);
		params.set('to', state.timeRange.to.toISOString().split('T')[0]);
	}

	// Station codes
	for (const code of state.stationCodes) {
		params.append('station', code);
	}

	// Zones
	for (const zone of state.zones) {
		params.append('zone', zone);
	}

	// Station type
	if (state.stationType !== 'all') {
		params.set('type', state.stationType);
	}

	// Day type
	if (state.dayType !== 'all') {
		params.set('dayType', state.dayType);
	}

	// Hour band
	if (state.hourBand.from !== 0 || state.hourBand.to !== 23) {
		params.set('hourFrom', String(state.hourBand.from));
		params.set('hourTo', String(state.hourBand.to));
	}

	return params;
}

function parseTimeRange(params: URLSearchParams): TimeRangePreset | TimeRange {
	const rangeParam = params.get('range');
	if (rangeParam && TIME_RANGE_PRESETS.includes(rangeParam)) {
		return rangeParam as TimeRangePreset;
	}

	const fromParam = params.get('from');
	const toParam = params.get('to');
	if (fromParam && toParam) {
		const from = new Date(fromParam);
		const to = new Date(toParam);
		if (!isNaN(from.getTime()) && !isNaN(to.getTime())) {
			return { from, to };
		}
	}

	return DEFAULT_FILTER_STATE.timeRange;
}

function parseHourBand(params: URLSearchParams): HourBand {
	const fromParam = params.get('hourFrom');
	const toParam = params.get('hourTo');

	if (fromParam !== null && toParam !== null) {
		const from = parseInt(fromParam, 10);
		const to = parseInt(toParam, 10);
		if (!isNaN(from) && !isNaN(to) && from >= 0 && from <= 23 && to >= 0 && to <= 23) {
			return { from, to };
		}
	}

	return DEFAULT_FILTER_STATE.hourBand;
}
