import axios from 'axios';

const API_URL = 'http://localhost:5000/api/opere';

//axios automatically transform data to and from json
//with fetch you manually do it with response.json()

//if lastsearch is provided it will be used to filter correlated suggestions
export const fetchingSuggestion = async (lastsearch = null) => {
    try {
        const url = lastsearch ? `${API_URL}/suggestions?last_search=${encodeURIComponent(lastsearch)}` : `${API_URL}/suggestions`;
        const { data } = await axios.get(url);
        return data;
    } catch (error) {
        console.error("error fetching suggestions", error);
        return [];
    }
}

export const fetchingSearch = async () => { 
try{
    const url = `${API_URL}/suggestions?search=${encodeURIComponent(query)}`;
    const {data} = await axios.get(url);
    return data;

}catch(error){
    console.error("error fetching from the search-bar",error);
    return [];
}

}