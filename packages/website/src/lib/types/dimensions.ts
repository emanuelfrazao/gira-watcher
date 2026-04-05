import type { BikeType, StationType } from './enums.js';

export interface Station {
	readonly stationCode: string;
	readonly serialNumber: string;
	readonly name: string;
	readonly description: string | null;
	readonly latitude: number;
	readonly longitude: number;
	readonly stype: StationType;
	readonly zone: string | null;
	readonly creationDate: Date | null;
	readonly totalDocks: number;
	readonly firstSeen: Date;
	readonly lastSeen: Date;
}

export interface Dock {
	readonly dockCode: string;
	readonly serialNumber: string;
	readonly stationCode: string;
	readonly dockNumber: number;
	readonly firstSeen: Date;
	readonly lastSeen: Date;
}

export interface Bike {
	readonly bikeCode: string;
	readonly serialNumber: string;
	readonly name: string;
	readonly bikeType: BikeType | null;
	readonly firstSeen: Date;
	readonly lastSeen: Date;
}
