/**
 * Public feature flags.
 *
 * Flags are sourced from ``$env/dynamic/public`` (Vite ``PUBLIC_*`` env
 * vars). We use the dynamic module rather than ``$env/static/public`` so
 * referencing a flag that isn't yet declared in a ``.env`` file doesn't
 * break type-check - the index signature returns ``string | undefined`` for
 * any unknown ``PUBLIC_*`` key. To disable a feature for a given deployment,
 * set the env var to ``"false"`` (or ``"0"``) at build time. Empty / unset /
 * any other value is treated as enabled, so the default is "on" in dev.
 */

import { env } from '$env/dynamic/public';

function parseFlag(raw: string | undefined, fallback: boolean): boolean {
	if (raw === undefined || raw === '') return fallback;
	const normalized = raw.trim().toLowerCase();
	if (['false', '0', 'no', 'off'].includes(normalized)) return false;
	if (['true', '1', 'yes', 'on'].includes(normalized)) return true;
	return fallback;
}

/**
 * Whether the Oracles (agentic bots) section is exposed in the frontend.
 *
 * When ``false``:
 * - The Navbar omits the "Oracles" entry.
 * - The home page omits the hero "Consult the Oracles" CTA and the Counsel
 *   Chamber section.
 * - The project detail page omits the "Ask the Tour Guide" button.
 * - The ``/oracles`` routes return 404.
 *
 * Defaults to enabled so local dev and existing deploys are unaffected.
 */
export const ORACLES_ENABLED = parseFlag(env.PUBLIC_ORACLES_ENABLED, true);
