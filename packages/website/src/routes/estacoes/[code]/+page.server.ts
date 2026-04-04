import type { PageServerLoad } from './$types';
import { getStationDetail } from '$lib/server/queries/station.js';
import { error } from '@sveltejs/kit';

export const config = {
	isr: { expiration: 300 }
};

export const load: PageServerLoad = async ({ params }) => {
	const detail = await getStationDetail(params.code);

	if (!detail) {
		error(404, { message: `Station ${params.code} not found` });
	}

	return { detail };
};
