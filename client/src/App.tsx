import { FormEvent, useState } from 'react'

import { fetchEventSource } from '@microsoft/fetch-event-source';
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
            setSpotifySongs(songs?.songs)
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
  
    async function handleSync(e: MouseEvent) {
      e.preventDefault()

      const body = spotifySongs.map((song) => {
        return {
          song_id: song.song_id,
          name: song.name,
          artist: song.artist,
        }  
      })

      const response = await fetch("http://localhost:8000/youtube-music/sync", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(body)
      })

      if (response.ok) {
        const message = await response.json()
        console.log(message)
        await fetchEventSource('http://localhost:8000/sync-status', {
          onmessage(ev) {
            const rawData = ev.data
            const formatted = rawData.replace(/'/g, '"')
            const data = JSON.parse(formatted)
            const updatedState = spotifySongs.map((song) => {
              if (song.song_id == data['song_id']) {
                song.found = Boolean(data['found'])
                song.liked = Boolean(data['liked'])
              }
              return song
            })
            setSpotifySongs(updatedState)
          }
        });
      }
    }

    return (
        <>
            <h1>Spotify YouTubeMusic Sync</h1>
            <button onClick={setAuth}>Auth Spotify</button>
            <button onClick={handleSync}>Sync</button>)
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
                    return <SpotifySong name={song.name} found={song.found} liked={song.liked}/>
                })}
            </div>
        </>
    )
}

export default App
