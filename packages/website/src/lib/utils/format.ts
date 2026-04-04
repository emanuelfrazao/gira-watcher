import type { Locale } from '$lib/types/enums.js';

const LOCALE_MAP: Record<Locale, string> = {
	pt: 'pt-PT',
	en: 'en-GB',
	es: 'es-ES',
	fr: 'fr-FR'
};

export function formatPercent(value: number, locale: Locale): string {
	return new Intl.NumberFormat(LOCALE_MAP[locale], {
		style: 'percent',
		minimumFractionDigits: 1,
		maximumFractionDigits: 1
	}).format(value);
}

export function formatNumber(value: number, locale: Locale): string {
	return new Intl.NumberFormat(LOCALE_MAP[locale]).format(value);
}

export function formatDate(date: Date, style: 'short' | 'long', locale: Locale): string {
	const options: Intl.DateTimeFormatOptions =
		style === 'short'
			? { day: 'numeric', month: 'short' }
			: { day: 'numeric', month: 'long', year: 'numeric' };
	return new Intl.DateTimeFormat(LOCALE_MAP[locale], options).format(date);
}

export function formatTime(date: Date, locale: Locale): string {
	const hour12 = locale === 'en';
	return new Intl.DateTimeFormat(LOCALE_MAP[locale], {
		hour: 'numeric',
		minute: '2-digit',
		hour12
	}).format(date);
}
