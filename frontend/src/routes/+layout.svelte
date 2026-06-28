<script lang="ts">
	import "../app.css";
	import { onMount } from "svelte";
	import { page } from "$app/stores";
	import { initWebSocket } from "$lib/stores/webSocket";
	import Navbar from "$lib/components/Navbar.svelte";
	import Footer from "$lib/components/Footer.svelte";
	import ProcessServer from "$lib/components/ProcessServer.svelte";
	import LegalWire from "$lib/components/LegalWire.svelte";

	onMount(() => {
		initWebSocket();

		// Mouse tracking for the ink-bloom hover effect on cards.
		// Cheap: only fires on mousemove inside elements that opt in.
		const handler = (e: MouseEvent) => {
			const target = e.target as HTMLElement | null;
			const card = target?.closest<HTMLElement>(".ink-bloom");
			if (!card) return;
			const rect = card.getBoundingClientRect();
			const x = ((e.clientX - rect.left) / rect.width) * 100;
			const y = ((e.clientY - rect.top) / rect.height) * 100;
			card.style.setProperty("--bloom-x", `${x}%`);
			card.style.setProperty("--bloom-y", `${y}%`);
		};
		window.addEventListener("mousemove", handler, { passive: true });
		return () => window.removeEventListener("mousemove", handler);
	});
</script>

<div class="min-h-screen flex flex-col relative" style="z-index: 0;">
	<Navbar />

	<!-- Real-time overlays -->
	<ProcessServer />

	<main class="flex-grow pt-20">
		{#key $page.url.pathname}
			<div class="page-enter">
				<slot />
			</div>
		{/key}
	</main>
	<Footer />

	<!-- The Wire sits on top of the footer -->
	<LegalWire />
</div>
