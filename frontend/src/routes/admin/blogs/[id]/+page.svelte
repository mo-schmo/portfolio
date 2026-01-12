<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    export let data;
    $: isEdit = data.blog !== null;
    let blog = (
        data.blog
            ? { ...data.blog }
            : {
                  title: "",
                  slug: "",
                  excerpt: "",
                  content: "",
                  publishedAt: new Date().toISOString(),
              }
    ) as any;

    let loading = false;
    let error = "";

    async function handleSubmit() {
        loading = true;
        error = "";

        const url = isEdit
            ? `http://localhost:8080/api/blog/${blog.id}`
            : "http://localhost:8080/api/blog";

        const method = isEdit ? "PUT" : "POST";

        try {
            const res = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(blog),
                credentials: "include",
            });

            if (res.ok) {
                goto("/admin/blogs");
            } else {
                const msg = await res.text();
                error = msg || "Failed to save the briefing.";
            }
        } catch (e) {
            error = "System error during filing operation.";
        } finally {
            loading = false;
        }
    }

    function generateSlug() {
        if (!isEdit && blog.title) {
            blog.slug = blog.title
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
                href="/admin/blogs"
                class="text-[10px] font-display font-bold uppercase tracking-widest hover:text-mahogany transition-colors"
                >Blog Posts</a
            >
            <span class="text-[10px]">/</span>
            <span
                class="text-[10px] font-display font-bold uppercase tracking-widest text-mahogany"
                >{isEdit ? "Edit Briefing" : "New Briefing"}</span
            >
        </nav>

        <header class="mb-16">
            <h1
                class="text-3xl md:text-5xl font-display font-black text-mahogany uppercase tracking-tighter"
            >
                {isEdit ? "Modify Briefing" : "Draft New Briefing"}
            </h1>
            <p class="font-serif italic text-ink/60 mt-2">
                {isEdit
                    ? `Updating Technical Briefing #${blog.id}`
                    : "Initiating new technical editorial."}
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
                            >Briefing Title</label
                        >
                        <input
                            type="text"
                            id="title"
                            bind:value={blog.title}
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
                            bind:value={blog.slug}
                            required
                            class="w-full bg-parchment border border-paper-line p-4 text-sm font-mono focus:outline-none focus:border-brass"
                        />
                    </div>
                </div>

                <!-- Excerpt -->
                <div class="space-y-3">
                    <label
                        for="excerpt"
                        class="block text-[10px] font-display font-bold uppercase tracking-[0.2em] text-mahogany/60"
                        >Abstract (Short Summary)</label
                    >
                    <textarea
                        id="excerpt"
                        bind:value={blog.excerpt}
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
                        >Body Content (Markdown)</label
                    >
                    <textarea
                        id="content"
                        bind:value={blog.content}
                        required
                        rows="15"
                        class="w-full bg-parchment border border-paper-line p-4 md:p-6 text-base leading-relaxed font-serif focus:outline-none focus:border-brass"
                    ></textarea>
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
                    on:click={() => goto("/admin/blogs")}
                    class="px-10 py-4 text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/40 hover:text-mahogany transition-colors"
                >
                    Discard Draft
                </button>
                <button
                    type="submit"
                    disabled={loading}
                    class="bg-mahogany text-parchment px-12 py-4 font-display font-bold uppercase tracking-[0.3em] text-xs hover:bg-mahogany-light transition-all shadow-[6px_6px_0px_rgba(45,27,27,0.1)] active:transform active:translate-y-1 disabled:opacity-50"
                >
                    {loading
                        ? "Filing..."
                        : isEdit
                          ? "Update Briefing"
                          : "Certify Briefing"}
                </button>
            </div>
        </form>
    </div>
</div>
