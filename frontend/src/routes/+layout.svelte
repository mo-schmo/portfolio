<script lang="ts">
	import "../app.css";
	import { onMount } from "svelte";
	import { initWebSocket } from "$lib/stores/webSocket";
	import Navbar from "$lib/components/Navbar.svelte";
	import Footer from "$lib/components/Footer.svelte";
	import ProcessServer from "$lib/components/ProcessServer.svelte";
	import LegalWire from "$lib/components/LegalWire.svelte";

	onMount(() => {
		initWebSocket();
	});
</script>

<div class="min-h-screen flex flex-col relative" style="z-index: 0;">
	<Navbar />

	<!-- Real-time overlays -->
	<ProcessServer />

	<main class="flex-grow pt-20">
		<slot />
	</main>
	<Footer />

	<!-- The Wire sits on top of the footer -->
	<LegalWire />
</div>
