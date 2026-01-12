import { fetchProjectById } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params }) => {
    if (params.id === 'new') {
        return { project: null };
    }
    try {
        const project = await fetchProjectById(params.id);
        return { project };
    } catch (e) {
        return { project: null, error: "Record not found" };
    }
};
