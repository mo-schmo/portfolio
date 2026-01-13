<script lang="ts">
    import { latestActivity } from "$lib/stores/webSocket";
    import { fly } from "svelte/transition";

    interface Notification {
        id: number;
        title: string;
        message: string;
        type: "evidence" | "briefing" | "update";
        timestamp: Date;
    }

    let notifications: Notification[] = [];
    let counter = 0;

    // Reactively handle new activity using auto-subscription
    $: if ($latestActivity) {
        handleActivity($latestActivity);
    }

    function handleActivity(activity: any) {
        let title = "";
        let message = "";
        let type: Notification["type"] = "update";

        switch (activity.type) {
            case "blog_created":
                title = "NEW BRIEFING FILED";
                message = activity.payload.title;
                type = "briefing";
                break;
            case "blog_updated":
                title = "BRIEFING AMENDED";
                message = activity.payload.title;
                type = "update";
                break;
            case "project_created":
                title = "NEW EVIDENCE ADMITTED";
                message = activity.payload.title;
                type = "evidence";
                break;
            case "project_updated":
                title = "RECORD AMENDED";
                message = activity.payload.title;
                type = "update";
                break;
        }

        if (title) {
            addNotification(title, message, type);
        }
    }

    function addNotification(
        title: string,
        message: string,
        type: Notification["type"],
    ) {
        const id = counter++;
        const newNotif: Notification = {
            id,
            title,
            message,
            type,
            timestamp: new Date(),
        };
        notifications = [newNotif, ...notifications];

        //Auto remove after 6 seconds
        setTimeout(() => {
            removeNotification(id);
        }, 6000);
    }

    function removeNotification(id: number) {
        notifications = notifications.filter((n) => n.id !== id);
    }
</script>

<div
    class="fixed top-24 right-4 z-50 flex flex-col gap-4 pointer-events-none w-full max-w-sm"
>
    {#each notifications as notif (notif.id)}
        <div
            transition:fly={{ x: 200, duration: 500 }}
            class="pointer-events-auto bg-parchment border-2 border-mahogany shadow-2xl relative overflow-hidden"
        >
            <!-- Decorative corner tab -->
            <div
                class="absolute top-0 right-0 w-8 h-8 bg-mahogany/10 -translate-y-1/2 translate-x-1/2 rotate-45"
            ></div>

            <div class="p-4 flex gap-4">
                <!-- Icon/Stamp -->
                <div class="flex-shrink-0 mt-1">
                    <div
                        class="w-10 h-10 border-2 border-brass rounded-full flex items-center justify-center text-brass font-display font-black text-xl rotate-[-12deg] opacity-80 mix-blend-multiply"
                    >
                        {#if notif.type === "evidence"}EX. A
                        {:else if notif.type === "briefing"}DOC
                        {:else}REV
                        {/if}
                    </div>
                </div>

                <div class="flex-grow">
                    <div class="flex justify-between items-start mb-1">
                        <h4
                            class="text-[10px] font-display font-black tracking-[0.2em] text-mahogany uppercase"
                        >
                            {notif.title}
                        </h4>
                        <button
                            on:click={() => removeNotification(notif.id)}
                            class="text-mahogany/40 hover:text-mahogany transition-colors"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="h-4 w-4"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            </svg>
                        </button>
                    </div>

                    <p
                        class="font-display font-bold text-mahogany text-lg leading-none mb-2 uppercase tracking-tight"
                    >
                        {notif.message}
                    </p>

                    <div
                        class="text-[9px] font-mono text-mahogany/50 uppercase"
                    >
                        Timestamp: {notif.timestamp.toLocaleTimeString()} // Ledger
                        ID: #{notif.id + 2042}
                    </div>
                </div>
            </div>

            <!-- Bottom status bar -->
            <div class="h-1 w-full bg-mahogany/5">
                <div
                    class="h-full bg-brass/50 origin-left"
                    style="animation: shrink 6s linear forwards;"
                ></div>
            </div>
        </div>
    {/each}
</div>

<style>
    @keyframes shrink {
        from {
            transform: scaleX(1);
        }
        to {
            transform: scaleX(0);
        }
    }
</style>
