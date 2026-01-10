import { fetchProjectBySlug } from '$lib/api';
import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ params }) => {
    try {
        const project = await fetchProjectBySlug(params.slug);
        return {
            project
        };
    } catch (e) {
        console.error('Error fetching project:', e);
        throw error(404, 'Project record not found');
    }
};
