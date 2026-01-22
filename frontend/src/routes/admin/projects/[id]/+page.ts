import { fetchProjectByIdAdmin } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
    if (params.id === 'new') {
        return { project: null };
    }
    try {
        const project = await fetchProjectByIdAdmin(params.id, fetch);
        return { project };
    } catch (e) {
        return { project: null, error: "Record not found" };
    }
};
