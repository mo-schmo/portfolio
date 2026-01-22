<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { BASE_URL } from "$lib/api";

    export let data;
    $: isEdit = data.project !== null;
    let project = (
        data.project
            ? { ...data.project }
            : {
                  title: "",
                  slug: "",
                  description: "",
                  content: "",
                  imageUrl: "",
                  githubUrl: "",
                  liveUrl: "",
                  technologies: "[]",
                  featured: false,
                  isDraft: true,
              }
    ) as any;

    let techInput = "";
    $: {
        if (
            project.technologies &&
            typeof project.technologies === "string" &&
            !techInput
        ) {
            try {
                const parsed = JSON.parse(project.technologies);
                techInput = Array.isArray(parsed) ? parsed.join(", ") : "";
            } catch (e) {
                techInput = "";
            }
        }
    }

    let loading = false;
    let error = "";

    async function handleSubmit() {
        loading = true;
        error = "";

        // Parse technologies
        const techArray = techInput
            .split(",")
            .map((t) => t.trim())
            .filter((t) => t !== "");
        const payload = {
            ...project,
            technologies: techArray,
        };

        const url = isEdit
            ? `${BASE_URL}/projects/${project.id}`
            : `${BASE_URL}/projects`;

        const method = isEdit ? "PUT" : "POST";

        try {
            const res = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
                credentials: "include",
            });

            if (res.ok) {
                goto("/admin/projects");
            } else {
                const msg = await res.text();
                error = msg || "Failed to save the record.";
            }
        } catch (e) {
            error = "System error during filing operation.";
        } finally {
            loading = false;
        }
    }

    function generateSlug() {
        if (!isEdit && project.title) {
            project.slug = project.title
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, "-")
                .replace(/(^-|-$)/g, "");
        }
    }
</script>

<div class="min-h-screen bg-parchment py-16 px-6 font-serif">
    <div class="container mx-auto max-w-4xl">
        <nav class="flex items-center gap-4 mb-12 text-mahogany/40">
            <a
                href="/admin"
                class="text-[10px] font-display font-bold uppercase tracking-widest hover:text-mahogany transition-colors"
                >Dashboard</a
            >
            <span class="text-[10px]">/</span>
            <a
                href="/admin/projects"
                class="text-[10px] font-display font-bold uppercase tracking-widest hover:text-mahogany transition-colors"
                >Projects</a
            >
            <span class="text-[10px]">/</span>
            <span
                class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany"
                >{isEdit ? "Edit Record" : "New Record"}</span
            >
        </nav>

        <header class="mb-16">
            <h1
                class="text-3xl md:text-5xl font-display font-black text-mahogany uppercase tracking-tighter"
            >
                {isEdit ? "Modify Record" : "File New Record"}
            </h1>
            <p class="font-serif italic text-ink/60 mt-2">
                {isEdit
                    ? `Updating Case File #${project.id}`
                    : "Initiating new technical documentation."}
            </p>
        </header>

        <form on:submit|preventDefault={handleSubmit} class="space-y-12">
            <div
                class="legal-folio p-6 md:p-10 bg-white space-y-8 relative overflow-hidden"
            >
                <div class="absolute top-0 left-0 w-1 h-full bg-brass"></div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
                    <!-- Title -->
                    <div class="space-y-3">
                        <label
                            for="title"
                            class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                            >Subject Title</label
                        >
                        <input
                            type="text"
                            id="title"
                            bind:value={project.title}
                            on:blur={generateSlug}
                            required
                            class="w-full bg-parchment border border-paper-line p-4 text-sm focus:outline-none focus:border-brass"
                        />
                    </div>

                    <!-- Slug -->
                    <div class="space-y-3">
                        <label
                            for="slug"
                            class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                            >Identifier (Slug)</label
                        >
                        <input
                            type="text"
                            id="slug"
                            bind:value={project.slug}
                            required
                            class="w-full bg-parchment border border-paper-line p-4 text-sm font-mono focus:outline-none focus:border-brass"
                        />
                    </div>
                </div>

                <!-- Description -->
                <div class="space-y-3">
                    <label
                        for="description"
                        class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                        >Executive Summary</label
                    >
                    <textarea
                        id="description"
                        bind:value={project.description}
                        required
                        rows="3"
                        class="w-full bg-parchment border border-paper-line p-4 text-sm italic focus:outline-none focus:border-brass"
                    ></textarea>
                </div>

                <!-- Content (Markdown) -->
                <div class="space-y-3">
                    <label
                        for="content"
                        class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                        >Detailed Case Narrative (Markdown)</label
                    >
                    <textarea
                        id="content"
                        bind:value={project.content}
                        required
                        rows="15"
                        class="w-full bg-parchment border border-paper-line p-4 md:p-6 text-base leading-relaxed font-serif focus:outline-none focus:border-brass"
                        placeholder="# Project Overview\n\n![Exhibit 1](url)\n\nDetailed breakdown..."
                    ></textarea>
                </div>

                <!-- Tech stack -->
                <div class="space-y-3">
                    <label
                        for="technologies"
                        class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                        >Technical Stack (Comma separated)</label
                    >
                    <input
                        type="text"
                        id="technologies"
                        bind:value={techInput}
                        class="w-full bg-parchment border border-paper-line p-4 text-sm font-display uppercase tracking-widest focus:outline-none focus:border-brass"
                        placeholder="Go, Svelte, PostgreSQL"
                    />
                </div>
            </div>

            <!-- Secondary Folio (Metadata) -->
            <div class="legal-folio p-6 md:p-10 bg-white/50 space-y-8">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
                    <div class="space-y-3">
                        <label
                            for="imageUrl"
                            class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                            >Visual Exhibit URL (Cover)</label
                        >
                        <input
                            type="text"
                            id="imageUrl"
                            bind:value={project.imageUrl}
                            class="w-full bg-white border border-paper-line p-4 text-xs"
                        />
                    </div>
                    <div class="space-y-3">
                        <label
                            for="githubUrl"
                            class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                            >Source Repository URL</label
                        >
                        <input
                            type="text"
                            id="githubUrl"
                            bind:value={project.githubUrl}
                            class="w-full bg-white border border-paper-line p-4 text-xs"
                        />
                    </div>
                    <div class="space-y-3">
                        <label
                            for="liveUrl"
                            class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                            >Live Implementation URL</label
                        >
                        <input
                            type="text"
                            id="liveUrl"
                            bind:value={project.liveUrl}
                            class="w-full bg-white border border-paper-line p-4 text-xs"
                        />
                    </div>
                    <div class="flex items-center gap-4">
                        <input
                            type="checkbox"
                            id="featured"
                            bind:checked={project.featured}
                            class="w-5 h-5 accent-mahogany"
                        />
                        <label
                            for="featured"
                            class="text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                            >Designate as Featured Exhibit</label
                        >
                    </div>
                    <div class="flex items-center gap-4">
                        <input
                            type="checkbox"
                            id="isDraft"
                            bind:checked={project.isDraft}
                            class="w-5 h-5 accent-mahogany"
                        />
                        <label
                            for="isDraft"
                            class="text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                            >Save as Draft (Private)</label
                        >
                    </div>
                </div>
            </div>

            {#if error}
                <div
                    class="p-6 bg-mahogany/5 border border-mahogany/10 text-mahogany text-sm italic text-center"
                >
                    {error}
                </div>
            {/if}

            <div
                class="flex flex-col-reverse md:flex-row justify-end gap-4 md:gap-6"
            >
                <button
                    type="button"
                    on:click={() => goto("/admin/projects")}
                    class="px-10 py-4 text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/40 hover:text-mahogany transition-colors"
                >
                    Discard Changes
                </button>
                <button
                    type="submit"
                    disabled={loading}
                    class="bg-mahogany text-parchment px-12 py-4 font-display font-bold uppercase tracking-[0.3em] text-xs hover:bg-mahogany-light transition-all shadow-[6px_6px_0px_rgba(45,27,27,0.1)] active:transform active:translate-y-1 disabled:opacity-50"
                >
                    {loading
                        ? "Filing..."
                        : isEdit
                          ? "Update Archive"
                          : "Certify Record"}
                </button>
            </div>
        </form>
    </div>
</div>
