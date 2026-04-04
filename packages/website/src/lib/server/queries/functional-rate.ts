import type { DockFunctionalRateEntry } from '$lib/types/metrics.js';

// TODO: implement with db.ts pool — see Analysis 06 §2.4
export async function getDockFunctionalRate(range: string): Promise<DockFunctionalRateEntry[]> {
	return [
		{
			stationCode: 'A001',
			stationName: 'Av. Duque de Avila',
			totalDocks: 24,
			availableBikes: 8,
			availableEmptyDocks: 12,
			brokenOrUnknownDocks: 4,
			brokenPct: 0.167,
			degradationStatus: 'DEGRADED_WATCH'
		},
		{
			stationCode: 'B003',
			stationName: 'Parque das Nacoes',
			totalDocks: 30,
			availableBikes: 15,
			availableEmptyDocks: 14,
			brokenOrUnknownDocks: 1,
			brokenPct: 0.033,
			degradationStatus: 'OK'
		}
	];
}
