import "./App.css";
import Header from "./components/Header/header.jsx";
import Searchbar from "./searchbar/searchbar.jsx";
import HeroSection from "./text/HeroSection.jsx";
import Tiles from "./Categ.Esplorazione/tiles.jsx";

import { fetchSuggestions } from './utils/api.js';
import { useState, useEffect } from "react";

function App() {
  const [opera, setOpera] = useState([]); // Initialize with an empty array
  const [loading, setLoading] = useState(true);
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

  //Mapping over the Array: The operas.map() method iterates over each opera object. 
  // Each object’s properties are accessible using dot notation.
  if (loading) return <div>Loading</div>;
  if (error) return <div>Error occurred, {error}</div>;
  if (!opera.length) return <div>No results found, wait for it...NAH</div>;

  return (
    <>
      <div>

        <Header />
      </div>
      <div>
        <HeroSection titolo="Esplora il patrimonio culturale"
          sottotitolo="Accedi alla conoscenza attraverso intelligenza artificiale e ricerca avanzata"
          sfondo="./src/assets/img1.webp" />
      </div>
      <video controls>
        <source src="./src/assets/video.mp4" type="video/mp4" />
        <source src="./src/assets/video.webm" type="video/webm" />
        <source src="./src/assets/music/alcocerGibran.mp3" type="audio/mpeg" />
        <div>
          <Searchbar
            SearchIcon="./src/assets/search.png"
            SearchImg="./src/assets/image2.png" />
        </div>

      </video>
      <br />

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
