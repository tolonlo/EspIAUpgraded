"use client"

import { useState, useEffect } from "react"
import { Play, Pause, SkipBack, SkipForward, Volume2, List, Hand } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function SpotifyGestureMockup() {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      if (isPlaying) {
        setCurrentTime((prevTime) => (prevTime + 1) % 100)
      }
    }, 1000)
    return () => clearInterval(timer)
  }, [isPlaying])

  return (
    <div className="flex h-screen bg-background text-foreground">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 p-6">
        <h2 className="text-2xl font-bold mb-4">Your Playlist</h2>
        <ul className="space-y-2 max-h-[calc(100vh-8rem)] overflow-y-auto playlist-scrollbar">
          {Array.from({ length: 20 }, (_, i) => `Song ${i + 1}`).map((song, index) => (
            <li key={index} className="flex items-center space-x-2 p-2 rounded hover:bg-gray-700 transition-colors">
              <div className="w-8 h-8 bg-gray-600 rounded"></div>
              <span className="truncate">{song}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Video Feed */}
        <div className="flex-1 relative overflow-hidden">
          <div className="absolute inset-0 bg-gray-700 flex items-center justify-center">
            <span className="text-4xl text-gray-500">Camera Feed</span>
          </div>
          {/* Gesture Recognition Indicator */}
          <div className="absolute top-4 right-4 bg-primary text-primary-foreground px-3 py-1 rounded-full flex items-center gesture-active">
            <Hand size={18} className="mr-2" />
            <span>Gesture Active</span>
          </div>
        </div>

        {/* Music Player */}
        <div className="h-32 bg-gray-800 p-4 flex items-center">
          <div className="w-24 h-24 bg-gray-600 rounded-lg mr-4 overflow-hidden">
            <img src="/placeholder.svg" alt="Album cover" className="w-full h-full object-cover" />
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-bold">Current Song Title</h3>
            <p className="text-gray-400">Artist Name</p>
            <div className="mt-2 flex items-center">
              <div className="flex-1 bg-gray-700 h-1 rounded-full overflow-hidden">
                <div
                  className="bg-primary h-full transition-all duration-300 ease-in-out"
                  style={{ width: `${currentTime}%` }}
                ></div>
              </div>
              <span className="ml-2 text-sm">{formatTime(currentTime)}</span>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon" className="text-foreground hover:text-primary transition-colors">
              <SkipBack />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-12 w-12 text-foreground hover:text-primary transition-colors"
              onClick={() => setIsPlaying(!isPlaying)}
            >
              {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
            </Button>
            <Button variant="ghost" size="icon" className="text-foreground hover:text-primary transition-colors">
              <SkipForward />
            </Button>
          </div>
          <Button variant="ghost" size="icon" className="ml-4 text-foreground hover:text-primary transition-colors">
            <Volume2 />
          </Button>
          <Button variant="ghost" size="icon" className="ml-2 text-foreground hover:text-primary transition-colors">
            <List />
          </Button>
        </div>
      </div>
    </div>
  )
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`
}

