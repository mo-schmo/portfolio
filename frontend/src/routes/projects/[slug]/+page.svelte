<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    export let data;
    $: project = data.project;

    function parseTechnologies(techStr: string): string[] {
        try {
            const parsed = JSON.parse(techStr);
            if (typeof parsed === "string") {
                return JSON.parse(parsed);
            }
            return parsed;
        } catch (e) {
            return [];
        }
    }

    function renderMarkdown(text: string): string {
        let html = text;

        // Images: ![alt](url) -> wrap in folio style container
        html = html.replace(
            /!\[(.*?)\]\((.*?)\)/gim,
            `
			<figure class="my-24 flex flex-col items-center">
				<div class="legal-folio p-1 bg-white border-2 border-paper-line shadow-2xl transition-all duration-700 hover:-rotate-1 group max-w-3xl">
					<div class="p-4 bg-white border border-paper-line/30">
						<div class="relative overflow-hidden">
							<img src="$2" alt="$1" class="max-w-full h-auto grayscale-[0.2] group-hover:grayscale-0 transition-all duration-1000" />
							<div class="absolute inset-0 pointer-events-none ring-1 ring-inset ring-black/5"></div>
						</div>
					</div>
				</div>
				<figcaption class="mt-8 font-display font-black text-[10px] uppercase tracking-[0.4em] text-mahogany/30 border-b border-mahogany/10 pb-2">
					Exhibit Case // $1
				</figcaption>
			</figure>
			`,
        );

        // Headers
        html = html.replace(
            /^### (.*$)/gim,
            '<h3 class="text-xl font-display font-black text-mahogany mb-6 mt-16 uppercase tracking-widest border-l-2 border-brass pl-4">$1</h3>',
        );
        html = html.replace(
            /^## (.*$)/gim,
            '<div class="folio-divider"></div><h2 class="text-3xl font-display font-black text-mahogany mb-10 mt-20 uppercase tracking-tight">$1</h2>',
        );
        html = html.replace(
            /^# (.*$)/gim,
            '<h1 class="text-5xl font-display font-black text-mahogany mb-12 mt-24 uppercase tracking-tighter border-l-4 border-mahogany pl-8">$1</h1>',
        );

        // Bold and italic
        html = html.replace(
            /\*\*(.*?)\*\*/gim,
            '<strong class="text-mahogany font-black border-b border-mahogany/10">$1</strong>',
        );
        html = html.replace(
            /\*(.*?)\*/gim,
            '<em class="italic text-mahogany/80 underline decoration-brass/30 underline-offset-4">$1</em>',
        );

        // Paragraphs
        const paragraphs = html.split(/\n\n+/);
        html = paragraphs
            .map((p) => p.trim())
            .filter((p) => p.length > 0)
            .map((p) => {
                if (
                    p.startsWith("<h") ||
                    p.startsWith("<figure") ||
                    p.startsWith("<div")
                ) {
                    return p;
                }
                return `<p class="mb-10 text-ink/90 leading-[1.9] text-xl font-serif text-justify tracking-tight">${p.replace(/\n/gim, "<br/>")}</p>`;
            })
            .join("");

        return html;
    }
</script>

<svelte:head>
    <title>{project?.title || "Case Study"} - Mohammed Hamza</title>
</svelte:head>

<div
    class="bg-parchment min-h-screen selection:bg-mahogany/10 selection:text-mahogany"
>
    {#if project}
        <div class="container mx-auto px-6 py-28 max-w-4xl relative">
            <!-- Watermark Stamp -->
            <div
                class="absolute top-20 right-10 opacity-60 pointer-events-none hidden lg:block"
            >
                <div class="legal-stamp">
                    Authenticated Result<br />Record ID: {project.id}
                </div>
            </div>

            <!-- Header Navigation -->
            <nav
                class="flex justify-between items-center mb-32 border-b border-paper-line pb-8"
            >
                <button
                    on:click={() => goto("/projects")}
                    class="group flex items-center text-mahogany/50 hover:text-mahogany transition-colors font-display font-bold uppercase tracking-[0.2em] text-[10px]"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-3 w-3 mr-4 group-hover:-translate-x-1 transition-transform"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M10 19l-7-7m0 0l7-7m-7 7h18"
                        />
                    </svg>
                    Archived Folios
                </button>

                <div class="flex gap-10">
                    {#if project.githubUrl}
                        <a
                            href={project.githubUrl}
                            target="_blank"
                            class="text-mahogany/40 hover:text-brass transition-colors text-[10px] font-display font-bold uppercase tracking-[0.2em]"
                            >Source Code</a
                        >
                    {/if}
                    {#if project.liveUrl}
                        <a
                            href={project.liveUrl}
                            target="_blank"
                            class="text-mahogany/40 hover:text-brass transition-colors text-[10px] font-display font-bold uppercase tracking-[0.2em]"
                            >Live Registry</a
                        >
                    {/if}
                </div>
            </nav>

            <article class="relative">
                <header class="mb-32">
                    <div class="flex items-start justify-between mb-16">
                        <div class="max-w-2xl">
                            <div
                                class="text-brass font-display font-bold mb-6 tracking-[0.5em] uppercase text-[10px] flex items-center"
                            >
                                <span class="w-8 h-px bg-brass mr-4"></span>
                                Technical Record // {new Date(
                                    project.createdAt,
                                ).getFullYear()}
                            </div>

                            <h1
                                class="text-6xl md:text-8xl font-display font-black mb-10 text-mahogany leading-[0.9] uppercase tracking-tighter"
                            >
                                {project.title}
                            </h1>
                        </div>

                        {#if project.id}
                            <div class="hidden sm:block">
                                <div
                                    class="w-20 h-20 border-4 border-double border-mahogany/20 rounded-full flex items-center justify-center text-mahogany/20 font-display font-black text-xl rotate-12"
                                >
                                    #{project.id}
                                </div>
                            </div>
                        {/if}
                    </div>

                    <div
                        class="flex flex-wrap gap-3 p-8 bg-white/50 border border-paper-line rounded-sm mb-20 shadow-sm relative overflow-hidden group"
                    >
                        <div
                            class="absolute top-0 left-0 w-1 h-full bg-brass"
                        ></div>
                        {#each parseTechnologies(project.technologies) as tech}
                            <span
                                class="px-5 py-2 bg-mahogany text-parchment text-[9px] font-display font-bold uppercase tracking-[0.2em] shadow-sm hover:translate-y-[-1px] transition-transform cursor-default"
                            >
                                {tech}
                            </span>
                        {/each}
                    </div>

                    <div class="w-full h-px bg-mahogany/10"></div>
                </header>

                <div class="case-content">
                    {@html renderMarkdown(project.content)}
                </div>

                <footer
                    class="mt-40 pt-24 border-t-2 border-paper-line text-center group"
                >
                    <div class="inline-block relative">
                        <div
                            class="font-display font-bold text-mahogany/60 text-xs mb-6 uppercase tracking-[0.4em] transition-colors group-hover:text-brass"
                        >
                            Final Closing Statement
                        </div>
                        <div
                            class="text-mahogany/30 font-serif italic text-[11px] tracking-wide"
                        >
                            This record was certified on {new Date(
                                project.updatedAt,
                            ).toLocaleDateString("en-US", {
                                year: "numeric",
                                month: "long",
                                day: "numeric",
                            })}
                        </div>
                        <div
                            class="mt-12 opacity-10 grayscale group-hover:grayscale-0 group-hover:opacity-40 transition-all duration-700"
                        >
                            <div
                                class="text-4xl font-display font-black text-mahogany opacity-30 select-none"
                            >
                                M. HAMZA
                            </div>
                            <div
                                class="text-[10px] font-display font-bold tracking-[0.5em] uppercase mt-2"
                            >
                                Counsel & Engineer
                            </div>
                        </div>
                    </div>
                </footer>
            </article>
        </div>
    {:else}
        <div class="container mx-auto px-4 py-40 text-center">
            <div
                class="inline-block border-2 border-mahogany/10 p-12 animate-pulse"
            >
                <p
                    class="text-mahogany/30 font-display font-bold uppercase tracking-[0.3em] text-sm italic"
                >
                    Accessing Archives...
                </p>
            </div>
        </div>
    {/if}
</div>

<style>
    :global(.case-content img) {
        @apply rounded-none shadow-2xl;
    }

    :global(.case-content p:first-of-type::first-letter) {
        font-family: "Playfair Display", serif;
        @apply text-6xl md:text-8xl text-mahogany font-black mr-1;
        line-height: 0;
        vertical-align: middle;
    }

    :global(.folio-divider::after) {
        content: "§";
        @apply absolute left-1/2 -translate-x-1/2 -translate-y-1/2 bg-parchment px-4 text-mahogany/20 font-serif text-lg italic;
    }

    .folio-divider {
        @apply relative;
    }
</style>
