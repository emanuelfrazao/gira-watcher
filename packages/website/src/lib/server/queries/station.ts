import type { StationMapPoint, StationRankingRow, StationDetail } from '$lib/types/metrics.js';
import type { Station } from '$lib/types/dimensions.js';
import type { GlobalFilterState } from '$lib/types/filters.js';

// TODO: implement with db.ts pool — see Analysis 06 §3.4
export async function getStationMapData(range: string): Promise<StationMapPoint[]> {
	return [
		{
			stationCode: 'A001',
			name: 'Av. Duque de Avila',
			latitude: 38.7340,
			longitude: -9.1460,
			stype: 'A',
			zone: 'Centro',
			bikes: 8,
			docks: 12,
			totalDocks: 24,
			availabilityPct: 0.33,
			healthLevel: 'warning'
		},
		{
			stationCode: 'B003',
			name: 'Parque das Nacoes',
			latitude: 38.7680,
			longitude: -9.0940,
			stype: 'B',
			zone: 'Oriental',
			bikes: 15,
			docks: 14,
			totalDocks: 30,
			availabilityPct: 0.50,
			healthLevel: 'good'
		}
	];
}

// TODO: implement with db.ts pool — see Analysis 06 §3.4
export async function getStationRanking(filters: Partial<GlobalFilterState>): Promise<StationRankingRow[]> {
	const now = new Date();
	const sparkline = Array.from({ length: 7 }, (_, i) => ({
		timestamp: new Date(now.getTime() - (6 - i) * 86400000),
		value: 0.3 + Math.random() * 0.4
	}));

	return [
		{
			stationCode: 'A001',
			stationName: 'Av. Duque de Avila',
			zone: 'Centro',
			stype: 'A',
			currentBikes: 8,
			currentEmptyDocks: 12,
			emptyRate7d: 0.45,
			emptyRate30d: 0.42,
			functionalRate: 0.83,
			peakStatus: 'DESERT',
			deadDockFlagCount: 2,
			sparklineData: sparkline
		}
	];
}

// TODO: implement with db.ts pool — see Analysis 06 §3.4
export async function getStationDetail(code: string): Promise<StationDetail | null> {
	const now = new Date();
	return {
		station: {
			stationCode: code,
			serialNumber: 'SN001',
			name: 'Av. Duque de Avila',
			description: null,
			latitude: 38.7340,
			longitude: -9.1460,
			stype: 'A',
			zone: 'Centro',
			creationDate: null,
			totalDocks: 24,
			firstSeen: new Date('2026-01-01'),
			lastSeen: now
		},
		currentSnapshot: {
			stationCode: code,
			observedAt: now,
			runId: 'placeholder-run-001',
			bikes: 8,
			docks: 12,
			assetStatus: 'active',
			version: 1,
			updateDate: now
		},
		availabilityTimeline24h: [],
		availabilityTrend30d: [],
		functionalRateHistory: [],
		peakPerformance: {
			stationCode: code,
			stationName: 'Av. Duque de Avila',
			peakEmptyRatePct: 0.65,
			overallEmptyRatePct: 0.45,
			delta: 0.20,
			peakStatus: 'DESERT',
			morningEmptyRate: 0.70,
			eveningEmptyRate: 0.55
		},
		deadDockEvents: [],
		dataQuality: {
			observationCompleteness: 0.97,
			gapCount: 3,
			longestGapMinutes: 15,
			staleUpdateDateAlerts: 0
		}
	};
}

// TODO: implement with db.ts pool — see Analysis 06 §3.4
export async function searchStations(
	query: string
): Promise<Pick<Station, 'stationCode' | 'name' | 'zone' | 'stype'>[]> {
	return [
		{ stationCode: 'A001', name: 'Av. Duque de Avila', zone: 'Centro', stype: 'A' },
		{ stationCode: 'B003', name: 'Parque das Nacoes', zone: 'Oriental', stype: 'B' }
	];
}
