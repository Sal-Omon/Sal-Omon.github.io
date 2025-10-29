import React from 'react';
import "./tiles.css";

export default function Tiles({ opera }) { //opera destructuring is used to extract the opera object from props 
    // const data = Array.isArray(opera ? opera : [opera]);

    return (
        <div className="tiles-container">
            <div key={opera.id} className="tile1">
                <img src={opera.img_url} alt={opera.title} />
                <p>prima colonna</p>
                <p>{opera.title}</p>
                <p>{opera.description}</p>
                <span>{opera.creation_date}</span>
            </div>

            <div key={opera.id} className="tile2">
                <img src={opera.img_url} alt={opera.title} />
                <p>seconda colonna</p>
                <p>{opera.title}</p>
                <p>{opera.description}</p>
                <span>{opera.creation_date}</span>
            </div>

            <div key={opera.id} className="tile3">
                <img src={opera.img_url} alt={opera.title} />
                <p>terza colonna</p>
                <p>{opera.title}</p>
                <p>{opera.description}</p>
                <span>{opera.creation_date}</span>
            </div>
        </div>
    
    );
};


