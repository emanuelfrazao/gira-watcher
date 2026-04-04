import type { PeakDesertEntry } from '$lib/types/metrics.js';

// TODO: implement with db.ts pool — see Analysis 06 §2.4
export async function getPeakDesertIndex(range: string): Promise<PeakDesertEntry[]> {
	return [
		{
			stationCode: 'A001',
			stationName: 'Av. Duque de Avila',
			peakEmptyRatePct: 0.65,
			overallEmptyRatePct: 0.45,
			delta: 0.20,
			peakStatus: 'DESERT',
			morningEmptyRate: 0.70,
			eveningEmptyRate: 0.55
		},
		{
			stationCode: 'B003',
			stationName: 'Parque das Nacoes',
			peakEmptyRatePct: 0.25,
			overallEmptyRatePct: 0.20,
			delta: 0.05,
			peakStatus: 'OK',
			morningEmptyRate: 0.28,
			eveningEmptyRate: 0.22
		}
	];
}
