<script lang="ts">
    import {
        latestActivity,
        wsStatus,
        activeWitnesses,
    } from "$lib/stores/webSocket";

    let lastMessage = "Awaiting transmission...";

    // Reactively update the ticket text using auto-subscription
    $: if ($latestActivity) {
        const act = $latestActivity;
        if (act.type === "blog_created")
            lastMessage = `NEW BRIEFING FILED: ${act.payload.title}`;
        else if (act.type === "blog_updated")
            lastMessage = `BRIEFING AMENDED: ${act.payload.title}`;
        else if (act.type === "project_created")
            lastMessage = `NEW EVIDENCE SUBMITTED: ${act.payload.title}`;
        else if (act.type === "project_updated")
            lastMessage = `EVIDENCE UPDATED: ${act.payload.title}`;
        else if (act.type.includes("deleted"))
            lastMessage = `RECORD EXPUNGED FROM ARCHIVES`;
    }
</script>

<div></div>
<div
    class="fixed bottom-0 left-0 w-full z-40 bg-mahogany-dark border-t border-brass/30 text-parchment-dark shadow-[0_-4px_20px_rgba(0,0,0,0.3)] font-mono text-xs"
>
    <div class="flex items-stretch h-8">
        <!-- Status Indicator -->
        <div
            class="px-4 flex items-center gap-3 bg-black/20 border-r border-white/5"
        >
            <div class="relative flex h-2 w-2">
                {#if $wsStatus === "connected"}
                    <span
                        class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"
                    ></span>
                    <span
                        class="relative inline-flex rounded-full h-2 w-2 bg-green-500"
                    ></span>
                {:else}
                    <span
                        class="relative inline-flex rounded-full h-2 w-2 bg-red-500"
                    ></span>
                {/if}
            </div>
            <span
                class="font-display font-bold tracking-[0.2em] uppercase text-[9px] opacity-70"
            >
                {$wsStatus === "connected" ? "UPLINK SECURE" : "OFFLINE"}
            </span>
        </div>

        <!-- The Ticker -->
        <div class="flex-grow flex items-center overflow-hidden relative mx-4">
            <div
                class="whitespace-nowrap animate-ticker opacity-80 font-serif italic"
            >
                /// OFFICIAL COURT RECORD /// {lastMessage} /// SYSTEM OPERATIONAL
                /// ALL RECORDS PRESERVED ///
            </div>
        </div>

        <!-- Witness Count -->
        <div
            class="px-6 flex items-center gap-2 bg-brass/10 border-l border-white/5 whitespace-nowrap"
        >
            <span
                class="font-display font-bold tracking-[0.2em] uppercase text-[9px] text-brass-light"
            >
                WITNESSES PRESENT:
            </span>
            <span class="font-mono font-bold text-parchment">
                {$activeWitnesses.toString().padStart(3, "0")}
            </span>
        </div>
    </div>
</div>

<style>
    @keyframes ticker {
        0% {
            transform: translateX(100%);
        }
        100% {
            transform: translateX(-100%);
        }
    }
    .animate-ticker {
        animation: ticker 20s linear infinite;
    }
</style>
