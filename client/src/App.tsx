import { FormEvent, useState } from 'react'

import SpotifySong from './components/SpotifySong'

function App() {
    const [ playlistId, setPlaylistId ] = useState<string | undefined>(undefined)
    const [ spotifySongs, setSpotifySongs ] = useState([])

    async function handleSubmit(e: FormEvent) {
        e.preventDefault()
        const response = await fetch(`http://localhost:8000/spotify/playlists/${playlistId}/songs`, {
            method: 'GET',
            credentials: 'include'
        })
        if (response.ok) {
            const songs = await response.json()
            setSpotifySongs(songs)
        }
    }

    async function setAuth() {
        const response = await fetch("http://localhost:8000/auth/access-token", {
            method: 'POST',
            credentials: 'include',
        })
        if (response.ok) {
            console.log("authenticated")
        }
    }
    
    return (
        <>
            <h1>Spotify YouTubeMusic Sync</h1>
            <button onClick={setAuth}>Auth Spotify</button>
            <form method="POST" onSubmit={handleSubmit}>
                <input
                    value={playlistId}
                    type="text"
                    name='spotifyPlaylistId'
                    placeholder='Playlist ID'
                    onChange={(e) => setPlaylistId(e.target.value) }
                />
                <button>Fetch Songs</button>
            </form>
            <hr />
            <div>
                {spotifySongs?.map((song) => {
                    return <SpotifySong name={song.name} found liked />
                })}
            </div>
        </>
    )
}

export default App
