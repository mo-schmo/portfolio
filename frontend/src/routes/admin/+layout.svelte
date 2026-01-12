<script lang="ts">
    import { auth, checkAuth } from "$lib/stores/auth";
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    onMount(() => {
        checkAuth();
    });

    $: if (
        !$auth.loading &&
        !$auth.isAuthenticated &&
        $page.url.pathname !== "/admin/login"
    ) {
        goto("/admin/login");
    }
</script>

{#if $auth.loading}
    <div class="min-h-screen bg-parchment flex items-center justify-center">
        <div class="animate-pulse flex flex-col items-center">
            <div
                class="text-brass font-display font-bold tracking-[0.4em] uppercase text-xs mb-4"
            >
                Verifying Status
            </div>
            <div class="w-12 h-px bg-mahogany opacity-20"></div>
        </div>
    </div>
{:else if $auth.isAuthenticated || $page.url.pathname === "/admin/login"}
    <slot />
{:else}
    <div class="min-h-screen bg-parchment flex items-center justify-center">
        <p class="font-serif italic text-mahogany/40 text-sm">
            Redirecting to primary access terminal...
        </p>
    </div>
{/if}
