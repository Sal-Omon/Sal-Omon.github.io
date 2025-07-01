import { useState } from "react";
import "./searchbar.css";


export default function Searchbar({ SearchIcon, SearchImg }) {
    const [input, setInput] = useState("");
    const [result, setResult] = useState();


    function handleInputChanges(e) {
        setInput(e.target.value);
    }


    function handleTextualSearch() {
        const found = opere.find(elem =>
            elem.name.toLowerCase().includes(input.toLowerCase())

        );
        setInput(found ? found.name : "No results are found prick")
    }



    return (
        <form action="risultatidiricerca.html" className="form-searchbar">
            <label htmlFor="textinput" className="searchbar-label" >Ricerca testuale</label>
            <input
                value={input}
                type="text"
                id="textinput"
                className="searchbarInput"
                onChange={handleInputChanges}
            />

            <div id="icone">
                <button type="button" id="iconadiricerca" aria-label="Cerca" onClick={handleTextualSearch}>
                    <img src={SearchIcon} alt="iconadiricerca" />
                </button>

                <button type="button" id="iconadiricercaimg" aria-label="Carica immagine">
                    <img src={SearchImg} alt="iconadiricercaimmagini" />
                </button>
            </div>
            {result && <div className="search-result">{result}</div>}
        </form >
    );
}