import type { KpiValue } from '$lib/types/metrics.js';
import type { ScrapeRun } from '$lib/types/audit.js';

// TODO: implement with db.ts pool — see Analysis 06 §2.4
export async function getKpiValues(range: string): Promise<KpiValue[]> {
	const now = new Date();
	const sparkline = Array.from({ length: 7 }, (_, i) => ({
		timestamp: new Date(now.getTime() - (6 - i) * 86400000),
		value: 0.7 + Math.random() * 0.2
	}));

	return [
		{
			metricId: 'dock_empty_rate',
			currentValue: 0.23,
			previousValue: 0.25,
			delta: -0.02,
			deltaPercent: -8.0,
			healthLevel: 'warning',
			sparklineData: sparkline
		},
		{
			metricId: 'system_availability',
			currentValue: 0.78,
			previousValue: 0.75,
			delta: 0.03,
			deltaPercent: 4.0,
			healthLevel: 'good',
			sparklineData: sparkline
		},
		{
			metricId: 'peak_desert_index',
			currentValue: 0.35,
			previousValue: 0.32,
			delta: 0.03,
			deltaPercent: 9.4,
			healthLevel: 'warning',
			sparklineData: sparkline
		},
		{
			metricId: 'dead_dock_detector',
			currentValue: 12,
			previousValue: 15,
			delta: -3,
			deltaPercent: -20.0,
			healthLevel: 'good',
			sparklineData: sparkline
		},
		{
			metricId: 'dock_functional_rate',
			currentValue: 0.91,
			previousValue: 0.89,
			delta: 0.02,
			deltaPercent: 2.2,
			healthLevel: 'excellent',
			sparklineData: sparkline
		}
	];
}

// TODO: implement with db.ts pool — see Analysis 06 §3.2
export async function getLatestScrapeRun(): Promise<ScrapeRun | null> {
	return {
		runId: 'placeholder-run-001',
		runType: 'station',
		commitSha: 'abc1234',
		githubRunUrl: null,
		startedAt: new Date(),
		finishedAt: new Date(),
		stationsQueried: 50,
		docksQueried: null,
		bikesQueried: null,
		recordsWritten: 50,
		exitStatus: 'success'
	};
}
