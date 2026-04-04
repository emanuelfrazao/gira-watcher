/**
 * Shared MapLibre GL JS configuration.
 *
 * TODO: Implement with MapLibre API — see Analysis 06 §3.2
 */

/** Default map center: Lisbon (Praca do Comercio) */
export const DEFAULT_CENTER: readonly [number, number] = [-9.1393, 38.7073];

/** Default zoom level for city overview */
export const DEFAULT_ZOOM = 12;

/** Station marker circle radius steps by zoom level */
export const MARKER_RADIUS = {
	min: 4,
	max: 10,
	zoomMin: 10,
	zoomMax: 15
} as const;
