import type { Handle } from '@sveltejs/kit';

/**
 * Server hooks for locale handling.
 *
 * TODO: Integrate Paraglide's i18n.handle() for compile-time i18n
 * and localized pathnames. See Analysis 06 §4.
 *
 * Localized pathname mapping (to be implemented with Paraglide):
 *   /estacoes     → /en/stations, /es/estaciones, /fr/stations
 *   /analise      → /en/analysis, /es/analisis,   /fr/analyse
 *   /historias    → /en/stories,  /es/historias,   /fr/histoires
 *   /metodologia  → /en/methodology, /es/metodologia, /fr/methodologie
 *   /sobre        → /en/about,    /es/acerca,     /fr/a-propos
 */

export const handle: Handle = async ({ event, resolve }) => {
	// Default locale is Portuguese
	event.locals.locale = 'pt';

	return resolve(event, {
		transformPageChunk: ({ html }) => html.replace('%sveltekit.lang%', 'pt')
	});
};
