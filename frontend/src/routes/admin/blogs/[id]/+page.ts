import { fetchBlogByIdAdmin } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
    if (params.id === 'new') {
        return { blog: null };
    }
    try {
        const blog = await fetchBlogByIdAdmin(params.id, fetch);
        return { blog };
    } catch (e) {
        return { blog: null, error: "Briefing not found" };
    }
};
