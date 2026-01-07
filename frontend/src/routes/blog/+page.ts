import { fetchAllBlogs } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
    try {
        const posts = await fetchAllBlogs();
        return {
            posts
        };
    } catch (error) {
        console.error('Error loading blogs:', error);
        return {
            posts: [],
            error: 'Failed to load blog posts'
        };
    }
};
