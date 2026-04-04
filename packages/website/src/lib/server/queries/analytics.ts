import type { RateCurvePoint, HourlyHeatmapCell } from '$lib/types/metrics.js';

// TODO: implement with db.ts pool — see Analysis 06 §3.5
export async function getRateCurves(range: string): Promise<RateCurvePoint[]> {
	return Array.from({ length: 24 }, (_, i) => ({
		hourOfDay: i,
		arrivals: Math.floor(10 + Math.random() * 30),
		departures: Math.floor(10 + Math.random() * 30),
		arrivalRateCorrected: 10 + Math.random() * 30,
		departureRateCorrected: 10 + Math.random() * 30,
		rebalancingEvents: Math.floor(Math.random() * 5),
		arrivalCiUpper: 35 + Math.random() * 10,
		arrivalCiLower: 5 + Math.random() * 5,
		departureCiUpper: 35 + Math.random() * 10,
		departureCiLower: 5 + Math.random() * 5
	}));
}

// TODO: implement with db.ts pool — see Analysis 06 §3.5
export async function getHourlyHeatmap(range: string): Promise<HourlyHeatmapCell[]> {
	const cells: HourlyHeatmapCell[] = [];
	for (let day = 0; day < 7; day++) {
		for (let hour = 0; hour < 24; hour++) {
			cells.push({
				dayOfWeek: day,
				hourOfDay: hour,
				averageAvailability: 0.5 + Math.random() * 0.4
			});
		}
	}
	return cells;
}
