<script lang="ts">
	import { onMount } from 'svelte';
	
	const experience = [
		{
			title: "Software Engineer, Tech Lead",
			company: "Ford Motor Company Credit - Consumer Offers and Renewals",
			period: "Jan 2022 - Present",
			achievements: [
				"Migrated legacy Vue.js app to React.js, unifying tech stack and boosting scalability and productivity",
				"Built CI/CD pipelines with Google Cloud Build, automating deployments and improving release reliability",
				"Led cloud migration to GCP using Cloud Run, Postgres, and BigQuery for higher performance and lower cost",
				"Integrated Adobe Experience Manager with GraphQL APIs, streamlining content delivery workflows",
				"Enhanced observability with Cloud Monitoring, ContentSquare, and Splunk integrations",
				"Designed and deployed automated BigQuery-to-Postgres pipelines with Apache Beam on Dataflow, cutting data sync time and enhancing analytics reliability"
			]
		},
		{
			title: "Software Engineer",
			company: "Ford Motor Company Credit",
			period: "Jan 2021 – Dec 2021",
			achievements: [
				"Developed Vue.js front-end with Spring Boot microservices, improving modularity and scalability",
				"Built an ML-based next-vehicle recommendation app using Flask",
				"Cut API latency from ~5s to ~200ms through caching and ORM optimization",
				"Implemented WCAG-compliant E2E tests and optimized MySQL for high-volume environments",
				"Automated onboarding workflows with DevOps scripting to accelerate developer setup"
			]
		}
	];

	const skills = {
		Languages: ["Java", "Python", "JavaScript", "R", "C++", "Golang", "C"],
		Frameworks: ["React Native", "React", "Vue.js", "Java Spring Boot", "GraphQL"],
		DevOps: ["GitHub", "Jenkins", "Docker", "Google Cloud Build", "Cloud Run", "BigQuery"],
		Practices: ["Agile", "Paired Programming", "Test-Driven Development"]
	};

	let mounted = false;
	onMount(() => {
		mounted = true;
	});
</script>

<svelte:head>
	<title>Mohammed Hamza - Software Engineer</title>
</svelte:head>

<div class="container mx-auto px-4 py-12">
	<!-- Hero Section -->
	<section class="text-center mb-20">
		<div class="mb-8">
			<h1 class="text-6xl md:text-8xl font-bold mb-4 neon-text animate-glow">
				MOHAMMED HAMZA
			</h1>
			<div class="text-2xl md:text-3xl text-cyber-pink mb-4 neon-text">
				Software Engineer
			</div>
			<div class="text-xl text-cyber-brown/90 mb-6">
				Detroit, MI
			</div>
			<a
				href="/contact"
				class="inline-block px-8 py-3 neon-border glow-on-hover bg-black/20"
			>
				Contact Me
			</a>
		</div>
	</section>

	<!-- About Section -->
	<section class="mb-20">
		<h2 class="text-4xl font-bold mb-8 neon-text">About</h2>
		<div class="glass-card p-8 rounded-lg">
			<p class="text-lg leading-relaxed mb-4">
				Experienced Software Engineer and Tech Lead with a passion for building scalable applications and leading technical initiatives. 
				Specialized in modern web technologies, cloud architecture, and full-stack development.
			</p>
			<p class="text-lg leading-relaxed">
				Currently working on breaking into the legal field and getting into law school, 
				while continuously exploring new technologies and best practices.
			</p>
		</div>
	</section>

	<!-- Experience Section -->
	<section class="mb-20">
		<h2 class="text-4xl font-bold mb-8 neon-text">Experience</h2>
		<div class="space-y-8">
			{#each experience as exp}
				<div class="glass-card p-6 rounded-lg border-l-4 border-cyber-cyan">
					<div class="mb-4">
						<h3 class="text-2xl font-bold text-cyber-pink mb-2">{exp.title}</h3>
						<div class="text-xl text-cyber-cyan mb-2">{exp.company}</div>
						<div class="text-cyber-cyan/70">{exp.period}</div>
					</div>
					<ul class="space-y-2">
						{#each exp.achievements as achievement}
							<li class="flex items-start">
								<span class="text-cyber-cyan mr-2">▸</span>
								<span>{achievement}</span>
							</li>
						{/each}
					</ul>
				</div>
			{/each}
		</div>
	</section>

	<!-- Education Section -->
	<section class="mb-20">
		<h2 class="text-4xl font-bold mb-8 neon-text">Education</h2>
		<div class="glass-card p-6 rounded-lg">
			<h3 class="text-2xl font-bold text-cyber-pink mb-2">Wayne State University</h3>
			<div class="text-xl text-cyber-cyan mb-2">Bachelor of Science in Computer Science</div>
			<div class="text-cyber-cyan/70 mb-2">Minor in Mathematics w/ Concentration in Data Science</div>
			<div class="text-cyber-cyan/70">Fall 2017 – Winter 2020 • Detroit, MI</div>
		</div>
	</section>

	<!-- Skills Section -->
	<section class="mb-20">
		<h2 class="text-4xl font-bold mb-8 neon-text">Skills & Technologies</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
			{#each Object.entries(skills) as [category, items]}
				<div class="glass-card p-6 rounded-lg">
					<h3 class="text-xl font-bold text-cyber-pink mb-4">{category}</h3>
					<ul class="space-y-2">
						{#each items as item}
							<li>{item}</li>
						{/each}
					</ul>
				</div>
			{/each}
		</div>
	</section>
</div>
