<script lang="ts">
	let formData = {
		name: "",
		email: "",
		message: "",
	};

	let submitted = false;
	let submitting = false;

	async function handleSubmit() {
		submitting = true;
		// In the future, this will connect to the backend API
		await new Promise((resolve) => setTimeout(resolve, 1000));
		submitted = true;
		submitting = false;
		formData = { name: "", email: "", message: "" };
	}
</script>

<svelte:head>
	<title>Contact - Mohammed Hamza</title>
</svelte:head>

<div class="container mx-auto px-4 py-28 max-w-2xl">
	<h1
		class="text-4xl md:text-6xl font-display font-black mb-16 text-mahogany text-center tracking-tighter uppercase"
	>
		Notice of Inquiry
	</h1>

	<div class="legal-folio p-10 md:p-14 bg-white/50">
		{#if submitted}
			<div class="text-center py-8">
				<div class="text-5xl mb-6 text-brass">密封</div>
				<h2 class="text-3xl font-display font-bold text-mahogany mb-6">
					Communication Received
				</h2>
				<p class="mb-10 font-serif italic text-lg text-mahogany/70">
					Your inquiry has been logged. Expect a formal response in
					due course.
				</p>
				<button
					on:click={() => (submitted = false)}
					class="btn-outline-legal text-xs px-10"
				>
					Issue New Notice
				</button>
			</div>
		{:else}
			<form on:submit|preventDefault={handleSubmit} class="space-y-8">
				<div>
					<label
						for="name"
						class="block text-mahogany font-display font-bold uppercase tracking-widest text-xs mb-3"
					>
						Full Name / Entity
					</label>
					<input
						id="name"
						type="text"
						bind:value={formData.name}
						required
						class="w-full px-5 py-4 bg-parchment/30 border border-paper-line focus:border-mahogany focus:outline-none font-serif text-lg placeholder:text-mahogany/30 italic"
						placeholder="The undersigned..."
					/>
				</div>

				<div>
					<label
						for="email"
						class="block text-mahogany font-display font-bold uppercase tracking-widest text-xs mb-3"
					>
						Electronic Correspondence
					</label>
					<input
						id="email"
						type="email"
						bind:value={formData.email}
						required
						class="w-full px-5 py-4 bg-parchment/30 border border-paper-line focus:border-mahogany focus:outline-none font-serif text-lg placeholder:text-mahogany/30 italic"
						placeholder="correspondence@domain.com"
					/>
				</div>

				<div>
					<label
						for="message"
						class="block text-mahogany font-display font-bold uppercase tracking-widest text-xs mb-3"
					>
						Subject Matter
					</label>
					<textarea
						id="message"
						bind:value={formData.message}
						required
						rows="6"
						class="w-full px-5 py-4 bg-parchment/30 border border-paper-line focus:border-mahogany focus:outline-none rounded-none resize-none font-serif text-lg placeholder:text-mahogany/30 italic"
						placeholder="Elaborate on the nature of your request..."
					></textarea>
				</div>

				<button
					type="submit"
					disabled={submitting}
					class="w-full btn-legal disabled:opacity-50 disabled:cursor-not-allowed"
				>
					{submitting ? "Processing..." : "Submit Formal Inquiry"}
				</button>
			</form>
		{/if}
	</div>

	<div class="mt-20 text-center">
		<p
			class="text-mahogany/50 font-display font-bold uppercase tracking-[0.2em] text-xs mb-6"
		>
			Direct Line of Communication
		</p>
		<a
			href="mailto:HAMZA.ABJOL.MOHAMMED@GMAIL.COM"
			class="text-mahogany hover:text-brass transition-colors text-lg md:text-2xl font-display font-black tracking-tighter decoration-mahogany/20 underline-offset-8 decoration-2 break-all"
		>
			HAMZA.ABJOL.MOHAMMED@GMAIL.COM
		</a>
	</div>
</div>
