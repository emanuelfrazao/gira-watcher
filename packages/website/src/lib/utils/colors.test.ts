import { describe, it, expect } from 'vitest';
import {
	sequentialPalette,
	divergingPalette,
	categoricalPalette,
	statusColors
} from './colors.js';

const HEX_REGEX = /^#[0-9A-Fa-f]{6}$/;

describe('color palettes', () => {
	it('4.1: sequential palette has 5 entries', () => {
		expect(sequentialPalette).toHaveLength(5);
	});

	it('4.2: diverging palette has 5 entries', () => {
		expect(divergingPalette).toHaveLength(5);
	});

	it('4.3: categorical palette has 4 entries', () => {
		expect(categoricalPalette).toHaveLength(4);
	});

	it('4.4: all palette entries are valid hex colors', () => {
		const allColors = [...sequentialPalette, ...divergingPalette, ...categoricalPalette];
		for (const color of allColors) {
			expect(color).toMatch(HEX_REGEX);
		}
	});

	it('4.5: status colors are exported with expected keys', () => {
		expect(statusColors).toHaveProperty('critical');
		expect(statusColors).toHaveProperty('warning');
		expect(statusColors).toHaveProperty('good');
		expect(statusColors).toHaveProperty('excellent');
		expect(statusColors).toHaveProperty('unknown');
	});
});
