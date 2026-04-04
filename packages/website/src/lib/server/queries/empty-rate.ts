import type { DockEmptyRateCell } from '$lib/types/metrics.js';

// TODO: implement with db.ts pool — see Analysis 06 §2.4
export async function getDockEmptyRateHeatmap(range: string): Promise<DockEmptyRateCell[]> {
	const now = new Date();
	return [
		{
			stationCode: 'A001',
			stationName: 'Av. Duque de Avila',
			date: now,
			emptyRatePct: 0.45,
			rollingAvg30d: 0.42
		},
		{
			stationCode: 'A002',
			stationName: 'Praca do Comercio',
			date: now,
			emptyRatePct: 0.30,
			rollingAvg30d: 0.28
		}
	];
}
