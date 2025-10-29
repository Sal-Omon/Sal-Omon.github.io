import { useState } from "react";
import "./searchbar.css";

//onSearch parent Component/useSearch
export default function Searchbar({ searchTerm, onInputChange, isLoading, SearchIcon, SearchImg }) {
    const [error, setError] = useState(null); //validation error
    const [isFocused, SetIsFocused] = useState(false);


    const handleFocus = () => { SetIsFocused(true); }
    const handleBlur = () => { SetIsFocused(false); }


    function handleInputChanges(e) {
        const value = e.target.value;
        onInputChange(value); // Update parent state
        if (!value.trim()) {
            setError("Please enter a valid search term");
        } else {
            setError(null);
        }
    }


    function handleFormSubmit(e) {
        e.preventDefault();
        if (searchTerm.trim() === '') {
            setError("Please enter a valid search term");
        }
    }

    const suggestions = [];
    //single boolean variable
    const shouldShowSuggestion =
        (searchTerm && searchTerm.trim().length() > 0)
        && isFocused
        && (suggestions.length > 0);


    return (
        <form
            onSubmit={handleFormSubmit}
            className="form-searchbar">
            <label
                htmlFor="textinput"
                className="searchbar-label" >Ricerca testuale</label>
            <input
                value={searchTerm}
                type="text"
                id="textinput"
                className={`searchbarInput ${isFocused ? "focused" : ""} `}
                onChange={handleInputChanges}
                disabled={isLoading}
                placeholder={isLoading ? "Searching..." : "Search artifacts, creators, or tags..."}
                onFocus={handleFocus}
                onBlur={handleBlur}
            /> 


            <div id="icone">
                <button
                    type="submit"
                    id="iconadiricerca"
                    aria-label="Cerca"
                    onClick={handleTextualSearch}>
                    {isLoading ? (
                        <div
                            className="spinner"> </div>
                    ) : (
                        <img
                            src={SearchIcon}
                            alt="iconadiricerca" />
                    )}
                </button>
            </div>

            <button
                type="submit"
                id="iconadiricercaimg"
                aria-label="Carica immagine"
                className="btn-img-icon">
                <img
                    src={SearchImg}
                    alt="iconadiricercaimmagini" />
            </button>

            {error && <div
                className="search-error">{error}</div>}
        </form >
    );
}