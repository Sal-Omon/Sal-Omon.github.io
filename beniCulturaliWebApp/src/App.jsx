import "./App.css";
import Header from "./components/Header/header.jsx";
import HeroSection from "./components/text/HeroSection.jsx";
import Tiles from "./components/Categ.Esplorazione/tiles.jsx";
import Searchbar from "./components/searchbar/searchbar.jsx";

import { fetchSuggestions } from './utils/api.js';
import { fetchSearch } from './utils/api.js';
import { useState, useEffect } from "react";

function App() {
  const [opera, setOpera] = useState([]); // Initialize with an empty array
  const [loading, setLoading] = useState(true); // This state will track if the data is still being fetched
  const [error, setError] = useState(null);

  //Fetching the Data: When the component mounts, 
  //useEffect triggers the loadOperas function which calls your API service and sets the JSON data into the operas state.



  useEffect(() => { //fetching data on component mount
    const loadSuggestions = async () => {
      try {
        const suggestions = await fetchSuggestions();
        setOpera(suggestions);
      } catch (error) {
        setError(error.message || "An error occurred while fetching data");
      } finally {
        setLoading(false);
      }
    };
    loadSuggestions();
  }, []);

  useEffect(() => {
    const loadSearch = async () => {
      try {
        const lastSearch = await fetchSearch();
        setOpera(lastSearch);
      } catch (error) {
        setError(error.message || "An error occurred while fetching search data");
      }
      finally {
        setLoading(false); // Ensure loading is set to false after fetching search data
      }
    };
    loadSearch();
  }, []); // This effect runs whenever the opera state changes, allowing you to perform actions based on the updated data.



  //Mapping over the Array: The operas.map() method iterates over each opera object. 
  // Each object’s properties are accessible using dot notation.
  let content;
  if (loading) {
    content = <div className="loading">Loading...</div>;
  } else if (error) {
    content = <div className="error">Error: {error}</div>;
  } else if (!opera.length) {
    content = <div className="no-results">No results found...NAH</div>;
  }


  return (
    <>
      <div>
        <p>{opera.length} risultati trovati</p>
        <Header />
      </div>
      <div className="hero-section">
        <HeroSection titolo="Esplora il patrimonio culturale"
          sottotitolo="Accedi alla conoscenza attraverso intelligenza artificiale e ricerca avanzata"
          sfondo="./src/assets/imgValledeiTempli.webp" />
      </div>
      <video controls>
        <source src="./src/assets/video.mp4" type="video/mp4" />
        <source src="./src/assets/video.webm" type="video/webm" />
        <source src="./src/assets/music/alcocerGibran.mp3" type="audio/mpeg" />
      </video>
      <div>
        <Searchbar
          SearchIcon="./src/assets/search.png"
          SearchImg="./src/assets/image2.png" />
      </div>
      <br />

      {content ? content : <Tiles opera={opera} />}
      <div>
        <Tiles opera={opera} />
      </div>
      <div>
        <footer className="footer" style={{ marginTop: "100px" }}>
          <p style={{ marginBottom: "10px" }}>© 2023 beniCulturaliWebApp. All rights reserved.</p>
        </footer>
      </div>
    </>
  )
}


export default App;
