export type StationType = 'A' | 'B';
export type AssetStatus = 'active' | 'repair';
export type DockState = 'empty' | 'occupied';
export type BikeType = 'electric' | 'conventional';
export type RunType = 'station' | 'detail';
export type ExitStatus = 'success' | 'partial' | 'error';
export type PeakPeriod = 'morning' | 'evening' | 'off_peak';
export type PeakStatus = 'DESERT' | 'OK';
export type DegradationStatus = 'STRUCTURALLY_DEGRADED' | 'DEGRADED_WATCH' | 'OK';
export type DeadDockStatus = 'FLAGGED' | 'OK';
export type BikeActivityStatus = 'ACTIVE' | 'STATIONARY' | 'IDLE_SUSPICIOUS';

/** Semantic health thresholds for KPI cards */
export type HealthLevel = 'critical' | 'warning' | 'good' | 'excellent';

/** Supported locales */
export type Locale = 'pt' | 'en' | 'es' | 'fr';

/** Time range presets available in filters */
export type TimeRangePreset = '24h' | '7d' | '30d' | '90d' | 'all';

/** Day type filter */
export type DayType = 'weekday' | 'weekend' | 'all';
