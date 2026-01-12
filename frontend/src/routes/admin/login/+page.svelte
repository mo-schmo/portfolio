<script lang="ts">
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    let username = "";
    let password = "";
    let error = "";
    let loading = false;

    async function handleLogin() {
        loading = true;
        error = "";

        try {
            const res = await fetch("http://localhost:8080/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
                credentials: "include",
            });

            if (res.ok) {
                auth.set({
                    isAuthenticated: true,
                    isAdmin: true,
                    loading: false,
                });
                goto("/admin");
            } else {
                const data = await res.text();
                error =
                    data || "Invalid credentials. Please verify your identity.";
            }
        } catch (e) {
            error = "System error. Connection to archive failed.";
        } finally {
            loading = false;
        }
    }
</script>

<div class="min-h-screen bg-parchment flex items-center justify-center p-6">
    <div class="max-w-md w-full">
        <div class="text-center mb-12">
            <div
                class="text-brass font-display font-bold mb-4 tracking-[0.4em] uppercase text-xs"
            >
                Secure Archive Access
            </div>
            <h1
                class="text-4xl font-display font-black text-mahogany uppercase tracking-tighter mb-2"
            >
                Administration
            </h1>
            <div class="w-16 h-1 bg-mahogany mx-auto opacity-20"></div>
        </div>

        <div
            class="legal-folio p-6 md:p-10 bg-white shadow-2xl relative overflow-hidden"
        >
            <div class="absolute top-0 left-0 w-1 h-full bg-mahogany"></div>

            <form on:submit|preventDefault={handleLogin} class="space-y-8">
                <div>
                    <label
                        for="username"
                        class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60 mb-3"
                    >
                        Credential ID
                    </label>
                    <input
                        type="text"
                        id="username"
                        bind:value={username}
                        required
                        class="w-full bg-parchment border border-paper-line p-4 font-serif text-ink focus:outline-none focus:border-brass transition-colors"
                        placeholder="Username"
                    />
                </div>

                <div>
                    <label
                        for="password"
                        class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60 mb-3"
                    >
                        Security Passcode
                    </label>
                    <input
                        type="password"
                        id="password"
                        bind:value={password}
                        required
                        class="w-full bg-parchment border border-paper-line p-4 font-serif text-ink focus:outline-none focus:border-brass transition-colors"
                        placeholder="••••••••"
                    />
                </div>

                {#if error}
                    <div
                        class="p-4 bg-mahogany/5 border border-mahogany/10 text-mahogany text-xs font-serif italic text-center"
                    >
                        {error}
                    </div>
                {/if}

                <button
                    type="submit"
                    disabled={loading}
                    class="w-full bg-mahogany text-parchment py-4 font-display font-bold uppercase tracking-[0.3em] text-xs hover:bg-mahogany-light transition-all shadow-[4px_4px_0px_rgba(45,27,27,0.1)] active:transform active:translate-y-1 disabled:opacity-50"
                >
                    {loading ? "Verifying..." : "Authorize Entry"}
                </button>
            </form>
        </div>

        <div class="mt-12 text-center opacity-30">
            <div
                class="text-[10px] font-display font-bold uppercase tracking-[0.5em]"
            >
                Department of Technical Records
            </div>
        </div>
    </div>
</div>
