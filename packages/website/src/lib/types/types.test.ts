import { describe, it, expect } from 'vitest';
import { parseFilters, serializeFilters } from '$lib/utils/filters.js';
import { DEFAULT_FILTER_STATE } from '$lib/types/filters.js';

describe('type export contracts', () => {
	it('5.1: filters.ts exports parseFilters', () => {
		expect(typeof parseFilters).toBe('function');
	});

	it('5.2: filters.ts exports serializeFilters', () => {
		expect(typeof serializeFilters).toBe('function');
	});

	it('5.3: filters.ts exports DEFAULT_FILTER_STATE', () => {
		expect(DEFAULT_FILTER_STATE).not.toBeNull();
		expect(typeof DEFAULT_FILTER_STATE).toBe('object');
	});

	it('5.4: DEFAULT_FILTER_STATE has all required fields', () => {
		expect(DEFAULT_FILTER_STATE).toHaveProperty('timeRange');
		expect(DEFAULT_FILTER_STATE).toHaveProperty('stationCodes');
		expect(DEFAULT_FILTER_STATE).toHaveProperty('zones');
		expect(DEFAULT_FILTER_STATE).toHaveProperty('stationType');
		expect(DEFAULT_FILTER_STATE).toHaveProperty('dayType');
		expect(DEFAULT_FILTER_STATE).toHaveProperty('hourBand');
	});

	it('5.5: DEFAULT_FILTER_STATE.stationCodes is an empty array', () => {
		expect(DEFAULT_FILTER_STATE.stationCodes).toEqual([]);
	});

	it('5.6: DEFAULT_FILTER_STATE.zones is an empty array', () => {
		expect(DEFAULT_FILTER_STATE.zones).toEqual([]);
	});

	it('5.7: DEFAULT_FILTER_STATE.timeRange is 7d', () => {
		expect(DEFAULT_FILTER_STATE.timeRange).toBe('7d');
	});
});
