import type { AuditTrailRow, ObservationCompletenessDay } from '$lib/types/metrics.js';

// TODO: implement with db.ts pool — see Analysis 06 §3.6
export async function getAuditTrail(range: string): Promise<AuditTrailRow[]> {
	const now = new Date();
	return [
		{
			runId: 'run-001',
			runType: 'station',
			startedAt: new Date(now.getTime() - 300000),
			finishedAt: new Date(now.getTime() - 295000),
			exitStatus: 'success',
			recordsWritten: 50,
			commitSha: 'abc1234',
			githubRunUrl: null
		},
		{
			runId: 'run-002',
			runType: 'detail',
			startedAt: new Date(now.getTime() - 600000),
			finishedAt: new Date(now.getTime() - 590000),
			exitStatus: 'success',
			recordsWritten: 320,
			commitSha: 'def5678',
			githubRunUrl: null
		}
	];
}

// TODO: implement with db.ts pool — see Analysis 06 §3.6
export async function getObservationCompleteness(
	range: string
): Promise<ObservationCompletenessDay[]> {
	const now = new Date();
	return Array.from({ length: 7 }, (_, i) => ({
		date: new Date(now.getTime() - (6 - i) * 86400000),
		expectedObservations: 288,
		actualObservations: Math.floor(280 + Math.random() * 8),
		completenessPercent: 0.97 + Math.random() * 0.03
	}));
}
