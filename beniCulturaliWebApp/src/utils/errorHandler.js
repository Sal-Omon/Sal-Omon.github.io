export const ArtifactErrors = {
    SEARCH_FAILED: 'SEARCH_FAILED',
    FETCH_FAILED: 'FETCH_FAILED',
    INVALID_FILTER: 'INVALID_FILTER',
    NETWORK_ERROR: 'NETWORK_ERROR',
    TIMEOUT_ERROR: 'TIMEOUT_ERROR',
    NOT_FOUND: 'NOT_FOUND',
    SERVER_ERROR: 'SERVER_ERROR',
    VALIDATION_ERROR: 'VALIDATION_ERROR',
    UNKNWON_ERROR: 'UNKNOWN_ERROR'
};

/**
 * Formatted error object
 * @typedef {Object} FormattedError
 * @property {string} type - Error type from ArtifactErrors
 * @property {string} message - User-friendly message in Italian
 * @property {string|null} details - Technical error details
 * @property {number|null} statusCode - HTTP status code if available
 * @property {boolean} isRetryable - Whether the operation can be retried
 */

//-------------------------------------------------------------------------
// ERROR MESSAGES MAPPING
//-------------------------------------------------------------------------

const ERROR_MESSAGES = {
    [ArtifactErrors.SEARCH_FAILED]: 'la ricerca non può essere completata.',
    [ArtifactErrors.FETCH_FAILED]: 'il recupero è fallito.',
    [ArtifactErrors.INVALID_FILTER]: 'il filtro fornito non è valido.',
    [ArtifactErrors.NETWORK_ERROR]: 'si è verificato un errore di rete.',
    [ArtifactErrors.TIMEOUT_ERROR]: 'la richiesta è scaduta.',
    [ArtifactErrors.NOT_FOUND]: 'l\'elemento richiesto non è stato trovato.',
    [ArtifactErrors.SERVER_ERROR]: 'si è verificato un errore del server.',
    [ArtifactErrors.VALIDATION_ERROR]: 'si è verificato un errore di convalida.',
    [ArtifactErrors.UNKNWON_ERROR]: 'si è verificato un errore imprevisto.'
};

//-------------------------------------------------------------------------
// ERROR DETECTION HELPERS
//-------------------------------------------------------------------------

/**
 * Check if error is a network error
 * @param {Error} error
 * @returns {boolean}
 */
function isNetworkError(error) {
    return (
        error.message.includes('Failed to fetch') ||
        error.message.includes('Network request failed') ||
        error.message.includes('NetworkError') ||
        error.name === 'NetworkError'
    )
}


/**
 * Check if error is timeout error
 * @param {Error} error
 * @returns {boolean}
 */
function isTimeoutError(error) {
    return (
        error.message.includes('timeout') ||
        error.message.includes('aborted') ||
        error.name === 'AbortError' ||
        error.name === 'TimeoutError'
    );
}

/**
 * Check if error is retryable (network/timeout errors usually are)
 * @param {string} errorType
 * @param {number|null} statusCode
 * @returns {boolean}
 */
function isRetryable(errorType, statusCode) {
    // Network errors and timeouts are retryable
    if (errorType === ArtifactErrors.NETWORK_ERROR ||
        errorType === ArtifactErrors.TIMEOUT_ERROR) {
        return true;
    }

    //server errrors are retryable
    if (statusCode && statusCode >= 500 && statusCode < 600) {
        return true;
    }

    if (statusCode === 429) {
        return true;
    }
    return false;
}

//-------------------------------------------------------------------------
// ERROR CLASSIFICATION
//-------------------------------------------------------------------------

/**
 * Classify error based on status code or error type
 * @param {Error} error
 * @param {number|null} statusCode
 * @returns {string} Error type from ArtifactErrors
 */
function classifyError(error, statusCode = null) {
    //first check for network errors
    if (isNetworkError(error)) {
        return ArtifactErrors.NETWORK_ERROR;
    }

    if (isTimeoutError(error)) {
        return ArtifactErrors.TIMEOUT_ERROR;
    }
    //check validation errrors (from SearchParamsManager)
    if (error.message.includes('deve essere' ||
        error.message.includes('Contenuto mancante'))) {
        return ArtifactErrors.VALIDATION_ERROR;
    }
    //Classify by http status code
    if (statusCode) {
        if (statusCode === 404) return ArtifactErrors.NOT_FOUND;
        if (statusCode >= 400 && statusCode < 500) return ArtifactErrors.INVALID_FILTER;
        if (statusCode >= 500) return ArtifactErrors.SERVER_ERROR;
    }
    if (error.message.includes('search') || error.message.includes('ricerca')) {
        return ArtifactErrors.SEARCH_FAILED;
    }
    if (error.message.includes('fetch') || error.message.includes('load')) {
        return ArtifactErrors.FETCH_FAILED;
    }
    return ArtifactErrors.UNKNWON_ERROR;
}


/**
 * ----------------------------------------------
 * MAIN ERROR HANDLER
 * ----------------------------------------------
 */



/**
 *Format an artifact-related error with user-friendly messags
 *@param {string} type - from ArtifactError 
 *@param {Error} error - original error object
 *@param {number|null} [statusCode] 
 *@returns {FormattedError}
 * 
 *  
*/

export function handleArtifactError(type, error, statusCode = null) {
    const message = ERROR_MESSAGES[type] || ERROR_MESSAGES[ArtifactErrors.UNKNWON_ERROR];
    const details = error?.message || null;

    return {
        type,
        message,
        details,
        statusCode,
        isRetryable: isRetryable(type, statusCode)
    };
}

/**
 * Automatically detect and format any error
 * @param {Error} error - Error object
 * @param {number|null} [statusCode] - HTTP status code if available
 * @returns {FormattedError}
 */
export function formatArtifactError(error, statusCode = null) {
    //handle null /undefined errrors
    if (!error) {
        return handleArtifactError(
            ArtifactErrors.UNKNWON_ERROR,
            new Error('unknown error occurred'),
            statusCode
        )
    }
    const errorType = classifyError(error, statusCode);
    return handleArtifactError(errorType, error, statusCode);
}

/**
 * Format HTTP response errors (from api.js)
 * Extracts status code and creates formatted error
 * @param {Response} response - Fetch Response object
 * @param {string} [errorText] - Optional error text from response body
 * @returns {FormattedError}
 */
export function formatHTTPError(response, errorText = '') {
    const statusCode = response.status;
    const errorMessage = errorText || response.statusText || 'HTTP Error';
    const error = new Error(` HTTP ${statusCode}: ${errorMessage}`);

    return formatArtifactError(error, statusCode);
}

/**
 * ----------------------------------------------------------
 * ERROR LOGGING 
 * ----------------------------------------------------------
 * 
 */
/**
 * Log error with context for debugging
 * @param {FormattedError} formattedError
 * @param {string} [context] - Context where error occurred
 */
export function logArtifactError(formattedError, context = '') {
    const prefix = context ? [`${context}`] : '[ArtifactError]';

    console.error(`${prefix} ${formattedError.type}:`, {
        message: formattedError.message,
        details: formattedError.details,
        statusCode: formattedError.statusCode,
        isRetryable: formattedError.isRetryable
    });
}


/**
 * 
 * ---------------------------------------------------------
 * USER-Friendly error helpersssss
 */


/**
 * Get a user friendly saction suggestion based on error type
 * @param {FormattedError}
 * @returns {string}
 */

export function getErrorSuggestion(formattedError, ERROR_MESSAGES) {

    const suggestions = {
        [ArtifactErrors.NETWORK_ERROR]: 'Controlla la tua connessione internet e riprova',
        [ArtifactErrors.TIMEOUT_ERROR]: 'La richiesta sta impiegando troppo tempo. Riprova tra qualche istante',
        [ArtifactErrors.NOT_FOUND]: 'La risorsa richiesta non esiste',
        [ArtifactErrors.SERVER_ERROR]: 'Il server sta riscontrando problemi. Riprova più tardi',
        [ArtifactErrors.VALIDATION_ERROR]: 'Verifica i parametri di ricerca e riprova',
        [ArtifactErrors.INVALID_FILTER]: 'Alcuni filtri non sono validi. Modifica la ricerca',
        [ArtifactErrors.SEARCH_FAILED]: 'Prova a modificare i criteri di ricerca',
        [ArtifactErrors.FETCH_FAILED]: 'Impossibile caricare i dati. Riprova',
    };

    return suggestions[formattedError.type] || 'Riprova o contatti il supporto al numero 666-111-000'
}