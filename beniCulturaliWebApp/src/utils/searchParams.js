/**
 * ---------------------------
 * SEARCH PARAMETERS TYPES
 * ---------------------------
 *  * Search filters matching backend /artifacts/search endpoint
 * @typedef {Object} SearchFilters
 * @property {number|string|null} [id] - Artifact ID
 * @property {string|null} [name] - Artifact name (partial match)
 * @property {string|null} [creator] - Creator name
 * @property {string|null} [format] - Format name (e.g., "Painting")
 * @property {string|null} [location] - Location name
 * @property {string|null} [material] - Material name
 * @property {string|null} [conservationReport] - Conservation Report name
 * @property {string|null} [tag] - Tag name
 * @property {string|null} [q] - General text search query
 */

/**
 * Complete search parameters including pagination
 * @typedef {Object} SearchParams
 * @property {number} page - Page number (1-indexed)
 * @property {number} per_page - Items per page
 * @property {number|string|null} [id] - Artifact ID
 * @property {string|null} [name] - Artifact name
 * @property {string|null} [creator] - Creator name
 * @property {string|null} [format] - Format name
 * @property {string|null} [location] - Location name
 * @property {string|null} [material] - Material name
 * @property {string|null} [conservationReport] - Conservation Report name
 * @property {string|null} [tag] - Tag name
 * @property {string|null} [q] - Text search query
 */

/**
 * Validation error
 * @typedef {Object} ValidationError
 * @property {boolean} valid - Always false
 * @property {string} message - Error message in Italian
 * @property {string} field - Field that failed validation
 * 
 * 
 * 
 * 
 */

export class SearchParamsManager {
    /**
     * @params {Partial<SearchParams>} [initialParams={}] - initial parameters
     * 
     */

    constructor(initialParams = {}) {
        this.params = {
            page: 1,
            per_page: 20,
            ...this._validateInitialParams(initialParams)
        };
    }

    /**
     * 
     * Valid initial parameters
     * @private
     * @params {Object}
     * @returns {Object} validate params
     */

    _validateInitialParams(params) {
        const validated = {};

        if (params.page !== undefined) {
            const pageNum = Number(params.page);
            validated.page = isNan(pageNum) && pageNum > 0 ? pageNum : 1;
        }
        if (params.per_page !== undefined) {
            const perPageNum = Number(params.per_page);
            validated.per_page = isNaN(perPageNum) && perPageNum > 0 && perPageNum <= 100 ? perPageNum : 20;
        }

        const stringFields = ['name', 'description', 'creator', 'format', 'location', 'material', 'conservationReport', 'tag', 'q'];
        stringFields.forEach(field => {
            if (params[field] !== undefined && params[field] !== null) {
                const trimmed = String(params[field]).trim();
                if (trimmed) validated[field] = trimmed;
            }
        })

        if (params.id !== undefined && params.id !== null) {
            validated.id = params.id;
        }
        return validated;


    }
    /**
     * Validate a string parameter
     * @private
     * @param {any} value - Value to validate
     * @param {string} fieldName - Field name for error message
     * @returns {ValidationError|{valid: true, value: string}}
     */

    _validateString(value, fieldName) {
        if (value === null || value === undefined) {
            return { valid: true, value: null };
        }

        if (typeof value !== 'string') {
            return {
                valid: false,
                message: `${fieldName} deve essere una stringa`,
                field: fieldName
            };
        }

        const trimmed = value.trim();
        if (trimmed === '') {
            return {
                valid: false,
                message: "Contenuto mancante",
                field: fieldName
            };
        }

        return { valid: true, value: trimmed };
    }

    /**
     * Validate a number parameter
     * @private
     * @param {any} value - Value to validate
     * @param {string} fieldName - Field name for error message
     * @param {number} min - Minimum value
     * @param {number} [max] - Maximum value
     * @returns {ValidationError|{valid: true, value: number}}
     */

    _validateNumber(value, fieldName, min, max) {
        const num = Number(value);

        if (isNan(num)) {
            return {
                valid: false,
                message: `${fieldName} dev'essere un numero`,
                field: fieldName
            };
        }
        if (num < min) {
            return {
                valid: false,
                message: `${fieldName} deve essere maggiore o uguale a ${min}`,
                field: fieldName
            };
        }
        if (num > max) {
            return {
                valid: false,
                message: `${fieldName} deve essere minore o uguale a ${max}`,
                field: fieldName
            }
        }

        return { valid: true, value: num };
    }

    /**
     * Set general text search query
     * @param {string} query - Search query
     * @returns {SearchParamsManager} For chaining
     * @throws {Error} If validation fails
     */

    setTextSearch(query) {
        const validation = this._validateString(query, 'query');
        if (!validation.valid) {
            throw new Error(validation.message) // error message display
        }

        if (validation.value === null) {
            delete this.params.q;
        } else {
            this.params.q = validation.value;
        }

        return this;
    }

    /**
     * Set artifact ID filter
     * @param {number|string} id - Artifact ID
     * @returns {SearchParamsManager} For chaining
     */

    setId(id) {
        if (id === null || id === undefined) {
            delete this.params.id;
        } else {
            this.params.id = id;
        }
        return this;
    }


    /**
     * Set artifact name filter
     * @param {string} name - Artifact name
     * @returns {SearchParamsManager} For chaining
     * @throws {Error} If validation fails
     */

    setName(name) {
        const validation = this._validateString(name, 'name');
        if (!validation.valid) {
            throw new Error(validation.message);
        }

        if (validation.value === null) {
            delete this.params.name;
        } else {
            this.params.name = validation.value;
        }
        return this;

    }
    /**
     * Set creator filter
     * @param {string} creator - Creator name
     * @returns {SearchParamsManager} For chaining
     * @throws {Error} If validation fails
     */
    setCreator(creator) {
        const validation = this._validateString(creator, 'creator');
        if (!validation.valid) {
            throw new Error(validation.message);
        }

        if (validation.value === null) {
            delete this.params.creator;
        } else {
            this.params.creator = validation.value;
        }
        return this;
    }

    /**
     * Set format filter
     * @param {string} format - Format name
     * @returns {SearchParamsManager} For chaining
     * @throws {Error} If validation fails
     */
    setFormat(format) {
        const validation = this._validateString(format, 'format');
        if (!validation.valid) {
            throw new Error(validation.message);
        }

        if (validation.value === null) {
            delete this.params.format;
        } else {
            this.params.format = validation.value;
        }

        return this;
    }


    /**
     * Set Location filter
     * @param {string} location - Location name
     * @returns {SearchParamsManager} for chaining
     * @throws {Error} if validation fails
     */
    setLocation(location) {
        const validation = this._validateString(location, 'location');
        if (!validation.valid) {
            throw new Error(validation.message);
        }

        if (validation.value === null) {
            delete this.params.location;
        } else {
            this.params.location = validation.value;
        }

        return this;
    }

    /**
     * Set material filter
     * @param {string} material - Material name
     * @returns {SearchParamsManager} For chaining
     * @throws {Error} If validation fails
     */
    setMaterial(material) {
        const validation = this._validateString(material, 'material');

        if (!validation.valid) {
            throw new Error(validation.message);
        }

        if (validation.value === null) {
            delete this.params.material;
        } else {
            this.params.material = validation.value;
        }
        return this;
    }


    /**
     * 
     * set conservation reports
     * @param {string} conservationReport
     * @returns {SearchParamsManager} 
     * @throws {Error} if validation fails
     */
    setConservationReport(conservationReport) {
        const validation = this._validateString(conservationReport, 'conservationReport');

        if (!validation.valid) {
            throw new Error(validation.message);
        }

        if (validation.value === null) {
            delete this.params.conservationReport;
        } else {
            this.params.conservationReport = validation.value;
        }
        return this;

    }


    /**
 * Set tag filter
 * @param {string} tag - Tag name
 * @returns {SearchParamsManager} For chaining
 * @throws {Error} If validation fails
 */
    setTag(tag) {
        const validation = this._validateString(tag, 'tag');

        if (!validation.valid) {
            throw new Error(validation.message);
        }

        if (validation.value === null) {
            delete this.params.tag;
        } else {
            this.params.tag = validation.value;
        }
        return this;
    }

    /**
         * Set pagination parameters
         * @param {number} page - Page number (must be >= 1)
         * @param {number} [perPage] - Items per page (must be 1-100)
         * @returns {SearchParamsManager} For chaining
         * @throws {Error} If validation fails
         */

    setPagination(page, perPage) {
        const pageValidation = this._validateNumber(page, 'page', 1);

        if (!pageValidation.valid) {
            throw new Error(pageValidation.message);
        }
        this.params.page = pageValidation.value;

        if (perPage !== undefined) {
            const perPageValidation = this._validateNumber(perPage, 'per_page', 1, 100);
            if (!perPageValidation.valid) {
                throw new Error(perPageValidation.message);
            }
            this.params.per_page = perPageValidation.value;
        }
        return this;

    }

    /**
     * Set multiple filters at once
     * @param {Partial<SearchFilters>} filters - Filters object
     * @returns {SearchParamsManager} For chaining
     * @throws {Error} If any validation fails
     */
    setFilters(filters) {
        if (filters.id !== undefined) this.setId(filters.id);
        if (filters.name !== undefined) this.setName(filters.name);
        if (filters.creator !== undefined) this.setCreator(filters.creator);
        if (filters.format !== undefined) this.setFormat(filters.format);
        if (filters.location !== undefined) this.setLocation(filters.location);
        if (filters.material !== undefined) this.setMaterial(filters.material);
        if (filters.tag !== undefined) this.setTag(filters.tag);
        if (filters.conservationReport !== undefined) this.setConservationReport(filters.conservationReport);
        if (filters.q !== undefined) this.setTextSearch(filters.q);

        return this;
    }

    /**
     * Clear all filters (keeps pagination)
     * @returns {SearchParamsManager} For chaining
     */
    clearFilters() {
        const { page, per_page } = this.params;
        this.params = { page, per_page };
        return this;
    }

    /**
    * Clear a specific filter
    * @param {string} filterName - Name of filter to clear
    * @returns {SearchParamsManager} For chaining
    */
    clearFilter(filterName) {
        if (filterName !== 'page' && filterName !== 'per_page') {
            delete this.params[filterName];
        }
        return this;
    }

    /**
     * Reset to initial state (page 1, per_page 20, no filters)
     * @returns {SearchParamsManager} For chaining
     */
    reset() {
        this.params = { page: 1, per_page: 20 };
        return this;
    }

    /**
     * Check if any filters are active (excluding pagination)
     * @returns {boolean}
     */

    hasActiveFilters() {
        const filterKeys = Object.keys(this.params).filter(key =>
            key !== 'page' && key !== 'per_page'); //excludes page e per page
        return filterKeys.length > 0;
    }

    /**
     * Get active filter count (excluding pagination)
     * @returns {number}
     */
    getActiveFilterCount() {
        return Object.keys(this.params).filter(key =>
            key !== 'page' && key !== 'per_page'
        ).length;
    }

    /**
     * Build final parameters object (removes null/undefined values)
     * @returns {SearchParams}
     */
    build() {
        const cleaned = {};
        Object.keys(this.params).forEach(key => {
            const value = this.params[key];
            if (value !== undefined && value !== null) {
                cleaned[key] = value;
            }
        });
        return cleaned;
    }

    /**
     * Create URL search params string
     * @returns {string} Query string (e.g., "page=1&per_page=20&name=Mona")
     */
    toURLSearchParams() {
        const params = this.build();
        const searchParams = new URLSearchParams();

        Object.keys(params).forEach(key => {
            searchParams.append(key, String(params[key]));
        });
        return searchParams.toString();
    }

    /**
     * Create SearchParamsManager from URL search params
     * @param {string|URLSearchParams} searchParams - URL search params
     * @returns {SearchParamsManager}
     */
    static fromURLSearchParams(searchParams) {
        const params = {};
        const urlParams = typeof searchParams === 'string'
            ? new URLSearchParams(searchParams)
            : searchParams;

        urlParams.forEach((value, key) => {
            params[key] = value;
        });
        return new SearchParamsManager(params);
    }

    /**
     * Clone this manager
     * @returns {SearchParamsManager}
     */
    clone() {
        return new SearchParamsManager({ ...this.params });
    }

}
