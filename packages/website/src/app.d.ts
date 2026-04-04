import type { Locale } from '$lib/types/enums.js';

declare global {
	namespace App {
		interface Locals {
			locale: Locale;
		}
	}
}

export {};
