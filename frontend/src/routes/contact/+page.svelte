<script lang="ts">
	import { fade, fly, scale } from "svelte/transition";
	import { cubicIn, quintOut } from "svelte/easing";

	let formData = {
		name: "",
		email: "",
		message: "",
	};

	let submitted = false;
	let submitting = false;

	async function handleSubmit() {
		submitting = true;
		try {
			const response = await fetch(
				"https://formsubmit.co/ajax/HAMZA.ABJOL.MOHAMMED@GMAIL.COM",
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
						Accept: "application/json",
					},
					body: JSON.stringify({
						name: formData.name,
						email: formData.email,
						message: formData.message,
						_subject: "New Inquiry from Portfolio",
						_captcha: "false", // Disable captcha for smoother UX
						// Honey pot field handled by formsubmit.co automatically if named _honey?
						// Actually formsubmit.co uses a hidden input named _honey. We'll add it in the markup for safety if we were using standard form sub logic,
						// but for AJAX we can just send it empty if we want, or rely on their backend detection.
						// Let's explicitly send an empty _honey for good measure in the JSON body if needed,
						// but usually it's a hidden field in the DOM. We'll handle it in markup to be safe/standard
					}),
				},
			);

			if (response.ok) {
				submitted = true;
				formData = { name: "", email: "", message: "" };
			} else {
				alert("Something went wrong. Please try again.");
			}
		} catch (error) {
			console.error(error);
			alert("Something went wrong. Please try again.");
		} finally {
			submitting = false;
		}
	}
</script>

<svelte:head>
	<title>Contact - Mohammed Hamza</title>
</svelte:head>

<div class="container mx-auto px-4 py-28 max-w-2xl overflow-hidden">
	<h1
		class="text-4xl md:text-6xl font-display font-black mb-16 text-mahogany text-center tracking-tighter uppercase"
	>
		Notice of Inquiry
	</h1>

	<div class="legal-folio p-10 md:p-14 bg-white/50 relative min-h-[500px]">
		{#if submitted}
			<div
				in:scale={{
					duration: 400,
					start: 1.5,
					opacity: 0,
					easing: cubicIn,
				}}
				out:fly={{ x: -200, duration: 400, opacity: 0 }}
				class="text-center py-8 absolute inset-0 flex flex-col items-center justify-center"
			>
				<div
					class="text-5xl mb-6 text-brass transform rotate-[-12deg] border-4 border-brass p-4 inline-block font-black tracking-widest opacity-80 mix-blend-multiply"
				>
					密封
				</div>
				<h2 class="text-3xl font-display font-bold text-mahogany mb-6">
					Communication Received
				</h2>
				<p
					class="mb-10 font-serif italic text-lg text-mahogany/70 max-w-sm mx-auto"
				>
					Your inquiry has been logged. Expect a formal response in
					due course.
				</p>
				<button
					on:click={() => (submitted = false)}
					class="btn-outline-legal text-xs px-10 hover:bg-mahogany hover:text-white transition-colors"
				>
					Issue New Notice
				</button>
			</div>
		{:else}
			<div
				in:fly={{ x: 200, duration: 500, delay: 200, easing: quintOut }}
				out:fade={{ duration: 200 }}
			>
				<form on:submit|preventDefault={handleSubmit} class="space-y-8">
					<!-- Honey pot to prevent spam -->
					<input type="text" name="_honey" style="display:none" />

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
						class="w-full btn-legal disabled:opacity-50 disabled:cursor-not-allowed group relative overflow-hidden"
					>
						<span
							class="relative z-10 transition-colors duration-300"
						>
							{submitting
								? "Processing..."
								: "Submit Formal Inquiry"}
						</span>
					</button>
				</form>
			</div>
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
