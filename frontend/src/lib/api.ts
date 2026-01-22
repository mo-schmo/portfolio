import { PUBLIC_API_URL } from '$env/static/public';

export const BASE_URL = PUBLIC_API_URL || 'http://localhost:8080/api';

export interface BlogPost {
    id: number;
    title: string;
    slug: string;
    excerpt: string;
    content: string;
    publishedAt: string;
    isDraft: boolean;
}

export interface Project {
    id: number;
    title: string;
    slug: string;
    description: string;
    content: string;
    imageUrl?: string;
    githubUrl?: string;
    liveUrl?: string;
    technologies: string; // JSON array stored as string
    featured: boolean;
    createdAt: string;
    updatedAt: string;
    isDraft: boolean;
}

export async function fetchAllBlogs(): Promise<BlogPost[]> {
    const response = await fetch(`${BASE_URL}/blog`);
    if (!response.ok) {
        throw new Error('Failed to fetch blogs');
    }
    return response.json();
}

export async function fetchAllBlogsAdmin(fetch = window.fetch): Promise<BlogPost[]> {
    const response = await fetch(`${BASE_URL}/admin/blog`, { credentials: 'include' });
    if (!response.ok) {
        throw new Error('Failed to fetch blogs');
    }
    return response.json();
}

export async function fetchBlogBySlug(slug: string): Promise<BlogPost> {
    const response = await fetch(`${BASE_URL}/blog/slug/${slug}`);
    if (!response.ok) {
        if (response.status === 404) {
            throw new Error('Blog post not found');
        }
        throw new Error('Failed to fetch blog post');
    }
    return response.json();
}

export async function fetchAllProjects(): Promise<Project[]> {
    const response = await fetch(`${BASE_URL}/projects`);
    if (!response.ok) {
        throw new Error('Failed to fetch projects');
    }
    return response.json();
}

export async function fetchAllProjectsAdmin(fetch = window.fetch): Promise<Project[]> {
    const response = await fetch(`${BASE_URL}/admin/projects`, { credentials: 'include' });
    if (!response.ok) {
        throw new Error('Failed to fetch projects');
    }
    return response.json();
}

export async function fetchProjectBySlug(slug: string): Promise<Project> {
    const response = await fetch(`${BASE_URL}/projects/slug/${slug}`);
    if (!response.ok) {
        if (response.status === 404) {
            throw new Error('Project not found');
        }
        throw new Error('Failed to fetch project');
    }
    return response.json();
}

export async function fetchBlogById(id: string | number): Promise<BlogPost> {
    const response = await fetch(`${BASE_URL}/blog/${id}`);
    if (!response.ok) {
        throw new Error('Failed to fetch blog post');
    }
    return response.json();
}

export async function fetchBlogByIdAdmin(id: string | number, fetch = window.fetch): Promise<BlogPost> {
    const response = await fetch(`${BASE_URL}/admin/blog/${id}`, { credentials: 'include' });
    if (!response.ok) {
        throw new Error('Failed to fetch blog post');
    }
    return response.json();
}

export async function fetchProjectById(id: string | number): Promise<Project> {
    const response = await fetch(`${BASE_URL}/projects/${id}`);
    if (!response.ok) {
        throw new Error('Failed to fetch project');
    }
    return response.json();
}

export async function fetchProjectByIdAdmin(id: string | number, fetch = window.fetch): Promise<Project> {
    const response = await fetch(`${BASE_URL}/admin/projects/${id}`, { credentials: 'include' });
    if (!response.ok) {
        throw new Error('Failed to fetch project');
    }
    return response.json();
}
