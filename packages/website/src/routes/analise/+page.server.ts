import type { PageServerLoad } from './$types';
import { getRateCurves, getHourlyHeatmap } from '$lib/server/queries/analytics.js';

export const config = {
	isr: { expiration: 3600 }
};

export const load: PageServerLoad = async ({ url }) => {
	const range = url.searchParams.get('range') ?? '30d';
	const [rateCurves, heatmap] = await Promise.all([
		getRateCurves(range),
		getHourlyHeatmap(range)
	]);

	return { rateCurves, heatmap };
};
