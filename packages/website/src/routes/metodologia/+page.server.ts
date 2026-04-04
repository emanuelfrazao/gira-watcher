import type { PageServerLoad } from './$types';
import { getAuditTrail, getObservationCompleteness } from '$lib/server/queries/audit.js';

export const config = {
	isr: { expiration: 3600 }
};

export const load: PageServerLoad = async ({ url }) => {
	const range = url.searchParams.get('range') ?? '30d';
	const [auditTrail, completeness] = await Promise.all([
		getAuditTrail(range),
		getObservationCompleteness(range)
	]);

	return { auditTrail, completeness };
};
