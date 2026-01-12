import { fetchBlogById } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params }) => {
    if (params.id === 'new') {
        return { blog: null };
    }
    try {
        const blog = await fetchBlogById(params.id);
        return { blog };
    } catch (e) {
        return { blog: null, error: "Briefing not found" };
    }
};
