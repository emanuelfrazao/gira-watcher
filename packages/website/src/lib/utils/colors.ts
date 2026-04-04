/** Sequential palette (YlGn — ColorBrewer 5-class) */
export const sequentialPalette: readonly string[] = [
	'#FFFFCC',
	'#C2E699',
	'#78C679',
	'#31A354',
	'#006837'
];

/** Diverging palette (RdYlGn — ColorBrewer 5-class) */
export const divergingPalette: readonly string[] = [
	'#D73027',
	'#FC8D59',
	'#FEE08B',
	'#91CF60',
	'#1A9850'
];

/** Categorical palette (Okabe-Ito subset — 4 colors) */
export const categoricalPalette: readonly string[] = [
	'#E69F00',
	'#56B4E9',
	'#009E73',
	'#0072B2'
];

/** Semantic status colors for health indicators */
export const statusColors = {
	critical: '#D55E00',
	warning: '#E69F00',
	good: '#009E73',
	excellent: '#056449',
	unknown: '#9C9690'
} as const;
