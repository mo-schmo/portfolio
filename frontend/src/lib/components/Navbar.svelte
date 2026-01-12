<script lang="ts">
    import { page } from "$app/stores";
    import { auth, checkAuth } from "$lib/stores/auth";
    import { slide } from "svelte/transition";
    import { onMount } from "svelte";

    onMount(async () => {
        await checkAuth();
    });

    const navItems = [
        { href: "/", label: "Home" },
        { href: "/projects", label: "Projects" },
        { href: "/blog", label: "Blog" },
        { href: "/contact", label: "Contact" },
    ];

    $: allNavItems = $auth.isAuthenticated
        ? [...navItems, { href: "/admin", label: "Admin" }]
        : navItems;

    let isMobileMenuOpen = false;

    function toggleMenu() {
        isMobileMenuOpen = !isMobileMenuOpen;
    }

    // Close menu when a link is clicked
    function closeMenu() {
        isMobileMenuOpen = false;
    }
</script>

<nav
    class="fixed top-0 w-full z-50 bg-parchment/95 backdrop-blur-sm border-b border-paper-line"
>
    <div class="container mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
            <a
                href="/"
                on:click={closeMenu}
                class="text-3xl font-display font-bold text-mahogany hover:text-brass transition-colors duration-300 tracking-tighter decoration-mahogany/20 underline-offset-4 decoration-2"
            >
                HAMZA & CO.
            </a>

            <div class="hidden md:flex items-center space-x-12">
                <ul class="flex space-x-12">
                    {#each allNavItems as item}
                        <li>
                            <a
                                href={item.href}
                                class="legal-nav-link {$page.url.pathname ===
                                item.href
                                    ? 'active'
                                    : ''}"
                            >
                                {item.label}
                            </a>
                        </li>
                    {/each}
                </ul>
            </div>

            <div class="flex items-center space-x-4 md:hidden">
                <button
                    on:click={toggleMenu}
                    class="text-mahogany hover:text-brass focus:outline-none transition-colors duration-300"
                    aria-label="Toggle Menu"
                >
                    {#if isMobileMenuOpen}
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-6 w-6"
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
                    {:else}
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16"
                            />
                        </svg>
                    {/if}
                </button>
            </div>
        </div>
    </div>

    {#if isMobileMenuOpen}
        <div
            transition:slide={{ duration: 300 }}
            class="md:hidden border-t border-paper-line bg-parchment"
        >
            <ul class="flex flex-col px-4 py-8 space-y-6">
                {#each allNavItems as item}
                    <li>
                        <a
                            href={item.href}
                            on:click={closeMenu}
                            class="block w-full text-lg font-display font-bold uppercase tracking-widest transition-colors duration-300 {$page
                                .url.pathname === item.href
                                ? 'text-mahogany'
                                : 'text-mahogany/60 hover:text-mahogany'}"
                        >
                            {item.label}
                        </a>
                    </li>
                {/each}
            </ul>
        </div>
    {/if}
</nav>
