import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getLatestScrapeRun } from '$lib/server/queries/kpi.js';

export const GET: RequestHandler = async () => {
	const lastRun = await getLatestScrapeRun();
	return json({
		data: lastRun,
		meta: {
			lastScrapeAt: lastRun?.startedAt.toISOString() ?? '',
			lastRunId: lastRun?.runId ?? '',
			timeRange: { from: '', to: '' },
			cacheStatus: 'MISS' as const
		}
	});
};
