export interface BlogPost {
	id: number;
	title: string;
	slug: string;
	excerpt: string;
	content: string;
	publishedAt: string;
	createdAt: string;
}

export interface Project {
	id: number;
	title: string;
	description: string;
	imageUrl?: string;
	githubUrl?: string;
	liveUrl?: string;
	technologies: string[];
	featured: boolean;
	createdAt: string;
}

export const mockBlogPosts: BlogPost[] = [
	{
		id: 1,
		title: "Building Scalable APIs with Go",
		slug: "building-scalable-apis-with-go",
		excerpt: "Exploring patterns and practices for building high-performance REST APIs in Golang.",
		content: "# Building Scalable APIs with Go\n\nGo has become one of my favorite languages for building backend services. In this post, I'll share some patterns I've learned while building production APIs...",
		publishedAt: "2024-01-15T10:00:00Z",
		createdAt: "2024-01-15T10:00:00Z"
	},
	{
		id: 2,
		title: "Migrating Vue.js to React: Lessons Learned",
		slug: "migrating-vue-to-react",
		excerpt: "My experience migrating a large Vue.js application to React at Ford Motor Company Credit.",
		content: "# Migrating Vue.js to React: Lessons Learned\n\nWhen we decided to migrate our legacy Vue.js application to React, the goal was to unify our tech stack...",
		publishedAt: "2024-01-10T10:00:00Z",
		createdAt: "2024-01-10T10:00:00Z"
	},
	{
		id: 3,
		title: "Cloud Migration to GCP: A Success Story",
		slug: "cloud-migration-gcp",
		excerpt: "How we migrated our infrastructure to Google Cloud Platform, improving performance and reducing costs.",
		content: "# Cloud Migration to GCP: A Success Story\n\nCloud migration is never easy, but the benefits can be transformative...",
		publishedAt: "2024-01-05T10:00:00Z",
		createdAt: "2024-01-05T10:00:00Z"
	}
];

export const mockProjects: Project[] = [
	{
		id: 1,
		title: "Trace-Bio App",
		description: "Cross-platform React Native companion app to a wearable biosensor. Enabled real-time measurements to be drawn from the sensor and provided graphical visualizations of metrics.",
		technologies: ["React Native", "JavaScript", "GraphQL"],
		featured: true,
		createdAt: "2023-06-01T00:00:00Z"
	},
	{
		id: 2,
		title: "FlexiT",
		description: "An Android app designed to help users get in the habit of exercising by providing workouts, music, and motivational quotes.",
		technologies: ["Android", "Java", "Firebase"],
		featured: true,
		createdAt: "2022-03-15T00:00:00Z"
	},
	{
		id: 3,
		title: "ML-Based Vehicle Recommendation System",
		description: "Machine learning application built with Flask for recommending next vehicles to customers based on their preferences and history.",
		technologies: ["Python", "Flask", "Machine Learning", "Scikit-learn"],
		featured: false,
		createdAt: "2021-08-20T00:00:00Z"
	}
];
