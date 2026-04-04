import { describe, it, expect } from 'vitest';
import { formatPercent, formatNumber, formatDate, formatTime } from './format.js';

describe('formatPercent', () => {
	it('2.1: formats 0.781 with PT locale', () => {
		const result = formatPercent(0.781, 'pt');
		expect(result).toContain('78');
		expect(result).toContain('%');
	});

	it('2.2: formats 0 correctly', () => {
		const result = formatPercent(0, 'pt');
		expect(result).toContain('0');
		expect(result).toContain('%');
	});

	it('2.3: formats 1 as 100%', () => {
		const result = formatPercent(1, 'pt');
		expect(result).toContain('100');
		expect(result).toContain('%');
	});
});

describe('formatNumber', () => {
	it('2.4: formats 1234 with PT locale using dot separator', () => {
		const result = formatNumber(1234, 'pt');
		// Portuguese uses dot or space as thousands separator
		expect(result.replace(/\s/g, '')).toMatch(/1[.\u00a0]?234/);
	});

	it('2.5: formats 0', () => {
		const result = formatNumber(0, 'pt');
		expect(result).toBe('0');
	});
});

describe('formatDate', () => {
	it('2.6: short format returns non-empty string with day', () => {
		const date = new Date('2026-03-15');
		const result = formatDate(date, 'short', 'pt');
		expect(result.length).toBeGreaterThan(0);
		expect(result).toContain('15');
	});

	it('2.7: long format is longer than short for same date', () => {
		const date = new Date('2026-03-15');
		const short = formatDate(date, 'short', 'pt');
		const long = formatDate(date, 'long', 'pt');
		expect(long.length).toBeGreaterThan(short.length);
	});
});

describe('formatTime', () => {
	it('2.8: EN locale uses AM/PM', () => {
		const date = new Date('2026-03-15T14:30:00');
		const result = formatTime(date, 'en');
		expect(result).toMatch(/[AaPp][Mm]/);
	});

	it('2.9: PT locale does not use AM/PM', () => {
		const date = new Date('2026-03-15T14:30:00');
		const result = formatTime(date, 'pt');
		expect(result).not.toMatch(/[AaPp][Mm]/);
	});
});
