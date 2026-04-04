import type { BikeFleetRow, BikeTripSegment } from '$lib/types/metrics.js';

// TODO: implement with db.ts pool — see Analysis 06 §3.5
export async function getBikeFleet(): Promise<BikeFleetRow[]> {
	return [
		{
			bikeCode: 'E001',
			bikeName: 'GIRA E001',
			bikeType: 'electric',
			currentStationCode: 'A001',
			currentStationName: 'Av. Duque de Avila',
			battery: 78,
			lastMovement: new Date(),
			activityStatus: 'ACTIVE',
			distinctStationsVisited: 12
		},
		{
			bikeCode: 'C042',
			bikeName: 'GIRA C042',
			bikeType: 'conventional',
			currentStationCode: 'B003',
			currentStationName: 'Parque das Nacoes',
			battery: null,
			lastMovement: new Date(Date.now() - 86400000),
			activityStatus: 'STATIONARY',
			distinctStationsVisited: 5
		}
	];
}

// TODO: implement with db.ts pool — see Analysis 06 §3.5
export async function getBikeTrips(bikeCode: string): Promise<BikeTripSegment[]> {
	const now = new Date();
	return [
		{
			bikeCode,
			fromStationCode: 'A001',
			fromStationName: 'Av. Duque de Avila',
			fromLat: 38.734,
			fromLon: -9.146,
			toStationCode: 'B003',
			toStationName: 'Parque das Nacoes',
			toLat: 38.768,
			toLon: -9.094,
			departedBefore: new Date(now.getTime() - 3600000),
			arrivedBy: new Date(now.getTime() - 2400000),
			tripDurationHours: 0.33,
			batteryAtDeparture: 85,
			batteryAtArrival: 72
		}
	];
}
