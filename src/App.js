// Filename - App.js
// Importing modules
import React, { useState } from "react";
import "./App.css";
 
function App() {
    // usestate for setting a javascript
    // object for storing and using data
    const [data, setdata] = useState({
        most_hated: "",
        hate_value: 0,
        games_surveyed: 0,
    });
    
    const [game_name, setname] = useState("");
    const [game_tag, settag] = useState("");
    const [games, setgames] = useState("");
    const [role, setrole] = useState("");
    const [queue, setqueue] = useState("");
    const [gamesFaced, setgamesfaced] = useState("");
 
        // Using useEffect for single rendering

        function handleNameChange(e) {
            setname(e.target.value)
            console.log(`input changed..${e.target.value}`)
        }

        function handleTagChange(f) {
            settag(f.target.value)
            console.log(`input changed..${f.target.value}`)
        }

        function handleGamesChange(g) {
            setgames(g.target.value)
            console.log(`input changed..${g.target.value}`)
        }

        function handleRoleChange(h) {
            setrole(h.target.value)
            console.log(`input changed..${h.target.value}`)
        }

        function handleQueueChange(i) {
            setqueue(i.target.value)
            console.log(`input changed..${i.target.value}`)
        }
        
        function handleFacedChange(j) {
            setgamesfaced(j.target.value)
            console.log(`input changed..${j.target.value}`)
        }

        function handleSubmit(e) {
            e.preventDefault();
            setdata({
                most_hated: "loading...",
                hate_value: 0,
                games_surveyed: 0,
            })
            let Data = new FormData()
            Data.set("game_name", game_name)
            Data.set("game_tag", game_tag)
            Data.set("role", role)
            Data.set("queue", queue)
            Data.set("games", games)
            Data.set("gamesFaced", gamesFaced)
            // Using fetch to fetch the api from 
            // flask server it will be redirected to proxy
            fetch("/data", {
                "method": "POST",
                "body": Data
            }).then((res) => res.json().then((data) => {
                    // Setting a data from api
                    setdata({
                        most_hated: data.Most_Hated,
                        hate_value: data.Hate_Value,
                        games_surveyed: data.Games_Surveyed,
                    });
                })
            );
        }
    return (
        <div className="App">
            <header className="App-header">
                <h1>Champion Hatred Calculator</h1>
                <form onSubmit={handleSubmit}>
                    <label>
                        Name: 
                        <input 
                            onChange={ handleNameChange } 
                            text="text" 
                            name="name"
                            value={game_name}
                            placeholder="Game Name" 
                        />
                    </label> 
                    <label>
                        Tag:   
                        <input 
                            onChange={ handleTagChange } 
                            text="text" 
                            name="tag"
                            value={game_tag}
                            placeholder="Tag (ex. NA1)" 
                        />
                    </label>
                    <br />
                    <label for="Role">
                        Select a Role:
                        <select name="Role" id="Role" onChange={ handleRoleChange } value={role}>
                            <option value="ALL">All</option>
                            <option value="TOP">Top</option>
                            <option value="JUNGLE">Jungle</option>
                            <option value="MID">Mid</option>
                            <option value="BOTTOM">Bottom</option>
                            <option value="UTILITY">Support</option>
                        </select>
                    </label> 
                    <label>
                        Queue:
                        <select name="Queue" id="Queue" onChange={ handleQueueChange } value={queue}>
                            <option value='420'>Ranked Solo Duo</option>
                            <option value='440'>Ranked Flex</option>
                            <option value="400">Normal Draft</option>
                        </select>
                    </label> 
                    <label>
                        Number of Games:   
                        <input 
                            onChange={ handleGamesChange } 
                            text="text" 
                            name="games"
                            value={games}
                            placeholder="Number of Games" 
                        />
                    </label>
                    <label>
                        Minimum Games Against:   
                        <input 
                            onChange={ handleFacedChange } 
                            text="text" 
                            name="gamesFaced"
                            value={gamesFaced}
                            placeholder="Minimum Games Against" 
                        />
                    </label>
                    <br />
                    <button 
                        type = "submit">
                            Submit
                    </button>
                </form>
                {/* <p>Game Name: {game_name}</p>
                Tag: {game_tag} */}
                <b />
                <p>{"You Hate: " + data.most_hated}</p>
                <p>{"Hate Value: " + data.hate_value}</p>
                <p>{"Games Surveyed: " + data.games_surveyed}</p>
            </header>
        </div>
    );
}
 
export default App;