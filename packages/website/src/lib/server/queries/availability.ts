import type { AvailabilityPoint } from '$lib/types/metrics.js';

// TODO: implement with db.ts pool — see Analysis 06 §2.4
export async function getSystemAvailability(range: string): Promise<AvailabilityPoint[]> {
	const now = new Date();
	return Array.from({ length: 24 }, (_, i) => ({
		timestamp: new Date(now.getTime() - (23 - i) * 3600000),
		availability: 0.65 + Math.random() * 0.25,
		rollingAverage24h: 0.75,
		totalBikes: Math.floor(200 + Math.random() * 100),
		totalCapacity: 400
	}));
}
