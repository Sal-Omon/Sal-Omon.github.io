import { quickSearch, searchArtifacts } from "./api";


/**
 * TypeScript-like tyoe definition for artifact filters
 * @typeof {Object} ArtifactFilter
 * @property {number|string} [id] - Artifact ID
 * @property {string} [name] - Artifact name
 * @property {string} [creator] - Artifact creator
 * @property {string} [format] - Artifact format
 * @property {string} [location] - Artifact location
 * @property {string} [material] - Artifact material
 * @property {string|string[]} [tag] - Artifact tag
 * @property {string[]} [images] - Artifact img
 * @property {string} [q] - Text search query 
 * 
 */



const ArtifactFilterBuilder = {
    //Basic filter definition - Each method creates a single filter
    //Match your backend routes filters exactly
    filters: {
        //Each filter function takes a value and returns an object with that filter
        id: (value) => ({ id: value }),
        name: (value) => ({ name: value }),
        creator: (value) => ({ creator: value }),
        format: (value) => ({ format: value }),
        location: (value) => ({ location: value }),
        material: (value) => ({ material: value }),
        tag: (value) => ({ tag: Array.isArray(value) ? value.join(',') : value }),//tag filter handles both single string and array input 
        q: (value) => ({ q: value })
    },

    //Common combination of filters for frequent use cases
    common: {
        /**
         * Quick search filter creation
         *@param {string} searchTerm - Search term 
         *@returns {ArtifactFilter}
         */
        quickSearch: (searchTerm) => ({ q: searchTerm }),
        /**
         * Location and material combination filter
         * @param {string} location - Artifact location
         * @param {string} [material] - Artifact material
         * @returns {ArtifactFilter}
         */
        byLocationAndMaterial: (location, material) => ({
            location,
            ...(material && { material })
        }),

        /**
         * Multiple tags filter
         * @param {string[]} tags  - Array of tags
         * @returns {ArtifactFilter}
         */
        byTags: (tags) => ({
            tag: Array.isArray(tags) ? tags.join(',') : tags || "",
        }),

        /**
         * 
         * @param {string} name - Artifact name
         * @param {string} format - Artifact format
         * @returns {ArtifactFilter}
         */
        byNameAndFormat: (name, format) => ({
            name,
            format,
        }),

        /**
         * Filter by creator and material
         */

        byPeriodAndLocation: (period, location) => ({
            period,
            location,
        }),

    },

    /**
     * Combine multiple filters safely
     * @param {...Object} filters - Filter objects to combine
     * @returns {ArtifactFilter}
    */

    //Combinee multiple filters 
    create: function (...filters) {
        return filters.reduce((acc, filter) => {
            if (!filter) return acc;

            //Convert function filters to objects if needed
            const raw = typeof filter === 'function' ? filter() : filter;
            const filterObj = { ...raw }; //Create a clean copy


            //Remove empty values
            Object.keys(filterObj).forEach(key => {
                const val = filterObj[key];
                if (
                    val === undefined ||
                    val === null ||
                    (typeof val === "string" && val.trim() === "") ||
                    (Array.isArray(val) && val.length === 0)
                ) {
                    delete filterObj[key];
                }
            });
            //only merge if there are actual values
            if (Object.keys(filterObj).length === 0) return acc;

            //Merge with accumulated filters
            return { ...acc, ...filterObj };

        }, {});
    },

    /**
     * Create filter builder instance for chaining
     * @returns {Object} Builder object with chainable methods
    */

    builder() {
        const filters = {};

        const api = {
            //Chain methods for building filters
            withId: (id) => {
                if (id !== undefined && id !== null && id !== "") filters.id = id;
                return api;
            },
            withName: (name) => {
                if (name) filters.name = name;
                return api;
            },
            withCreator: (creator) => {
                if (creator) filters.creator = creator;
                return api;
            },
            withLocation: (location) => {
                if (location) filters.location = location;
                return api;
            },
            withMaterial: (material) => {
                if (material) filters.material = material;
                return api;
            },
            withTags: (tags) => {
                if (tags && tags.length) filters.tag = tags.join(',');
                return api;
            },
            withSearchQuery: (query) => {
                if (query) filters.q = query;
                return api;
            },
            build() {
                return Object.keys(filters).reduce((out, k) => {
                    const v = filters[k];
                    if (
                        v === undefined ||
                        v === null ||
                        (typeof v === "string" && v.trim() === "") ||
                        (Array.isArray(v) && v.length === 0)
                    ) {
                        return out;
                    }
                    out[k] = v;
                    return out;
                }, {});
            },
        };
        return api;
    },

};


//---------------------------------------------------------
//Documentation through code - template for complex queries
//---------------------------------------------------------
export const FilterExamples = {
    // 1. Documentation through examples
    basic: () => {
        return ArtifactFilterBuilder.create(
            ArtifactFilterBuilder.filters.q("renaissance")  // Shows how to use basic search
        );
    },

    // 2. Template for common scenarios
    advanced: () => {
        return ArtifactFilterBuilder.create(
            ArtifactFilterBuilder.filters.location("Florence"),
            ArtifactFilterBuilder.filters.material("marble"),
            ArtifactFilterBuilder.common.byPeriodAndLocation("Renaissance", "Italy")
        );
    },

    // 3. Shows different filter creation patterns
    withBuilder: () => {
        return ArtifactFilterBuilder.builder()
            .withLocation("Rome")
            .withMaterial("marble")
            .withTags(["ancient", "sculpture"])
            .build();
    }
};

