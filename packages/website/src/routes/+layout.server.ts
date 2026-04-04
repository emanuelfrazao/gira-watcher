import type { LayoutServerLoad } from './$types';
import { getLatestScrapeRun } from '$lib/server/queries/kpi.js';

export const load: LayoutServerLoad = async ({ locals }) => {
	const lastRun = await getLatestScrapeRun();

	return {
		locale: locals.locale,
		lastScrapeAt: lastRun?.startedAt ?? null,
		lastRun
	};
};
