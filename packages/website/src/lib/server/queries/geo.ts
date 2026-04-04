import type { StationGeoJSON } from '$lib/types/chart-data.js';

/** Zone-level aggregation data */
export interface ZoneData {
	readonly zone: string;
	readonly stationCount: number;
	readonly avgAvailability: number;
}

// TODO: implement with db.ts pool — see Analysis 06 §3.5
export async function getStationGeoJSON(): Promise<StationGeoJSON> {
	return {
		type: 'FeatureCollection',
		features: [
			{
				type: 'Feature',
				geometry: {
					type: 'Point',
					coordinates: [-9.146, 38.734]
				},
				properties: {
					stationCode: 'A001',
					name: 'Av. Duque de Avila',
					latitude: 38.734,
					longitude: -9.146,
					stype: 'A',
					zone: 'Centro',
					bikes: 8,
					docks: 12,
					totalDocks: 24,
					availabilityPct: 0.33,
					healthLevel: 'warning'
				}
			},
			{
				type: 'Feature',
				geometry: {
					type: 'Point',
					coordinates: [-9.094, 38.768]
				},
				properties: {
					stationCode: 'B003',
					name: 'Parque das Nacoes',
					latitude: 38.768,
					longitude: -9.094,
					stype: 'B',
					zone: 'Oriental',
					bikes: 15,
					docks: 14,
					totalDocks: 30,
					availabilityPct: 0.5,
					healthLevel: 'good'
				}
			}
		]
	};
}

// TODO: implement with db.ts pool
export async function getZoneAggregations(): Promise<ZoneData[]> {
	return [
		{ zone: 'Centro', stationCount: 15, avgAvailability: 0.65 },
		{ zone: 'Oriental', stationCount: 8, avgAvailability: 0.72 }
	];
}
