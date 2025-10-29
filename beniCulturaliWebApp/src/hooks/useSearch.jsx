import { useState, useCallback, useEffect, useRef } from "react";
import { quickSearch } from "../utils/api"; // Assuming the path is correct

// A simple debounce utility function
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

export default function useSearch() {
    // 1. New State for the immediate input value
    const [searchTerm, setSearchTerm] = useState('');
    
    // 2. States for API call results
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    // This ref helps manage the promise cleanup for race conditions
    const abortControllerRef = useRef(null);

    // The actual function that performs the API call
    const executeSearch = useCallback(async(query) => {
        const trimmedQuery = query.trim();
        if (!trimmedQuery) {
            setData(null);
            return;
        }

        // Cleanup any previous running request before starting a new one
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }

        const controller = new AbortController();
        abortControllerRef.current = controller;
        
        setIsLoading(true);
        setError(null);

        try {
            // Pass the signal for abortion
            const response = await quickSearch(trimmedQuery, { signal: controller.signal });
            // Check if the request was aborted before setting state
            if (!controller.signal.aborted) {
                setData(response.items || []);
            }
        } catch (err) {
            // Ignore AbortError, which happens when a new search overwrites the old one
            if (err.name === 'AbortError') {
                console.log("Fetch aborted:", trimmedQuery);
                return; 
            }
            console.error("API error message", err.message)
            setError(err.message);
            setData(null);
        } finally {
             // Only set loading to false if this is the latest, completed request
            if (abortControllerRef.current === controller) {
                setIsLoading(false);
                abortControllerRef.current = null;
            }
        }
    }, []); 

    // Create a debounced version of executeSearch
    const debouncedSearch = useCallback(debounce(executeSearch, 500), [executeSearch]);
    const MIN_SEARCH_LENGTH = 1;
    // Effect to trigger search whenever searchTerm changes (Debounced search)
    useEffect(() => {
        if (searchTerm.trim().length > MIN_SEARCH_LENGTH) {
            debouncedSearch(searchTerm);
        } else {
            // Clear results immediately if the input is empty
            setData(null);
            setError(null);
            setIsLoading(false);
        }
        
        // Cleanup function: abort any pending request when the component unmounts 
        // or before the next searchTerm change
        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
                abortControllerRef.current = null;
            }
        };

    }, [searchTerm, debouncedSearch]); // Re-run effect when searchTerm or debouncedSearch changes

    return {
        data,
        isLoading,
        error,
        searchTerm,
        setSearchTerm // Export setter to be used in Searchbar.jsx
    };
}



//the debounce function is a utility that
//delays the execution of a function until 
//after a specified wait time has passed since the last time it was invoked.
//This is particularly useful for optimizing performance 
// in scenarios like search input fields, where you want to limit the number of API calls made as the user types.  