import type { StationMapPoint } from './metrics.js';

/** GeoJSON FeatureCollection for MapLibre GL JS station layer */
export interface StationGeoJSON {
	readonly type: 'FeatureCollection';
	readonly features: ReadonlyArray<StationFeature>;
}

export interface StationFeature {
	readonly type: 'Feature';
	readonly geometry: {
		readonly type: 'Point';
		readonly coordinates: readonly [longitude: number, latitude: number];
	};
	readonly properties: StationMapPoint;
}

/** Arc data for bike journey map overlay (F15) */
export interface JourneyArc {
	readonly from: readonly [longitude: number, latitude: number];
	readonly to: readonly [longitude: number, latitude: number];
	readonly departedBefore: Date;
	readonly arrivedBy: Date;
}
