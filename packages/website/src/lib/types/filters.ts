import type { DayType, StationType, TimeRangePreset } from './enums.js';

/** Concrete time range (resolved from preset or custom picker) */
export interface TimeRange {
	readonly from: Date;
	readonly to: Date;
}

/** Complete filter state -- serializable to/from URL search params */
export interface GlobalFilterState {
	readonly timeRange: TimeRangePreset | TimeRange;
	readonly stationCodes: ReadonlyArray<string>;
	readonly zones: ReadonlyArray<string>;
	readonly stationType: StationType | 'all';
	readonly dayType: DayType;
	readonly hourBand: HourBand;
}

export interface HourBand {
	readonly from: number; // 0-23
	readonly to: number; // 0-23
}

/** Default state: last 7 days, all stations, all zones, all types */
export const DEFAULT_FILTER_STATE: GlobalFilterState = {
	timeRange: '7d',
	stationCodes: [],
	zones: [],
	stationType: 'all',
	dayType: 'all',
	hourBand: { from: 0, to: 23 }
};
