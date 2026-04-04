import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getStationDetail } from '$lib/server/queries/station.js';

export const GET: RequestHandler = async ({ url }) => {
	const codes = url.searchParams.getAll('station');
	const details = await Promise.all(codes.map((code) => getStationDetail(code)));

	return json({
		data: details.filter((d) => d !== null),
		meta: {
			lastScrapeAt: new Date().toISOString(),
			lastRunId: 'placeholder',
			timeRange: { from: '', to: '' },
			cacheStatus: 'MISS' as const
		}
	});
};
