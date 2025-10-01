"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

export type Song = {
  id: string
  title: string
  artist: string
  url: string
}

type PlaylistContextType = {
  songs: Song[]
  currentSong: Song | null
  isPlaying: boolean
  addSong: (song: Song) => void
  removeSong: (id: string) => void
  playPause: () => void
  nextSong: () => void
  prevSong: () => void
  setCurrentSong: (song: Song) => void
}

const PlaylistContext = createContext<PlaylistContextType | undefined>(undefined)

const defaultSongs: Song[] = [
  {
    id: "1",
    title: "Summertime",
    artist: "Cinematic Orchestra",
    url: "/sample-audio.mp3",
  },
  {
    id: "2",
    title: "Midnight Jazz",
    artist: "Blue Note Ensemble",
    url: "/sample-audio.mp3",
  },
  {
    id: "3",
    title: "Ocean Waves",
    artist: "Ambient Sounds",
    url: "/sample-audio.mp3",
  },
]

export const PlaylistProvider = ({ children }: { children: ReactNode }) => {
  const [songs, setSongs] = useState<Song[]>(defaultSongs)
  const [currentSong, setCurrentSong] = useState<Song | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)

  useEffect(() => {
    // Initialize with the first song
    if (songs.length > 0 && !currentSong) {
      setCurrentSong(songs[0])
    }
  }, [songs, currentSong])

  const addSong = (song: Song) => {
    setSongs([...songs, song])
  }

  const removeSong = (id: string) => {
    setSongs(songs.filter((song) => song.id !== id))
    if (currentSong?.id === id) {
      setCurrentSong(songs.length > 1 ? songs[0] : null)
    }
  }

  const playPause = () => {
    setIsPlaying(!isPlaying)
  }

  const nextSong = () => {
    if (!currentSong || songs.length <= 1) return

    const currentIndex = songs.findIndex((song) => song.id === currentSong.id)
    const nextIndex = (currentIndex + 1) % songs.length
    setCurrentSong(songs[nextIndex])
  }

  const prevSong = () => {
    if (!currentSong || songs.length <= 1) return

    const currentIndex = songs.findIndex((song) => song.id === currentSong.id)
    const prevIndex = (currentIndex - 1 + songs.length) % songs.length
    setCurrentSong(songs[prevIndex])
  }

  return (
    <PlaylistContext.Provider
      value={{
        songs,
        currentSong,
        isPlaying,
        addSong,
        removeSong,
        playPause,
        nextSong,
        prevSong,
        setCurrentSong,
      }}
    >
      {children}
    </PlaylistContext.Provider>
  )
}

export const usePlaylist = () => {
  const context = useContext(PlaylistContext)
  if (context === undefined) {
    throw new Error("usePlaylist must be used within a PlaylistProvider")
  }
  return context
}

