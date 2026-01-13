<script lang="ts">
    import { onMount } from "svelte";
    import { fetchAllProjects, BASE_URL } from "$lib/api";
    import type { Project } from "$lib/api";

    let projects: Project[] = [];
    let loading = true;
    let error = "";

    onMount(async () => {
        try {
            projects = (await fetchAllProjects()) || [];
        } catch (e) {
            error = "Failed to retrieve project archives.";
        } finally {
            loading = false;
        }
    });

    async function handleDelete(id: number, title: string) {
        if (
            !confirm(
                `Are you certain you wish to purge the record for "${title}"? This action is irreversible.`,
            )
        ) {
            return;
        }

        try {
            const res = await fetch(`${BASE_URL}/projects/${id}`, {
                method: "DELETE",
                credentials: "include",
            });

            if (res.ok) {
                projects = projects.filter((p) => p.id !== id);
            } else {
                alert(
                    "Failed to purge record. Authorization may have expired.",
                );
            }
        } catch (e) {
            alert("System error during purge operation.");
        }
    }
</script>

<div class="min-h-screen bg-parchment py-16 px-6">
    <div class="container mx-auto max-w-6xl">
        <nav class="flex items-center gap-4 mb-12 text-mahogany/40">
            <a
                href="/admin"
                class="text-[10px] font-display font-bold uppercase tracking-widest hover:text-mahogany transition-colors"
                >Dashboard</a
            >
            <span class="text-[10px]">/</span>
            <span
                class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany"
                >Projects</span
            >
        </nav>

        <header
            class="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 mb-16"
        >
            <div>
                <h1
                    class="text-4xl md:text-5xl font-display font-black text-mahogany uppercase tracking-tighter"
                >
                    Project Registry
                </h1>
                <p class="font-serif italic text-ink/60 mt-2">
                    Manage technical case records and folio exhibits.
                </p>
            </div>

            <a
                href="/admin/projects/new"
                class="bg-mahogany text-parchment px-8 py-3 font-display font-bold uppercase tracking-widest text-xs hover:bg-mahogany-light transition-all shadow-[4px_4px_0px_rgba(45,27,27,0.1)] active:transform active:translate-y-1"
            >
                File New Record
            </a>
        </header>

        {#if loading}
            <div class="py-20 text-center">
                <div
                    class="animate-pulse font-display font-bold uppercase tracking-[0.3em] text-mahogany/30 text-xs"
                >
                    Consulting Archives...
                </div>
            </div>
        {:else if error}
            <div
                class="p-10 bg-mahogany/5 border border-mahogany/10 text-center font-serif italic text-mahogany"
            >
                {error}
            </div>
        {:else}
            <div class="legal-folio overflow-x-auto">
                <table class="w-full text-left min-w-[800px] md:min-w-0">
                    <thead
                        class="bg-parchment-dark/50 border-b border-paper-line"
                    >
                        <tr>
                            <th
                                class="px-8 py-4 text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/60"
                                >Record ID</th
                            >
                            <th
                                class="px-8 py-4 text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/60"
                                >Title</th
                            >
                            <th
                                class="px-8 py-4 text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/60"
                                >Slug</th
                            >
                            <th
                                class="px-8 py-4 text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/60"
                                >Status</th
                            >
                            <th
                                class="px-8 py-4 text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/60 text-right"
                                >Actions</th
                            >
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-paper-line/30">
                        {#each projects as project}
                            <tr
                                class="hover:bg-parchment/30 transition-colors group"
                            >
                                <td
                                    class="px-8 py-6 font-display font-bold text-xs text-brass"
                                    >#{project.id}</td
                                >
                                <td class="px-8 py-6">
                                    <div
                                        class="font-display font-bold text-mahogany uppercase tracking-tight"
                                    >
                                        {project.title}
                                    </div>
                                    <div
                                        class="text-[10px] text-mahogany/40 font-serif italic mt-1"
                                    >
                                        {project.description.slice(0, 60)}...
                                    </div>
                                </td>
                                <td
                                    class="px-8 py-6 font-mono text-[10px] text-mahogany/60"
                                    >{project.slug}</td
                                >
                                <td class="px-8 py-6">
                                    {#if project.featured}
                                        <span
                                            class="px-2 py-0.5 border border-brass/30 text-brass text-[9px] font-display font-bold uppercase tracking-widest rounded-sm"
                                            >Featured</span
                                        >
                                    {:else}
                                        <span
                                            class="text-mahogany/20 text-[9px] font-display font-bold uppercase tracking-widest"
                                            >Standard</span
                                        >
                                    {/if}
                                </td>
                                <td class="px-8 py-6 text-right">
                                    <div class="flex justify-end gap-6">
                                        <a
                                            href="/admin/projects/{project.id}"
                                            class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/40 hover:text-mahogany transition-colors"
                                        >
                                            Edit
                                        </a>
                                        <button
                                            on:click={() =>
                                                handleDelete(
                                                    project.id,
                                                    project.title,
                                                )}
                                            class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/20 hover:text-red-800 transition-colors"
                                        >
                                            Purge
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        {/if}
    </div>
</div>
