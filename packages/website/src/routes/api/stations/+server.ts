import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getStationMapData } from '$lib/server/queries/station.js';

export const GET: RequestHandler = async ({ url }) => {
	const range = url.searchParams.get('range') ?? '7d';
	const data = await getStationMapData(range);
	return json({ data, meta: placeholderMeta() });
};

function placeholderMeta() {
	return {
		lastScrapeAt: new Date().toISOString(),
		lastRunId: 'placeholder',
		timeRange: { from: '', to: '' },
		cacheStatus: 'MISS' as const
	};
}
