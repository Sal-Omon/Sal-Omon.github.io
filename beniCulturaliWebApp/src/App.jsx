import React from "react";
import SearchBar from "./components/Search/Searchbar";
import HeroSection from "./components/Text/HeroSection";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import Tiles from "./components/CategoryTiles/Tiles";
import useSearch from "./hooks/useSearch";
import SearchResults from "./components/Search/SearchResults";

/**
 * 
 * @typedef {Object} SearchResults
 * @property {Array} items
 */
/**
 * 
 * @typedef {Object} SearchHookReturn 
 * @property {SearchResults} data
 * @property {boolean} isLoading
 * @property {Error|null} error
 * @property {string} searchTerm
 * @property {function(string): void} setSearchTerm
 * 
 */

function App() {
/**@type {SearchHookReturn} */

  const { data: SearchResults,
    isLoading,
    error,
    searchTerm,
    setSearchTerm
  } = useSearch();
  
  const artifact = SearchResults?.items || [];



  return (
    <div>
      <div className="app-container">
        <Header />
        <main>
          <div className="hero-section">
            <HeroSection titolo="Esplora il patrimonio culturale"
              sottotitolo="Accedi alla conoscenza attraverso intelligenza artificiale e ricerca avanzata"
              sfondo="src\assets\imgValledeiTempli.webp"
            />
          </div>
          <section className="search-section">
            <p>Test base is running!!!</p>
            //SearchBar not working
          </section>
        </main>
      </div>
    </div>
  );
}


export default App;