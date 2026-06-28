import { PUBLIC_AGENTS_URL } from '$env/static/public';

export const AGENTS_BASE_URL = PUBLIC_AGENTS_URL || 'http://localhost:8001';

const SESSION_KEY = 'oracle.session.id';

export function getSessionId(): string {
	if (typeof localStorage === 'undefined') {
		return cryptoRandom();
	}
	let id = localStorage.getItem(SESSION_KEY);
	if (!id) {
		id = cryptoRandom();
		localStorage.setItem(SESSION_KEY, id);
	}
	return id;
}

function cryptoRandom(): string {
	if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
		return crypto.randomUUID();
	}
	return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export type StreamEvent =
	| { type: 'token'; text: string }
	| { type: 'tool_call'; tool: string; args: Record<string, unknown>; id?: string }
	| { type: 'tool_result'; tool: string; ok: boolean; summary: string }
	| { type: 'state'; node: string; status: 'running' | 'done' }
	| { type: 'citation'; id: string; title: string; href?: string; snippet?: string }
	| { type: 'message'; role: 'assistant' | 'user'; content: string }
	| { type: 'report'; report: unknown }
	| { type: 'error'; message: string }
	| { type: 'done' };

export interface StreamOptions {
	path: string;
	body: Record<string, unknown>;
	signal?: AbortSignal;
}

/**
 * Stream Server-Sent Events from the agents service using a POST body.
 *
 * We use ``fetch`` rather than the native ``EventSource`` because EventSource
 * cannot send a POST body. The line protocol is the same SSE wire format:
 * lines prefixed with ``data:`` containing JSON, separated by blank lines.
 */
export async function* streamSSE(opts: StreamOptions): AsyncGenerator<StreamEvent> {
	const response = await fetch(`${AGENTS_BASE_URL}${opts.path}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Accept: 'text/event-stream'
		},
		body: JSON.stringify(opts.body),
		signal: opts.signal
	});

	if (!response.ok || !response.body) {
		const text = await response.text().catch(() => '');
		yield {
			type: 'error',
			message: text || `Request failed with status ${response.status}`
		};
		return;
	}

	const reader = response.body.getReader();
	const decoder = new TextDecoder('utf-8');
	let buffer = '';

	try {
		while (true) {
			const { value, done } = await reader.read();
			if (done) break;
			buffer += decoder.decode(value, { stream: true });

			let sep = buffer.indexOf('\n\n');
			while (sep !== -1) {
				const raw = buffer.slice(0, sep);
				buffer = buffer.slice(sep + 2);
				const event = parseSSEEvent(raw);
				if (event) yield event;
				sep = buffer.indexOf('\n\n');
			}
		}
	} finally {
		reader.releaseLock();
	}
}

function parseSSEEvent(raw: string): StreamEvent | null {
	const lines = raw.split('\n');
	const dataLines: string[] = [];
	for (const line of lines) {
		if (line.startsWith('data:')) {
			dataLines.push(line.slice(5).trimStart());
		}
	}
	if (dataLines.length === 0) return null;
	const payload = dataLines.join('\n');
	try {
		return JSON.parse(payload) as StreamEvent;
	} catch {
		return null;
	}
}

export interface ClauseExplanation {
	clause_summary: string;
	plain_english: string;
	obligations: { party: string; obligation: string }[];
	risks: { severity: 'low' | 'medium' | 'high'; description: string }[];
	suggested_redlines: { original: string; suggestion: string; rationale: string }[];
}

export async function explainClause(clause: string, signal?: AbortSignal): Promise<ClauseExplanation> {
	const response = await fetch(`${AGENTS_BASE_URL}/agents/clause/explain`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ clause }),
		signal
	});
	if (!response.ok) {
		throw new Error(`Clause explainer failed: ${response.status}`);
	}
	return response.json();
}
