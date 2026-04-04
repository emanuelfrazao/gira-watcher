import type { PageServerLoad } from './$types';
import { getStationMapData, getStationRanking } from '$lib/server/queries/station.js';

export const config = {
	isr: { expiration: 300 }
};

export const load: PageServerLoad = async ({ url }) => {
	const range = url.searchParams.get('range') ?? '7d';
	const [mapData, ranking] = await Promise.all([
		getStationMapData(range),
		getStationRanking({ timeRange: range as '24h' | '7d' | '30d' | '90d' | 'all' })
	]);

	return { mapData, ranking };
};
