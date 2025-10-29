import { useState, useCallback } from 'react';

export function useArtifactSearch() {
    const [state, setState] = useState(
        {
            results: [],
            isLoading: false,
            error: null,
            pagination: {
                page: 1,
                perPage: 20,
                total: 0
            }
        }
    );

    const search = useCallback(async (params) => {
        const searchParams = new SearchParamsManager(params);
        try {
            const response = await searchArtifacts(searchParams.build());
        } catch (error) {
            const formattedError = formatArtifactError(error);
            setState((prevState) => ({
                ...prevState,
                isLoading: false,
                error: formattedError
            }));
        }
    }, []);

    return {
        ...state,
        search
    };
}
