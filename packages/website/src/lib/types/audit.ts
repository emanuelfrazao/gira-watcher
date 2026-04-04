import type { ExitStatus, RunType } from './enums.js';

export interface ScrapeRun {
	readonly runId: string;
	readonly runType: RunType;
	readonly commitSha: string;
	readonly githubRunUrl: string | null;
	readonly startedAt: Date;
	readonly finishedAt: Date | null;
	readonly stationsQueried: number | null;
	readonly docksQueried: number | null;
	readonly bikesQueried: number | null;
	readonly recordsWritten: number | null;
	readonly exitStatus: ExitStatus;
}
