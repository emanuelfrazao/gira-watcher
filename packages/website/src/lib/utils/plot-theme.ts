/**
 * Shared Observable Plot theme configuration.
 * Applied as default options to all Plot.plot() calls.
 *
 * TODO: Implement with Observable Plot API — see Analysis 06 §3.1
 */

export const plotTheme = {
	fontFamily: 'Inter, system-ui, sans-serif',
	fontSize: 12,
	backgroundColor: 'transparent',
	color: '#2C2925',
	grid: true,
	marginTop: 20,
	marginRight: 20,
	marginBottom: 30,
	marginLeft: 40
} as const;
