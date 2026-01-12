<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    async function handleLogout() {
        const res = await fetch("http://localhost:8080/api/auth/logout", {
            method: "POST",
            credentials: "include",
        });
        if (res.ok) {
            window.location.href = "/";
        }
    }
</script>

<div class="min-h-screen bg-parchment py-28 px-6">
    <div class="container mx-auto max-w-5xl">
        <header
            class="flex flex-col md:flex-row justify-between items-start md:items-end gap-8 mb-16 md:mb-20"
        >
            <div>
                <div
                    class="text-brass font-display font-bold tracking-[0.4em] uppercase text-xs mb-4"
                >
                    Central Archives Control
                </div>
                <h1
                    class="text-4xl md:text-6xl font-display font-black text-mahogany uppercase tracking-tighter"
                >
                    Dashboard
                </h1>
            </div>

            <button
                on:click={handleLogout}
                class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/40 hover:text-mahogany transition-colors border-b border-mahogany/10 pb-1"
            >
                Terminate Session
            </button>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
            <!-- Projects Management Card -->
            <a
                href="/admin/projects"
                class="legal-folio p-8 md:p-12 group hover:translate-y-[-4px] transition-all duration-500"
            >
                <div class="flex justify-between items-start mb-10">
                    <div
                        class="w-12 h-12 bg-mahogany/5 flex items-center justify-center rounded-sm"
                    >
                        <span class="text-2xl">📁</span>
                    </div>
                    <div
                        class="text-[10px] font-display font-bold text-brass uppercase tracking-widest"
                    >
                        Exhibit Folios
                    </div>
                </div>

                <h2
                    class="text-3xl font-display font-black text-mahogany uppercase tracking-tight mb-4"
                >
                    Projects
                </h2>
                <p class="font-serif italic text-ink/60 mb-10 leading-relaxed">
                    Review, modify, or archive technical project records and
                    detailed case studies.
                </p>

                <div
                    class="flex items-center text-xs font-display font-bold uppercase tracking-[0.2em] text-mahogany"
                >
                    Open Registry
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4 ml-3 group-hover:translate-x-2 transition-transform"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M17 8l4 4m0 0l-4 4m4-4H3"
                        />
                    </svg>
                </div>
            </a>

            <!-- Blogs Management Card -->
            <a
                href="/admin/blogs"
                class="legal-folio p-8 md:p-12 group hover:translate-y-[-4px] transition-all duration-500"
            >
                <div class="flex justify-between items-start mb-10">
                    <div
                        class="w-12 h-12 bg-mahogany/5 flex items-center justify-center rounded-sm"
                    >
                        <span class="text-2xl">🖋️</span>
                    </div>
                    <div
                        class="text-[10px] font-display font-bold text-brass uppercase tracking-widest"
                    >
                        Briefings & Opinions
                    </div>
                </div>

                <h2
                    class="text-3xl font-display font-black text-mahogany uppercase tracking-tight mb-4"
                >
                    Blog Posts
                </h2>
                <p class="font-serif italic text-ink/60 mb-10 leading-relaxed">
                    Draft and publish new technical briefs or update existing
                    archives in the public ledger.
                </p>

                <div
                    class="flex items-center text-xs font-display font-bold uppercase tracking-[0.2em] text-mahogany"
                >
                    Open Registry
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4 ml-3 group-hover:translate-x-2 transition-transform"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M17 8l4 4m0 0l-4 4m4-4H3"
                        />
                    </svg>
                </div>
            </a>
        </div>

        <div
            class="mt-16 md:mt-20 p-6 md:p-8 bg-white/50 border border-paper-line rounded-sm flex flex-col md:flex-row items-center justify-between gap-6"
        >
            <div class="flex flex-col md:flex-row items-center gap-4 md:gap-10">
                <div
                    class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/40"
                >
                    System Status: <span class="text-green-800 opacity-90"
                        >Operational</span
                    >
                </div>
                <div
                    class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/40"
                >
                    Security Level: <span class="text-mahogany">Restricted</span
                    >
                </div>
            </div>

            <a
                href="/"
                class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/60 hover:text-mahogany transition-colors"
            >
                View Public Front
            </a>
        </div>
    </div>
</div>
