import { error } from '@sveltejs/kit';
import { ORACLES_ENABLED } from '$lib/config/features';

/**
 * Guard every ``/oracles/*`` page behind the Oracles feature flag.
 *
 * Returning a 404 (rather than redirecting) means the routes simply don't
 * exist for deployments without the agents sidecar - no stale UI, and no
 * confusing redirect loops if the flag flips at build time.
 */
export const load = () => {
	if (!ORACLES_ENABLED) {
		throw error(404, 'Not Found');
	}
	return {};
};
