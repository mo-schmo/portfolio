<script lang="ts">
    import { page } from "$app/stores";
    import { auth, checkAuth } from "$lib/stores/auth";
    import { slide } from "svelte/transition";
    import { onMount } from "svelte";

    let isCondensed = false;
    let rafId: number | null = null;

    onMount(() => {
        checkAuth();

        const onScroll = () => {
            if (rafId !== null) return;
            rafId = requestAnimationFrame(() => {
                isCondensed = window.scrollY > 24;
                rafId = null;
            });
        };
        onScroll();
        window.addEventListener("scroll", onScroll, { passive: true });
        return () => {
            window.removeEventListener("scroll", onScroll);
            if (rafId !== null) cancelAnimationFrame(rafId);
        };
    });

    const navItems = [
        { href: "/", label: "Home" },
        { href: "/projects", label: "Projects" },
        { href: "/oracles", label: "Oracles" },
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

    function closeMenu() {
        isMobileMenuOpen = false;
    }
</script>

<nav
    class="masthead-nav fixed top-0 w-full z-50 bg-parchment/90 backdrop-blur-md"
    class:is-condensed={isCondensed}
>
    <div class="container mx-auto px-6 nav-row">
        <div class="flex items-center justify-between">
            <a
                href="/"
                on:click={closeMenu}
                class="wordmark font-display text-mahogany hover:text-brass transition-colors"
                aria-label="Hamza &amp; Co. — Home"
            >
                <span class="wordmark-h">Hamza</span>
                <span class="wordmark-amp">&amp;</span>
                <span class="wordmark-co">Co.</span>
            </a>

            <div class="hidden md:flex items-center">
                <ul class="flex items-center gap-x-9">
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
                    aria-expanded={isMobileMenuOpen}
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
                                stroke-width="1.5"
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
                                stroke-width="1.5"
                                d="M4 7h16M4 12h16M4 17h16"
                            />
                        </svg>
                    {/if}
                </button>
            </div>
        </div>
    </div>

    <span class="brass-hairline" aria-hidden="true"></span>

    {#if isMobileMenuOpen}
        <div
            transition:slide={{ duration: 240 }}
            class="md:hidden bg-parchment border-t border-paper-line"
        >
            <ul class="flex flex-col px-6 py-6">
                {#each allNavItems as item}
                    <li class="border-b border-paper-line/40 last:border-b-0">
                        <a
                            href={item.href}
                            on:click={closeMenu}
                            class="block py-4 eyebrow {$page.url.pathname ===
                            item.href
                                ? 'text-mahogany'
                                : 'hover:text-mahogany'}"
                        >
                            {item.label}
                        </a>
                    </li>
                {/each}
            </ul>
        </div>
    {/if}
</nav>

<style>
    .masthead-nav {
        transition: backdrop-filter 240ms ease-out;
    }

    .nav-row {
        padding-top: 1.4rem;
        padding-bottom: 1.4rem;
        transition: padding 260ms cubic-bezier(0.2, 0.7, 0.2, 1);
    }

    .is-condensed .nav-row {
        padding-top: 0.85rem;
        padding-bottom: 0.85rem;
    }

    .wordmark {
        display: inline-flex;
        align-items: baseline;
        gap: 0.25ch;
        font-weight: 500;
        font-size: clamp(1.35rem, 1.05rem + 0.8vw, 1.7rem);
        letter-spacing: -0.005em;
        line-height: 1;
        font-feature-settings: "liga" 1, "dlig" 1;
    }

    .wordmark-amp {
        font-style: italic;
        font-weight: 400;
        color: var(--brass);
        font-size: 0.85em;
        transform: translateY(-0.04em);
    }

    .wordmark-co {
        font-weight: 400;
        letter-spacing: 0;
    }

    /* 1px brass hairline replacing the heavy paper-line border */
    .brass-hairline {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent 0,
            color-mix(in oklch, var(--brass) 60%, transparent) 14%,
            color-mix(in oklch, var(--brass) 60%, transparent) 86%,
            transparent 100%
        );
        opacity: 0.55;
        pointer-events: none;
    }

    @media (prefers-reduced-motion: reduce) {
        .nav-row {
            transition: none;
        }
    }
</style>
