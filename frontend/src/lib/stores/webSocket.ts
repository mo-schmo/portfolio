import { browser } from "$app/environment";
import { writable } from "svelte/store";
import { PUBLIC_WS_URL } from '$env/static/public';


export const wsStatus = writable<'disconnected' | 'connecting' | 'connected'>('disconnected');
export const activeWitnesses = writable<number>(0);
export const latestActivity = writable<{ type: string; payload: any } | null>(null);

let socket: WebSocket | null = null;
let reconnectTimer: any;
let isConnecting = false;

export function initWebSocket() {
    if (!browser) return;
    if (isConnecting) return;
    if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) return

    isConnecting = true;
    wsStatus.set('connecting');

    // Handle different environments
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const host = window.location.hostname === 'localhost' ? 'localhost:8080' : window.location.host;
    const wsUrl = PUBLIC_WS_URL || `${protocol}://${host}/ws`

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        console.log('Archive Uplink Established');
        wsStatus.set('connected');
        isConnecting = false;
        if (reconnectTimer) clearTimeout(reconnectTimer);
    }

    socket.onmessage = (event) => {
        try {
            const msg = JSON.parse(event.data);
            if (msg.type === 'census_update') {
                activeWitnesses.set(msg.payload.count);
            }
            latestActivity.set(msg);
        }
        catch (e) {
            console.error("Failed to parse docket message", e);
        }
    }

    socket.onclose = () => {
        console.log('Archive Uplink Severed');
        wsStatus.set('disconnected');
        isConnecting = false;
        activeWitnesses.set(0);

        // Attempt to reconnect
        reconnectTimer = setTimeout(() => {
            initWebSocket();
        }, 3000);

    }
}