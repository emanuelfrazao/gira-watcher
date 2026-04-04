/**
 * All API routes return this envelope.
 * On success, `data` is present and `error` is absent.
 * On failure, `error` is present and `data` is absent.
 */
export type ApiResponse<T> =
	| { readonly data: T; readonly meta: ApiMeta }
	| { readonly error: ApiError; readonly meta: ApiMeta };

export interface ApiMeta {
	readonly lastScrapeAt: string;
	readonly lastRunId: string;
	readonly timeRange: { readonly from: string; readonly to: string };
	readonly cacheStatus: 'HIT' | 'MISS' | 'STALE';
}

export interface ApiError {
	readonly code: 'INVALID_PARAMS' | 'DB_ERROR' | 'NOT_FOUND' | 'INTERNAL';
	readonly message: string;
}
