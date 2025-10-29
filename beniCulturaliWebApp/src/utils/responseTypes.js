/**
 * Database Models(comples) -> DTO(simplified) -> API response(normalized) -> Frontend(formatted)
 */



/**
 * --------------------------------------------------
 * BACKEND DTO TYPES (matches artifact_dto.py)
 * _-_-----------------------------------------------
 */

/**
 * Single artifact as returned by the backend DTO
 * @typedef {Object} ArtifactDTO
 * @property {number} id
 * @property {string} name
 * @property {string|null} description
 * @property {string|null} format - Format name (e.g., "Painting")
 * @property {string|null} location - Location name (e.g., "Museum")
 * @property {string[]} creators - Array of creator names
 * @property {string[]} materials - Array of material names
 * @property {string[]} tags - Array of tag names
 * @property {string[]} images - Array of image URLs
 */

/**
 * --------------------------------------------------------
 * API RESPONSE TYPES (matches api.js normalizeResponse)
 * --------------------------------------------------------
 *
 */

/**
 * Pagination metadata from API responses
 * @typedef {Object} PaginationMeta
 * @property {number|null} page - Current page number
 * @property {number|null} per_page - Items per page
 * @property {number|null} total - Total number of items
 * @property {number|null} total_pages - Total number of pages
 */

/**
 * Normalized list response (for fetchAllArtifacts, searchArtifacts)
 * @typedef {Object} ArtifactListResponse
 * @property {ArtifactDTO[]} items - Array of artifacts
 * @property {PaginationMeta} meta - Pagination metadata
 */

/**
 * Normalized single item response (for getArtifactById)
 * @typedef {Object} ArtifactItemResponse
 * @property {ArtifactDTO} item - Single artifact
 * @property {Object} meta - Metadata (usually empty object)
 */

/**
 * ----------------------------------------------------------------------------
 * FORMATTED ARTIFACT FOR DISPLAY (frontend convertion)
 * ----------------------------------------------------------------------------
 */

/**
 * Artifact formatted for display in UI components
 * Flattens arrays into comma-separated strings for easier rendering
 * 
 * @typedef {Object} FormattedArtifact
 * @property {number} id
 * @property {string} name
 * @property {string} description
 * @property {string} format - Format name
 * @property {string} location - Location name
 * @property {string} creators - Comma-separated creator names
 * @property {string} materials - Comma-separated material names
 * @property {string[]} tags - Array of tag names (kept as array for filtering)
 * @property {string|null} primaryImage - First image URL or null
 * @property {string|null} thumbnailUrl - Generated thumbnail URL
 * @property {string[]} allImages - All image URLs
 */

/**
 * -----------------------------------------------------------------------------
 * RESPONSE TYPE CONSTANTS
 * -----------------------------------------------------------------------------
 */

export const ResponseTypes = {
    ARTIFACT: 'ARTIFACT',           // Single artifact (ArtifactItemResponse)
    ARTIFACT_LIST: 'ARTIFACT_LIST', // Multiple artifacts (ArtifactListResponse)
    SEARCH_RESULTS: 'SEARCH_RESULTS', // Search results (ArtifactListResponse)
}

/**
 * -----------------------------------------------------------------------------
 * ARTIFACT FORMATTER
 * -----------------------------------------------------------------------------
 */

export const ArtifactFormatter = {
    /**
     * Format a single artifact DTO for display in UI
     * Transforms backend DTO structure into a flattened, UI-friendly format
     * 
     * @param {ArtifactDTO} artifact - Raw artifact from backend DTO
     * @returns {FormattedArtifact}
     */
    formatForDisplay(artifact = {}) {
        const {
            id = null,
            name = "",
            description = "",
            format = "",
            location = "",
            creators = [],
            materials = [],
            tags = [],
            images = [],
        } = artifact;

        // Join arrays into comma-separated strings for display
        const creatorsStr = Array.isArray(creators) ? creators.join(", ") : "";
        const materialsStr = Array.isArray(materials) ? materials.join(", ") : "";
        
        // Keep tags as array for filtering/badges
        const tagsArray = Array.isArray(tags) ? tags : [];
        
        // Get primary image (first in array)
        const primaryImage = Array.isArray(images) && images.length > 0 
            ? images[0] //grabs the first url 
            : null;

        /**
         * Generate thumbnail URL from image URL
         * @param {string|null} url - Original image URL
         * @returns {string|null}
         */
        const makeThumb = (url) => {
            if (!url) return null;
            
            try {
                const hasQuery = url.includes("?");
                const separator = hasQuery ? "&" : "?";
                return `${url}${separator}size=thumb`;
            } catch (err) {
                console.error("Error generating thumbnail:", err);
                return null;
            }
        };

        const thumbnailUrl = makeThumb(primaryImage);

        return {
            id,
            name,
            description,
            format,
            location,
            creators: creatorsStr,
            materials: materialsStr,
            tags: tagsArray,
            primaryImage,
            thumbnailUrl,
            allImages: Array.isArray(images) ? images : [],
        };
    },






    
    /**
     * Format multiple artifacts for display
     * @param {ArtifactDTO[]} artifacts - Array of raw artifacts
     * @returns {FormattedArtifact[]}
     */
    formatList(artifacts = []) {
        if (!Array.isArray(artifacts)) {
            console.warn("formatList received non-array:", artifacts);
            return [];
        }
        return artifacts.map(artifact => this.formatForDisplay(artifact));
    },

    /**
     * Format normalized API list response
     * @param {ArtifactListResponse} response - Normalized API response
     * @returns {{ items: FormattedArtifact[], meta: PaginationMeta }}
     */
    formatListResponse(response) {
        const { items = [], meta = {} } = response;
        return {
            items: this.formatList(items),
            meta,
        };
    },

    /**
     * Format normalized API single item response
     * @param {ArtifactItemResponse} response - Normalized API response
     * @returns {{ item: FormattedArtifact, meta: Object }}
     */
    formatItemResponse(response) {
        const { item = null, meta = {} } = response;
        return {
            item: item ? this.formatForDisplay(item) : null,
            meta,
        };
    },
};