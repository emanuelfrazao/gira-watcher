import type { PageServerLoad } from './$types';

// SSG in production: stories are built at deploy time.
// In the skeleton, we use isr: false (on-demand, cached forever) because
// there are no real story entries to prerender. Switch to `prerender = true`
// with an entries() function once story content exists.
export const config = {
	isr: { expiration: false }
};

export const load: PageServerLoad = async ({ params }) => {
	// TODO: load story content from markdown or CMS
	return {
		slug: params.slug,
		title: 'Placeholder story',
		content: 'Story content will be loaded here.',
		publishedAt: new Date('2026-02-01')
	};
};
