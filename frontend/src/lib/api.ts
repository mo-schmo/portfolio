const BASE_URL = 'http://localhost:8080/api';

export interface BlogPost {
    id: number;
    title: string;
    slug: string;
    excerpt: string;
    content: string;
    publishedAt: string;
}

export async function fetchAllBlogs(): Promise<BlogPost[]> {
    const response = await fetch(`${BASE_URL}/blog`);
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
