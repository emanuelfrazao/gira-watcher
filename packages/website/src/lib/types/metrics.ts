import type {
	BikeActivityStatus,
	BikeType,
	DegradationStatus,
	DockState,
	ExitStatus,
	HealthLevel,
	PeakStatus,
	RunType,
	StationType
} from './enums.js';
import type { Station } from './dimensions.js';

/** F01: Single KPI card data */
export interface KpiValue {
	readonly metricId: MetricId;
	readonly currentValue: number;
	readonly previousValue: number;
	readonly delta: number;
	readonly deltaPercent: number;
	readonly healthLevel: HealthLevel;
	readonly sparklineData: ReadonlyArray<TimeSeriesPoint>;
}

export type MetricId =
	| 'dock_empty_rate'
	| 'system_availability'
	| 'peak_desert_index'
	| 'dead_dock_detector'
	| 'dock_functional_rate';

/** Generic time-series point used across multiple charts */
export interface TimeSeriesPoint {
	readonly timestamp: Date;
	readonly value: number;
}

/** F02: System-wide availability at a point in time */
export interface AvailabilityPoint {
	readonly timestamp: Date;
	readonly availability: number;
	readonly rollingAverage24h: number | null;
	readonly totalBikes: number;
	readonly totalCapacity: number;
}

/** F03: Dock empty rate per station per day (heatmap cell) */
export interface DockEmptyRateCell {
	readonly stationCode: string;
	readonly stationName: string;
	readonly date: Date;
	readonly emptyRatePct: number;
	readonly rollingAvg30d: number | null;
}

/** F04: Peak-hour desert index per station */
export interface PeakDesertEntry {
	readonly stationCode: string;
	readonly stationName: string;
	readonly peakEmptyRatePct: number;
	readonly overallEmptyRatePct: number;
	readonly delta: number;
	readonly peakStatus: PeakStatus;
	readonly morningEmptyRate: number;
	readonly eveningEmptyRate: number;
}

/** F05: Dead dock flagged period */
export interface DeadDockFlag {
	readonly stationCode: string;
	readonly stationName: string;
	readonly flaggedFrom: Date;
	readonly flaggedUntil: Date;
	readonly durationHours: number;
	readonly constantBikeCount: number;
}

/** F05: Dead dock summary statistics */
export interface DeadDockSummary {
	readonly totalFlaggedHours: number;
	readonly affectedStationCount: number;
	readonly excludedObservationPercent: number;
	readonly flags: ReadonlyArray<DeadDockFlag>;
}

/** F06: Dock functional rate per station */
export interface DockFunctionalRateEntry {
	readonly stationCode: string;
	readonly stationName: string;
	readonly totalDocks: number;
	readonly availableBikes: number;
	readonly availableEmptyDocks: number;
	readonly brokenOrUnknownDocks: number;
	readonly brokenPct: number;
	readonly degradationStatus: DegradationStatus;
}

/** F07: Station marker data for map rendering */
export interface StationMapPoint {
	readonly stationCode: string;
	readonly name: string;
	readonly latitude: number;
	readonly longitude: number;
	readonly stype: StationType;
	readonly zone: string | null;
	readonly bikes: number;
	readonly docks: number;
	readonly totalDocks: number;
	readonly availabilityPct: number;
	readonly healthLevel: HealthLevel;
}

/** F08: Station ranking row (composite of multiple metrics) */
export interface StationRankingRow {
	readonly stationCode: string;
	readonly stationName: string;
	readonly zone: string | null;
	readonly stype: StationType;
	readonly currentBikes: number;
	readonly currentEmptyDocks: number;
	readonly emptyRate7d: number;
	readonly emptyRate30d: number;
	readonly functionalRate: number;
	readonly peakStatus: PeakStatus;
	readonly deadDockFlagCount: number;
	readonly sparklineData: ReadonlyArray<TimeSeriesPoint>;
}

/** F09: Full station detail (composed from multiple queries) */
export interface StationDetail {
	readonly station: Station;
	readonly currentSnapshot: StationSnapshot;
	readonly availabilityTimeline24h: ReadonlyArray<AvailabilityPoint>;
	readonly availabilityTrend30d: ReadonlyArray<AvailabilityPoint>;
	readonly functionalRateHistory: ReadonlyArray<DockFunctionalRateEntry>;
	readonly peakPerformance: PeakDesertEntry;
	readonly deadDockEvents: ReadonlyArray<DeadDockFlag>;
	readonly dataQuality: StationDataQuality;
}

/** Import StationSnapshot for StationDetail */
import type { StationSnapshot } from './facts.js';

/** F09: Data quality summary for one station */
export interface StationDataQuality {
	readonly observationCompleteness: number;
	readonly gapCount: number;
	readonly longestGapMinutes: number;
	readonly staleUpdateDateAlerts: number;
}

/** F11: Arrival/departure rate curve point */
export interface RateCurvePoint {
	readonly hourOfDay: number;
	readonly arrivals: number;
	readonly departures: number;
	readonly arrivalRateCorrected: number;
	readonly departureRateCorrected: number;
	readonly rebalancingEvents: number;
	readonly arrivalCiUpper: number;
	readonly arrivalCiLower: number;
	readonly departureCiUpper: number;
	readonly departureCiLower: number;
}

/** F12: Hourly availability heatmap cell (day-of-week x hour) */
export interface HourlyHeatmapCell {
	readonly dayOfWeek: number;
	readonly hourOfDay: number;
	readonly averageAvailability: number;
}

/** F13: Dock-level occupancy grid cell */
export interface DockOccupancyCell {
	readonly dockCode: string;
	readonly dockNumber: number;
	readonly timestamp: Date;
	readonly state: DockState;
	readonly bikeCode: string | null;
}

/** F14: Bike fleet row */
export interface BikeFleetRow {
	readonly bikeCode: string;
	readonly bikeName: string;
	readonly bikeType: BikeType | null;
	readonly currentStationCode: string | null;
	readonly currentStationName: string | null;
	readonly battery: number | null;
	readonly lastMovement: Date | null;
	readonly activityStatus: BikeActivityStatus;
	readonly distinctStationsVisited: number;
}

/** F15: Bike trip segment */
export interface BikeTripSegment {
	readonly bikeCode: string;
	readonly fromStationCode: string;
	readonly fromStationName: string;
	readonly fromLat: number;
	readonly fromLon: number;
	readonly toStationCode: string;
	readonly toStationName: string;
	readonly toLat: number;
	readonly toLon: number;
	readonly departedBefore: Date;
	readonly arrivedBy: Date;
	readonly tripDurationHours: number;
	readonly batteryAtDeparture: number | null;
	readonly batteryAtArrival: number | null;
}

/** F16: Battery observation */
export interface BatteryObservation {
	readonly bikeCode: string;
	readonly observedAt: Date;
	readonly battery: number;
}

/** F21: Audit trail row (presentation-friendly projection of ScrapeRun) */
export interface AuditTrailRow {
	readonly runId: string;
	readonly runType: RunType;
	readonly startedAt: Date;
	readonly finishedAt: Date | null;
	readonly exitStatus: ExitStatus;
	readonly recordsWritten: number | null;
	readonly commitSha: string;
	readonly githubRunUrl: string | null;
}

/** F21: Daily observation completeness */
export interface ObservationCompletenessDay {
	readonly date: Date;
	readonly expectedObservations: number;
	readonly actualObservations: number;
	readonly completenessPercent: number;
}
