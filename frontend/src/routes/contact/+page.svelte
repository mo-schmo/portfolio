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

<div class="container mx-auto px-4 py-12 max-w-2xl">
	<h1
		class="text-3xl md:text-5xl font-bold mb-12 text-cyber-text text-center"
	>
		Get In Touch
	</h1>

	<div class="glass-card p-6 md:p-12 rounded-lg">
		{#if submitted}
			<div class="text-center">
				<div class="text-4xl mb-4">✓</div>
				<h2 class="text-2xl font-bold text-cyber-accent mb-4">
					Message Sent!
				</h2>
				<p class="mb-6">
					Thank you for reaching out. I'll get back to you soon.
				</p>
				<button
					on:click={() => (submitted = false)}
					class="px-6 py-2 neon-border glow-on-hover"
				>
					Send Another Message
				</button>
			</div>
		{:else}
			<form on:submit|preventDefault={handleSubmit} class="space-y-6">
				<div>
					<label
						for="name"
						class="block text-cyber-text mb-2 font-bold"
					>
						Name
					</label>
					<input
						id="name"
						type="text"
						bind:value={formData.name}
						required
						class="w-full px-4 py-3 bg-cyber-card border border-cyber-border focus:border-cyber-cyan focus:outline-none rounded-lg text-cyber-text"
						placeholder="Your Name"
					/>
				</div>

				<div>
					<label
						for="email"
						class="block text-cyber-text mb-2 font-bold"
					>
						Email
					</label>
					<input
						id="email"
						type="email"
						bind:value={formData.email}
						required
						class="w-full px-4 py-3 bg-cyber-card border border-cyber-border focus:border-cyber-cyan focus:outline-none rounded-lg text-cyber-text"
						placeholder="your.email@example.com"
					/>
				</div>

				<div>
					<label
						for="message"
						class="block text-cyber-text mb-2 font-bold"
					>
						Message
					</label>
					<textarea
						id="message"
						bind:value={formData.message}
						required
						rows="6"
						class="w-full px-4 py-3 bg-cyber-card border border-cyber-border focus:border-cyber-cyan focus:outline-none rounded-lg resize-none text-cyber-text"
						placeholder="Your message..."
					></textarea>
				</div>

				<button
					type="submit"
					disabled={submitting}
					class="w-full px-8 py-4 neon-border text-cyber-text hover:text-cyber-cyan bg-cyber-card font-bold text-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
				>
					{submitting ? "Sending..." : "Send Message"}
				</button>
			</form>
		{/if}
	</div>

	<div class="mt-12 text-center">
		<p class="text-cyber-text-muted mb-4">Or reach out directly:</p>
		<a
			href="mailto:HAMZA.ABJOL.MOHAMMED@GMAIL.COM"
			class="text-cyber-cyan hover:text-cyber-accent transition-colors text-lg md:text-xl break-all"
		>
			HAMZA.ABJOL.MOHAMMED@GMAIL.COM
		</a>
	</div>
</div>
