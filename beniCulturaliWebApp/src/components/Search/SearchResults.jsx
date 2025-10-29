import React from "react";


export default function SearchResults({
    isLoading,
    error,
    searchTerm,
    artifact
}) {
    const hasSearchTerm = searchTerm && searchTerm.trim().length > 0;
    const hasArtifacts = artifact && artifact.length > 0;

    if (isLoading) {
        return <div className="loading">Searching...</div>;
    }

    if (error) {
        return <div className="error">Error: {error}</div>;
    }

    if (hasSearchTerm && !hasArtifacts) {
        // Condition: Search executed, but no results found
        return <div className="no-results">No artifacts found matching "{searchTerm}"</div>;
    }

    if (hasArtifacts) {
        // Condition: Success! Render results
        return <Tiles artifact={artifact} />;
    }

    // Default/Initial state: Input is empty and no default data exists
    return <div className="no-results">Start typing to search for artifacts.</div>;

}