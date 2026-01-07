import { fetchBlogBySlug } from '$lib/api';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params }) => {
    try {
        const post = await fetchBlogBySlug(params.slug);
        return {
            post
        };
    } catch (e: any) {
        console.error('Error loading blog post:', e);
        if (e.message === 'Blog post not found') {
            throw error(404, 'Blog post not found');
        }
        throw error(500, 'Internal Server Error');
    }
};
