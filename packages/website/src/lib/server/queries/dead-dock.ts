import type { DeadDockSummary } from '$lib/types/metrics.js';

// TODO: implement with db.ts pool — see Analysis 06 §2.4
export async function getDeadDockSummary(range: string): Promise<DeadDockSummary> {
	const now = new Date();
	return {
		totalFlaggedHours: 156,
		affectedStationCount: 8,
		excludedObservationPercent: 2.3,
		flags: [
			{
				stationCode: 'A005',
				stationName: 'Campo Grande',
				flaggedFrom: new Date(now.getTime() - 12 * 3600000),
				flaggedUntil: new Date(now.getTime() - 4 * 3600000),
				durationHours: 8,
				constantBikeCount: 3
			}
		]
	};
}
