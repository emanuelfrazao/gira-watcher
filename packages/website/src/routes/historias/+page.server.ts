import type { PageServerLoad } from './$types';

export const config = {
	isr: { expiration: 3600 }
};

export const load: PageServerLoad = async () => {
	// TODO: load story index from CMS or markdown files
	return {
		stories: [
			{
				slug: 'primeiro-mes',
				title: 'O primeiro mes de dados',
				excerpt: 'Analise exploratoria dos primeiros 30 dias de recolha de dados.',
				publishedAt: new Date('2026-02-01')
			}
		]
	};
};
