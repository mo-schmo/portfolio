<script lang="ts">
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import Footer from '$lib/components/Footer.svelte';
</script>

<div class="min-h-screen flex flex-col relative" style="z-index: 0;">
	<Navbar />
	<main class="flex-grow pt-20">
		<slot />
	</main>
	<Footer />
</div>
