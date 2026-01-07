<script lang="ts">
    import { page } from '$app/stores';
    import { slide } from 'svelte/transition';
    import ThemeToggle from './ThemeToggle.svelte';

    const navItems = [
        { href: '/', label: 'Home' },
        { href: '/projects', label: 'Projects' },
        { href: '/blog', label: 'Blog' },
        { href: '/contact', label: 'Contact' }
    ];

    let isMobileMenuOpen = false;

    function toggleMenu() {
        isMobileMenuOpen = !isMobileMenuOpen;
    }

    // Close menu when a link is clicked
    function closeMenu() {
        isMobileMenuOpen = false;
    }
</script>

<nav class="fixed top-0 w-full z-50 bg-cyber-card-95 backdrop-blur-md border-b border-cyber-border">
    <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
            <a href="/" on:click={closeMenu} class="text-2xl font-bold text-cyber-text hover:text-cyber-cyan transition-colors duration-300">
                MH
            </a>

            <div class="hidden md:flex items-center space-x-8">
                <ul class="flex space-x-8">
                    {#each navItems as item}
                        <li>
                            <a
                                href={item.href}
                                class="transition-colors duration-300 {$page.url.pathname === item.href ? 'text-cyber-cyan' : 'text-cyber-text-muted hover:text-cyber-cyan'}"
                            >
                                {item.label}
                            </a>
                        </li>
                    {/each}
                </ul>
                <ThemeToggle />
            </div>

            <div class="flex items-center space-x-4 md:hidden">
                <ThemeToggle />
                
                <button 
                    on:click={toggleMenu}
                    class="text-cyber-text hover:text-cyber-cyan focus:outline-none transition-colors duration-300"
                    aria-label="Toggle Menu"
                >
                    {#if isMobileMenuOpen}
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    {:else}
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    {/if}
                </button>
            </div>
        </div>
    </div>

    {#if isMobileMenuOpen}
        <div 
            transition:slide={{ duration: 300 }}
            class="md:hidden border-t border-cyber-border bg-cyber-card-95"
        >
            <ul class="flex flex-col px-4 py-4 space-y-4">
                {#each navItems as item}
                    <li>
                        <a
                            href={item.href}
                            on:click={closeMenu}
                            class="block w-full py-2 text-lg transition-colors duration-300 {$page.url.pathname === item.href ? 'text-cyber-cyan' : 'text-cyber-text-muted hover:text-cyber-cyan'}"
                        >
                            {item.label}
                        </a>
                    </li>
                {/each}
            </ul>
        </div>
    {/if}
</nav>