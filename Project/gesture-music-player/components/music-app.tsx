"use client"

import { useState, useRef, useEffect } from "react"
import { Slider } from "@/components/ui/slider"
import { Button } from "@/components/ui/button"
import { usePlaylist } from "./playlist-context"
import { Play, Pause, SkipBack, SkipForward, Settings, Camera, CameraOff, Hand, Music, Plus, X } from "lucide-react"

export function MusicApp() {
  const { currentSong, isPlaying, playPause, nextSong, prevSong, songs, setCurrentSong, addSong, removeSong } =
    usePlaylist()

  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [showPlaylist, setShowPlaylist] = useState(false)
  const [showAddSong, setShowAddSong] = useState(false)
  const [newSong, setNewSong] = useState({ title: "", artist: "", url: "" })

  // Camera and gesture detection
  const [cameraActive, setCameraActive] = useState(false)
  const [detectedGesture, setDetectedGesture] = useState<string | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const audioRef = useRef<HTMLAudioElement>(null)

  // Audio player effects
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

  // Camera effects
  useEffect(() => {
    let stream: MediaStream | null = null

    const startCamera = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user" },
        })

        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }

        requestAnimationFrame(detectGestures)
      } catch (err) {
        console.error("Error accessing camera:", err)
      }
    }

    const stopCamera = () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop())
      }
      if (videoRef.current) {
        videoRef.current.srcObject = null
      }
    }

    if (cameraActive) {
      startCamera()
    } else {
      stopCamera()
    }

    return () => {
      stopCamera()
    }
  }, [cameraActive])

  // Mock gesture detection
  const detectGestures = () => {
    if (!cameraActive || !videoRef.current || !canvasRef.current) return

    const ctx = canvasRef.current.getContext("2d")
    if (!ctx) return

    ctx.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height)

    // Mock gesture detection
    const gestures = ["wave_right", "wave_left", "palm_up", "palm_down", "fist", "none"]
    const randomGesture = gestures[Math.floor(Math.random() * (gestures.length - 1))]
    const shouldDetect = Math.random() > 0.95 // Only detect occasionally for demo

    if (shouldDetect && randomGesture !== "none") {
      handleGestureDetected(randomGesture)
    }

    requestAnimationFrame(detectGestures)
  }

  const handleGestureDetected = (gesture: string) => {
    setDetectedGesture(gesture)

    switch (gesture) {
      case "wave_right":
        nextSong()
        break
      case "wave_left":
        prevSong()
        break
      case "fist":
        playPause()
        break
    }

    setTimeout(() => {
      setDetectedGesture(null)
    }, 1000)
  }

  const handleAddSong = () => {
    if (newSong.title && newSong.url) {
      addSong({
        ...newSong,
        id: Date.now().toString(),
      })
      setNewSong({ title: "", artist: "", url: "" })
      setShowAddSong(false)
    }
  }

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`
  }

  return (
    <div className="max-w-md mx-auto">
      <audio
        ref={audioRef}
        src={currentSong?.url || "/sample-audio.mp3"}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={nextSong}
      />

      {/* Camera View (when active) */}
      {cameraActive && (
        <div className="relative w-full aspect-video bg-slate-800 rounded mb-2">
          <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover rounded" />
          <canvas ref={canvasRef} width={320} height={240} className="absolute top-0 left-0 w-full h-full opacity-0" />
          {detectedGesture && (
            <div className="absolute bottom-1 left-1 bg-slate-800/80 px-1.5 py-0.5 rounded flex items-center">
              <Hand className="h-3 w-3 mr-1" />
              <span className="text-xs capitalize">{detectedGesture.replace("_", " ")}</span>
            </div>
          )}
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-1 right-1 h-6 w-6 bg-slate-800/50"
            onClick={() => setCameraActive(false)}
          >
            <X className="h-3 w-3" />
          </Button>
        </div>
      )}

      {/* Main Player UI */}
      <div className="bg-slate-800 rounded p-2">
        <div className="flex items-center justify-between mb-1">
          <div className="flex items-center overflow-hidden">
            <div className="w-8 h-8 bg-slate-700 rounded flex items-center justify-center mr-2 flex-shrink-0">
              <Music className="h-4 w-4 text-slate-400" />
            </div>
            <div className="overflow-hidden">
              <h3 className="font-medium text-sm truncate">{currentSong?.title || "No song"}</h3>
              <p className="text-xs text-slate-400 truncate">{currentSong?.artist || "Unknown"}</p>
            </div>
          </div>

          <div className="flex gap-1">
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => setCameraActive(!cameraActive)}>
              {cameraActive ? <CameraOff className="h-3 w-3" /> : <Camera className="h-3 w-3" />}
            </Button>
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => setShowPlaylist(!showPlaylist)}>
              <Settings className="h-3 w-3" />
            </Button>
          </div>
        </div>

        <div className="flex items-center text-xs mb-1">
          <span className="text-slate-400 w-7">{formatTime(currentTime)}</span>
          <Slider value={[currentTime]} max={duration || 100} step={0.1} onValueChange={handleSeek} className="mx-1" />
          <span className="text-slate-400 w-7">{formatTime(duration)}</span>
        </div>

        <div className="flex justify-center items-center">
          <Button variant="ghost" size="icon" className="h-7 w-7" onClick={prevSong}>
            <SkipBack className="h-4 w-4" />
          </Button>
          <Button variant="default" size="icon" className="h-9 w-9 mx-1 rounded-full" onClick={playPause}>
            {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          </Button>
          <Button variant="ghost" size="icon" className="h-7 w-7" onClick={nextSong}>
            <SkipForward className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Playlist Panel */}
      {showPlaylist && (
        <div className="bg-slate-800 rounded mt-2 p-2">
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-xs font-medium">Your Playlist</h3>
            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setShowAddSong(!showAddSong)}>
              <Plus className="h-3 w-3" />
            </Button>
          </div>

          {showAddSong && (
            <div className="mb-2 space-y-1">
              <input
                className="w-full text-xs p-1 rounded bg-slate-700 border-none"
                placeholder="Song title"
                value={newSong.title}
                onChange={(e) => setNewSong({ ...newSong, title: e.target.value })}
              />
              <input
                className="w-full text-xs p-1 rounded bg-slate-700 border-none"
                placeholder="Artist (optional)"
                value={newSong.artist}
                onChange={(e) => setNewSong({ ...newSong, artist: e.target.value })}
              />
              <input
                className="w-full text-xs p-1 rounded bg-slate-700 border-none"
                placeholder="Audio URL"
                value={newSong.url}
                onChange={(e) => setNewSong({ ...newSong, url: e.target.value })}
              />
              <Button size="sm" className="w-full text-xs h-7" onClick={handleAddSong}>
                Add
              </Button>
            </div>
          )}

          <div className="max-h-32 overflow-y-auto">
            {songs.length === 0 ? (
              <p className="text-slate-400 text-xs text-center py-2">No songs in playlist</p>
            ) : (
              songs.map((song) => (
                <div
                  key={song.id}
                  className={`flex items-center justify-between p-1 rounded mb-1 cursor-pointer text-xs ${
                    currentSong?.id === song.id ? "bg-slate-700" : "hover:bg-slate-700"
                  }`}
                  onClick={() => setCurrentSong(song)}
                >
                  <div className="flex items-center overflow-hidden">
                    <Music className="h-3 w-3 mr-1 text-slate-400 flex-shrink-0" />
                    <span className="truncate">{song.title}</span>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-5 w-5 ml-1"
                    onClick={(e) => {
                      e.stopPropagation()
                      removeSong(song.id)
                    }}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                </div>
              ))
            )}
          </div>

          {cameraActive && (
            <div className="mt-2 border-t border-slate-700 pt-1">
              <h3 className="text-xs font-medium mb-1">Gesture Guide</h3>
              <div className="grid grid-cols-3 gap-1 text-[10px]">
                <div>Wave Right: Next</div>
                <div>Wave Left: Prev</div>
                <div>Fist: Play/Pause</div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

