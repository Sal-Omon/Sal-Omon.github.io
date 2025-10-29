// api.js
const API_URL = import.meta.env.REACT_APP_API_URL ?? "/api";

/**
 * Fetch with timeout and combined cancellation support.
 * If the caller passes a signal, it is honored together with the internal timeout.
 *
 * @param {string} resource - URL string to fetch
 * @param {object} options - fetch options. Recognized keys: timeout (ms), signal (AbortSignal), method, headers, body
 * @returns {Promise<Response>}
 */


// a wrapper around fetch with configurable timeout, abortController, signal forwarding for external abort control
async function fetchWithTimeout(resource, { timeout = 8000,signal, ...options } = {}) {
  // controller used for the timeout (and for forwarding external aborts)
  const timeoutController = new AbortController();
  const finalSignal = timeoutController.signal;

  // If caller provided a signal, forward their abort to our timeout controller
  if (signal) {
    // If the external signal already aborted, propagate immediately
    if (signal.aborted) {
      timeoutController.abort();
    } else {
      const onAbort = () => timeoutController.abort();
      // attach once to avoid memory leaks (fires only one time)
      signal.addEventListener("abort", onAbort, { once: true });
    }
  }

  const id = setTimeout(() => timeoutController.abort(), timeout);

  try {
    // Use our timeout controller's signal so either external abort or timeout will stop the fetch
    const response = await fetch(resource, { ...options, signal: finalSignal });
    return response;
  } finally {
    clearTimeout(id);
  }
}

/**
 * Throws a descriptive Error for non-OK responses.
 * Returns parsed JSON (or null for 204 / non-JSON).
 *
 * @param {Response} response
 * @returns {Promise<any|null>}
 */

// handles response status and parsing 
async function handleResponse(response) {

  console.log(`API response status: ${response.status} for ${response.statusText}`);
  if (!response.ok) {
    // try to read body for additional details (best-effort)
    const errorText = await response.text().catch(() => "");
    console.error(`API error details: ${response.status} ${response.statusText}. Details:  ${errorText || "No details"}`);
    throw new Error(`HTTP ${response.status}: ${response.statusText}. ${errorText || "No details"}`);
  }

  // No content
  if (response.status === 204) {
    console.log("No content (204). Returning null.");
    return null;
  }


  // Safe parse — if body is empty/invalid JSON, return null
  return response.json().catch(() => {
    console.warn("Response body is not valid JSON or malformed. Returning null.");
    return null;
  });
}

/**
 * Lightweight normalizer for common API shapes.
 * - Lists: returns { items: [...], meta: {...} }
 * - Single resource: returns { item: {...}, meta: {...} }
 * - Fallback: wrap unknown value into { items: [value], meta: {} }
 *
 * @param {any} data
 * @returns {{ items?: any[], item?: any, meta: object }}
 */


//should match the DTOs from the backend
function normalizeResponse(data) {
  if (data == null) return { items: [], meta: {} };

  // If backend returned an array directly
  if (Array.isArray(data)) {
    return { items: data, meta: {} };
  }

  // Common list-like keys to detect paginated/list responses
  const listKeys = ["items", "results", "data"];
  for (const key of listKeys) {
    if (Array.isArray(data[key])) {
      const items = data[key];
      const meta =
        data.meta ??
        ({
          page: data.page ?? data.current_page ?? null,
          per_page: data.per_page ?? data.perPage ?? data.limit ?? null,
          total: data.total ?? data.total_count ?? data.count ?? null,
          total_pages: data.total_pages ?? data.totalPages ?? null,
        } ?? {});
      return { items, meta };
    }
  }

  // If backend explicitly returns a single resource under `.item`
  if (data.item && typeof data.item === "object") {
    return { item: data.item, meta: data.meta ?? {} };
  }

  // Heuristic: treat object with id-like property as single resource
  if (typeof data === "object" && (data.id || data._id || data.uuid || data.attributes)) {
    return { item: data, meta: {} };
  }

  // Fallback: wrap unknown object into items
  return { items: [data], meta: {} };
}

/**
 * Generic API request helper (GET/POST/PUT/DELETE).
 *
 * Options:
 *  - params: query params object
 *  - method: HTTP verb (default GET)
 *  - body: JS object to JSON.stringify (optional)
 *  - signal: AbortSignal (optional)
 *  - raw: if true, return backend JSON as-is (skip normalization)
 *  - headers: additional headers (optional)
 *  - timeout: ms (optional, default 8000)
 *
 * @param {string} endpoint
 * @param {object} opts
 * @returns {Promise<any>} normalized response by default, raw parsed JSON if opts.raw === true
 */



// function to make API requests, matches backend routes
async function apiRequest(endpoint, { params = {}, method = "GET", body, signal, raw = false, headers = {}, timeout = 8000 } = {}) {
  const url = new URL(`${API_URL}${endpoint}`);

  // Append query params (skip undefined/null/empty-string)
  Object.keys(params).forEach((k) => {
    const v = params[k];
    if (v !== undefined && v !== null && String(v).trim() !== "") {
      url.searchParams.append(k, v);
    }
  });

  // Prepare headers and body
  const finalHeaders = { ...headers };
  const options = { method, headers: finalHeaders, signal };
  const fullURL = url.toString();

  //----------------------------LOGS----------------------------
  console.log(`[API REQUEST] sending ${method} request to :${fullURL}`);
  if (Object.keys(params).length > 0) {
    console.log(`[API REQUEST] with query params: ${JSON.stringify(params)}`);
  }

  if (body !== undefined && body !== null) {
    finalHeaders["Content-Type"] = finalHeaders["Content-Type"] ?? "application/json";
    options.body = JSON.stringify(body);
    console.log(`[API REQUEST] with body: ${JSON.stringify(body).substring(0, 100)}`); // log first 100 chars of body
  }

  // fetchWithTimeout expects the timeout in its options
  const response = await fetchWithTimeout(url.toString(), { ...options, timeout });

  const parsed = await handleResponse(response);
  return raw ? parsed : normalizeResponse(parsed);
}

// ----- Domain functions (lightweight) -----

/**
 * Fetch a paginated list of artifacts (normalized).
 * @param {number} page
 * @param {number} per_page
 * @param {object} opts - optional fetch options (signal, raw, timeout, headers, method, body)
 */
export async function fetchAllArtifacts(page = 1, per_page = 20, opts = {}) {
  return apiRequest("/api/artifacts", { params: { page, per_page }, ...opts });
}

/**
 * Fetch a single artifact by id (normalized).
 * @param {string|number} artifactId
 * @param {object} opts
 */
export async function getArtifactById(artifactId, opts = {}) {
  return apiRequest(`/api/artifacts/${artifactId}`, { ...opts });
}

/**
 * Search artifacts with filters (normalized).
 * @param {object} filters
 * @param {number} page
 * @param {number} per_page
 * @param {object} opts
 */
export async function searchArtifacts(filters = {}, page = 1, per_page = 20, opts = {}) {
  return apiRequest("/api/artifacts/search", { params: { ...filters, page, per_page }, ...opts });
}

/**
 * Search artifacts by name (convenience wrapper).
 * @param {string} name
 * @param {number} page
 * @param {number} per_page
 * @param {object} opts
 */
export async function getArtifactsByName(name, page = 1, per_page = 20, opts = {}) {
  return searchArtifacts({ name }, page, per_page, opts);
}

/**
 * Quick text search (convenience wrapper).
 * @param {string} query
 * @param {number} page
 * @param {number} per_page
 * @param {object} opts
 */
export async function quickSearch(query, page = 1, per_page = 20, opts = {}) {
  return searchArtifacts({ q: query }, page, per_page, opts);
}
