import type { PageServerLoad } from './$types';
import { getKpiValues } from '$lib/server/queries/kpi.js';
import { getSystemAvailability } from '$lib/server/queries/availability.js';

export const config = {
	isr: { expiration: 300 }
};

export const load: PageServerLoad = async ({ url }) => {
	const range = url.searchParams.get('range') ?? '7d';
	const [kpis, availability] = await Promise.all([
		getKpiValues(range),
		getSystemAvailability(range)
	]);

	return { kpis, availability };
};
