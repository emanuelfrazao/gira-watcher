import { describe, it, expect } from 'vitest';
import { getKpiValues } from './kpi.js';
import { getSystemAvailability } from './availability.js';
import { getDockEmptyRateHeatmap } from './empty-rate.js';
import { getPeakDesertIndex } from './desert-index.js';
import { getDeadDockSummary } from './dead-dock.js';
import { getDockFunctionalRate } from './functional-rate.js';
import { getStationMapData, getStationRanking } from './station.js';
import { getRateCurves } from './analytics.js';
import { getBikeFleet } from './fleet.js';
import { getAuditTrail } from './audit.js';
import { getStationGeoJSON } from './geo.js';

describe('kpi.ts', () => {
	it('6.1: getKpiValues returns array of length 5', async () => {
		const result = await getKpiValues('7d');
		expect(result).toHaveLength(5);
	});

	it('6.2: each KpiValue has required fields', async () => {
		const result = await getKpiValues('7d');
		for (const kpi of result) {
			expect(kpi).toHaveProperty('metricId');
			expect(kpi).toHaveProperty('currentValue');
			expect(kpi).toHaveProperty('previousValue');
			expect(kpi).toHaveProperty('delta');
			expect(kpi).toHaveProperty('deltaPercent');
			expect(kpi).toHaveProperty('healthLevel');
			expect(kpi).toHaveProperty('sparklineData');
		}
	});
});

describe('availability.ts', () => {
	it('6.3: getSystemAvailability returns non-empty array', async () => {
		const result = await getSystemAvailability('7d');
		expect(result.length).toBeGreaterThan(0);
	});

	it('6.4: each point has required fields', async () => {
		const result = await getSystemAvailability('7d');
		for (const point of result) {
			expect(point).toHaveProperty('timestamp');
			expect(point).toHaveProperty('availability');
			expect(point).toHaveProperty('rollingAverage24h');
			expect(point).toHaveProperty('totalBikes');
			expect(point).toHaveProperty('totalCapacity');
		}
	});
});

describe('empty-rate.ts', () => {
	it('6.5: getDockEmptyRateHeatmap returns array', async () => {
		const result = await getDockEmptyRateHeatmap('7d');
		expect(Array.isArray(result)).toBe(true);
	});
});

describe('desert-index.ts', () => {
	it('6.6: getPeakDesertIndex returns array', async () => {
		const result = await getPeakDesertIndex('7d');
		expect(Array.isArray(result)).toBe(true);
	});
});

describe('dead-dock.ts', () => {
	it('6.7: getDeadDockSummary returns object with flags array', async () => {
		const result = await getDeadDockSummary('7d');
		expect(result).toHaveProperty('totalFlaggedHours');
		expect(result).toHaveProperty('affectedStationCount');
		expect(result).toHaveProperty('excludedObservationPercent');
		expect(result).toHaveProperty('flags');
		expect(Array.isArray(result.flags)).toBe(true);
	});
});

describe('functional-rate.ts', () => {
	it('6.8: getDockFunctionalRate returns array', async () => {
		const result = await getDockFunctionalRate('7d');
		expect(Array.isArray(result)).toBe(true);
	});
});

describe('station.ts', () => {
	it('6.9: getStationMapData returns array', async () => {
		const result = await getStationMapData('7d');
		expect(Array.isArray(result)).toBe(true);
	});

	it('6.10: getStationRanking returns array', async () => {
		const result = await getStationRanking({ timeRange: '7d' });
		expect(Array.isArray(result)).toBe(true);
	});
});

describe('analytics.ts', () => {
	it('6.11: getRateCurves returns array', async () => {
		const result = await getRateCurves('7d');
		expect(Array.isArray(result)).toBe(true);
	});
});

describe('fleet.ts', () => {
	it('6.12: getBikeFleet returns array', async () => {
		const result = await getBikeFleet();
		expect(Array.isArray(result)).toBe(true);
	});
});

describe('audit.ts', () => {
	it('6.13: getAuditTrail returns array', async () => {
		const result = await getAuditTrail('7d');
		expect(Array.isArray(result)).toBe(true);
	});
});

describe('geo.ts', () => {
	it('6.14: getStationGeoJSON returns valid GeoJSON shape', async () => {
		const result = await getStationGeoJSON();
		expect(result.type).toBe('FeatureCollection');
		expect(Array.isArray(result.features)).toBe(true);
	});
});

describe('all query functions', () => {
	it('6.15: all return promises', () => {
		// Verify each function returns a Promise when called
		const results = [
			getKpiValues('7d'),
			getSystemAvailability('7d'),
			getDockEmptyRateHeatmap('7d'),
			getPeakDesertIndex('7d'),
			getDeadDockSummary('7d'),
			getDockFunctionalRate('7d'),
			getStationMapData('7d'),
			getStationRanking({ timeRange: '7d' }),
			getRateCurves('7d'),
			getBikeFleet(),
			getAuditTrail('7d'),
			getStationGeoJSON()
		];
		for (const result of results) {
			expect(result).toBeInstanceOf(Promise);
		}
	});
});
