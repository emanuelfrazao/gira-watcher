import { describe, it, expect } from 'vitest';
import { parseFilters, serializeFilters } from './filters.js';
import { DEFAULT_FILTER_STATE } from '$lib/types/filters.js';
import type { GlobalFilterState } from '$lib/types/filters.js';

describe('filter serialization round-trip', () => {
	it('1.1: round-trips default filter state', () => {
		const serialized = serializeFilters(DEFAULT_FILTER_STATE);
		const parsed = parseFilters(serialized);
		expect(parsed).toEqual(DEFAULT_FILTER_STATE);
	});

	it('1.2: round-trips state with preset time range', () => {
		const state: GlobalFilterState = { ...DEFAULT_FILTER_STATE, timeRange: '30d' };
		const parsed = parseFilters(serializeFilters(state));
		expect(parsed.timeRange).toBe('30d');
	});

	it('1.3: round-trips state with custom time range', () => {
		const from = new Date('2026-03-01');
		const to = new Date('2026-03-31');
		const state: GlobalFilterState = { ...DEFAULT_FILTER_STATE, timeRange: { from, to } };
		const parsed = parseFilters(serializeFilters(state));
		expect(typeof parsed.timeRange).toBe('object');
		const tr = parsed.timeRange as { from: Date; to: Date };
		expect(tr.from.toISOString().split('T')[0]).toBe('2026-03-01');
		expect(tr.to.toISOString().split('T')[0]).toBe('2026-03-31');
	});

	it('1.4: round-trips state with multiple station codes', () => {
		const state: GlobalFilterState = {
			...DEFAULT_FILTER_STATE,
			stationCodes: ['A01', 'A02', 'B05']
		};
		const parsed = parseFilters(serializeFilters(state));
		expect(parsed.stationCodes).toEqual(['A01', 'A02', 'B05']);
	});

	it('1.5: round-trips state with multiple zones', () => {
		const state: GlobalFilterState = { ...DEFAULT_FILTER_STATE, zones: ['Z1', 'Z2'] };
		const parsed = parseFilters(serializeFilters(state));
		expect(parsed.zones).toEqual(['Z1', 'Z2']);
	});

	it('1.6: round-trips all fields populated (non-default)', () => {
		const state: GlobalFilterState = {
			timeRange: '90d',
			stationCodes: ['A01', 'B02'],
			zones: ['Centro', 'Oriental'],
			stationType: 'A',
			dayType: 'weekday',
			hourBand: { from: 7, to: 10 }
		};
		const parsed = parseFilters(serializeFilters(state));
		expect(parsed).toEqual(state);
	});
});

describe('parseFilters', () => {
	it('1.7: returns DEFAULT_FILTER_STATE for empty params', () => {
		const parsed = parseFilters(new URLSearchParams());
		expect(parsed).toEqual(DEFAULT_FILTER_STATE);
	});

	it('1.8: fills missing params from defaults (partial: only range)', () => {
		const params = new URLSearchParams('range=24h');
		const parsed = parseFilters(params);
		expect(parsed.timeRange).toBe('24h');
		expect(parsed.stationCodes).toEqual(DEFAULT_FILTER_STATE.stationCodes);
		expect(parsed.zones).toEqual(DEFAULT_FILTER_STATE.zones);
		expect(parsed.stationType).toBe('all');
		expect(parsed.dayType).toBe('all');
	});

	it('1.10: parses hourBand boundary values', () => {
		const params = new URLSearchParams('hourFrom=0&hourTo=23');
		const parsed = parseFilters(params);
		expect(parsed.hourBand).toEqual({ from: 0, to: 23 });
	});

	it('1.11: parses hourBand typical values', () => {
		const params = new URLSearchParams('hourFrom=7&hourTo=10');
		const parsed = parseFilters(params);
		expect(parsed.hourBand).toEqual({ from: 7, to: 10 });
	});
});

describe('serializeFilters', () => {
	it('1.9: produces expected param keys for non-default state', () => {
		const state: GlobalFilterState = {
			timeRange: '30d',
			stationCodes: ['A01'],
			zones: ['Z1'],
			stationType: 'B',
			dayType: 'weekend',
			hourBand: { from: 8, to: 18 }
		};
		const params = serializeFilters(state);
		expect(params.get('range')).toBe('30d');
		expect(params.getAll('station')).toEqual(['A01']);
		expect(params.getAll('zone')).toEqual(['Z1']);
		expect(params.get('type')).toBe('B');
		expect(params.get('dayType')).toBe('weekend');
		expect(params.get('hourFrom')).toBe('8');
		expect(params.get('hourTo')).toBe('18');
	});

	it('1.12: default state produces minimal params', () => {
		const params = serializeFilters(DEFAULT_FILTER_STATE);
		expect(params.toString()).toBe('');
	});
});
