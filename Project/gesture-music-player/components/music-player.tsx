"use client"

import { useState, useRef, useEffect } from "react"
import { Slider } from "@/components/ui/slider"
import { Button } from "@/components/ui/button"
import { usePlaylist } from "./playlist-context"
import { Play, Pause, SkipBack, SkipForward, Volume2, VolumeX, Music } from "lucide-react"

export function MusicPlayer() {
  const { currentSong, isPlaying, playPause, nextSong, prevSong, songs, setCurrentSong } = usePlaylist()

  const [volume, setVolume] = useState(80)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [isMuted, setIsMuted] = useState(false)

  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.play().catch((error) => {
          console.error("Error playing audio:", error)
        })
      } else {
        audioRef.current.pause()
      }
    }
  }, [isPlaying, currentSong])

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume / 100
    }
  }, [volume])

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime)
    }
  }

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration)
    }
  }

  const handleSeek = (value: number[]) => {
    if (audioRef.current) {
      audioRef.current.currentTime = value[0]
      setCurrentTime(value[0])
    }
  }

  const toggleMute = () => {
    if (audioRef.current) {
      audioRef.current.muted = !isMuted
      setIsMuted(!isMuted)
    }
  }

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`
  }

  return (
    <div className="flex flex-col">
      <audio
        ref={audioRef}
        src={currentSong?.url || "/sample-audio.mp3"}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={nextSong}
      />

      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <div className="w-16 h-16 bg-slate-700 rounded-md flex items-center justify-center mr-4">
            <Music className="h-8 w-8 text-slate-400" />
          </div>
          <div>
            <h3 className="font-medium text-lg">{currentSong?.title || "No song selected"}</h3>
            <p className="text-slate-400">{currentSong?.artist || "Unknown artist"}</p>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <div className="flex items-center mb-2">
          <span className="text-xs text-slate-400 w-10">{formatTime(currentTime)}</span>
          <Slider value={[currentTime]} max={duration || 100} step={0.1} onValueChange={handleSeek} className="mx-2" />
          <span className="text-xs text-slate-400 w-10">{formatTime(duration)}</span>
        </div>
      </div>

      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="icon" onClick={toggleMute}>
            {isMuted ? <VolumeX className="h-5 w-5" /> : <Volume2 className="h-5 w-5" />}
          </Button>
          <Slider value={[volume]} max={100} step={1} onValueChange={(value) => setVolume(value[0])} className="w-24" />
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="icon" onClick={prevSong}>
            <SkipBack className="h-5 w-5" />
          </Button>
          <Button variant="default" size="icon" className="h-12 w-12 rounded-full" onClick={playPause}>
            {isPlaying ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
          </Button>
          <Button variant="ghost" size="icon" onClick={nextSong}>
            <SkipForward className="h-5 w-5" />
          </Button>
        </div>
        <div className="w-[88px]"></div> {/* Spacer to balance the layout */}
      </div>

      <div className="mt-8">
        <h3 className="font-medium mb-3">Playlist</h3>
        <div className="max-h-48 overflow-y-auto pr-2">
          {songs.map((song) => (
            <div
              key={song.id}
              className={`flex items-center p-2 rounded-md mb-2 cursor-pointer ${
                currentSong?.id === song.id ? "bg-slate-700" : "hover:bg-slate-700"
              }`}
              onClick={() => setCurrentSong(song)}
            >
              <Music className="h-4 w-4 mr-3 text-slate-400" />
              <div>
                <p className="font-medium text-sm">{song.title}</p>
                <p className="text-xs text-slate-400">{song.artist}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

