import { describe, it, expect } from 'vitest';
import { resolvePreset } from './time.js';
import type { TimeRangePreset } from '$lib/types/enums.js';

const HOUR = 3600000;
const DAY = 24 * HOUR;

describe('resolvePreset', () => {
	it('3.1: resolves 24h to ~24 hour span', () => {
		const { from, to } = resolvePreset('24h');
		const diff = to.getTime() - from.getTime();
		expect(diff).toBeCloseTo(24 * HOUR, -3);
	});

	it('3.2: resolves 7d to ~7 day span', () => {
		const { from, to } = resolvePreset('7d');
		const diff = to.getTime() - from.getTime();
		expect(diff).toBeCloseTo(7 * DAY, -3);
	});

	it('3.3: resolves 30d to ~30 day span', () => {
		const { from, to } = resolvePreset('30d');
		const diff = to.getTime() - from.getTime();
		expect(diff).toBeCloseTo(30 * DAY, -3);
	});

	it('3.4: resolves 90d to ~90 day span', () => {
		const { from, to } = resolvePreset('90d');
		const diff = to.getTime() - from.getTime();
		expect(diff).toBeCloseTo(90 * DAY, -3);
	});

	it('3.5: resolves all to span from project start to now', () => {
		const { from, to } = resolvePreset('all');
		expect(from.getFullYear()).toBe(2026);
		expect(to.getTime()).toBeCloseTo(Date.now(), -3);
	});

	it('3.6: all presets have to close to now', () => {
		const presets: TimeRangePreset[] = ['24h', '7d', '30d', '90d', 'all'];
		for (const preset of presets) {
			const { to } = resolvePreset(preset);
			expect(Math.abs(to.getTime() - Date.now())).toBeLessThan(5000);
		}
	});

	it('3.7: all presets have from < to', () => {
		const presets: TimeRangePreset[] = ['24h', '7d', '30d', '90d', 'all'];
		for (const preset of presets) {
			const { from, to } = resolvePreset(preset);
			expect(from.getTime()).toBeLessThan(to.getTime());
		}
	});

	it('3.8: all presets return Date instances', () => {
		const presets: TimeRangePreset[] = ['24h', '7d', '30d', '90d', 'all'];
		for (const preset of presets) {
			const { from, to } = resolvePreset(preset);
			expect(from).toBeInstanceOf(Date);
			expect(to).toBeInstanceOf(Date);
		}
	});
});
