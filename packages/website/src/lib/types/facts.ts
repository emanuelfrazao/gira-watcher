import type { AssetStatus, DockState } from './enums.js';

export interface StationSnapshot {
	readonly stationCode: string;
	readonly observedAt: Date;
	readonly runId: string;
	readonly bikes: number;
	readonly docks: number;
	readonly assetStatus: AssetStatus;
	readonly version: number;
	readonly updateDate: Date;
}

export interface DockSnapshot {
	readonly dockCode: string;
	readonly observedAt: Date;
	readonly runId: string;
	readonly state: DockState;
	readonly bikeCode: string | null;
}

export interface BikeSnapshot {
	readonly bikeCode: string;
	readonly observedAt: Date;
	readonly runId: string;
	readonly dockCode: string;
	readonly stationCode: string;
	readonly battery: number | null;
}
