import { fetchAllProjects } from '$lib/api';
import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
    try {
        const projects = await fetchAllProjects();
        return {
            projects
        };
    } catch (error) {
        console.error('Error in projects load:', error);
        return {
            projects: []
        };
    }
};
