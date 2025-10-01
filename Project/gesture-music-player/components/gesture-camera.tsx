"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { usePlaylist } from "./playlist-context"
import { Camera, CameraOff, Hand, AlertTriangle, Info } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

// Mock gesture detection results for demonstration
type GestureResult = {
  gesture: string
  confidence: number
}

export function GestureCamera() {
  const [isActive, setIsActive] = useState(false)
  const [detectedGesture, setDetectedGesture] = useState<string | null>(null)
  const [cameraError, setCameraError] = useState<string | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const { playPause, nextSong, prevSong } = usePlaylist()

  // Start camera when active
  useEffect(() => {
    let stream: MediaStream | null = null

    const startCamera = async () => {
      try {
        // Reset any previous errors
        setCameraError(null)

        // Try to access the camera with fallback options
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: "user",
          },
        })

        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }

        // Start gesture detection loop
        requestAnimationFrame(detectGestures)
      } catch (err) {
        console.error("Error accessing camera:", err)

        // Set a user-friendly error message
        if (err instanceof DOMException) {
          if (err.name === "NotAllowedError") {
            setCameraError("Camera access was denied. Please allow camera access to use gesture controls.")
          } else if (err.name === "NotFoundError") {
            setCameraError("No camera was found on your device.")
          } else if (err.name === "NotReadableError") {
            setCameraError("Camera is already in use by another application.")
          } else {
            setCameraError(`Camera error: ${err.message}`)
          }
        } else {
          setCameraError("Could not access camera. Gesture controls will not be available.")
        }

        // Turn off the camera activation state
        setIsActive(false)
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

    if (isActive) {
      startCamera()
    } else {
      stopCamera()
    }

    return () => {
      stopCamera()
    }
  }, [isActive])

  // Mock gesture detection function
  // In a real app, you would use a library like MediaPipe or TensorFlow.js
  const detectGestures = () => {
    if (!isActive || !videoRef.current || !canvasRef.current) return

    const ctx = canvasRef.current.getContext("2d")
    if (!ctx) return

    // Draw video frame to canvas
    try {
      ctx.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height)

      // Mock gesture detection
      // In a real app, this would be replaced with actual ML-based detection
      const gestures = ["wave_right", "wave_left", "palm_up", "palm_down", "fist", "none"]
      const randomGesture = gestures[Math.floor(Math.random() * (gestures.length - 1))]
      const shouldDetect = Math.random() > 0.95 // Only detect occasionally for demo

      if (shouldDetect && randomGesture !== "none") {
        handleGestureDetected({
          gesture: randomGesture,
          confidence: 0.8 + Math.random() * 0.2,
        })
      }

      // Continue detection loop
      requestAnimationFrame(detectGestures)
    } catch (err) {
      console.error("Error in gesture detection:", err)
      // If there's an error in the detection loop, we don't want to crash the app
      requestAnimationFrame(detectGestures)
    }
  }

  const handleGestureDetected = (result: GestureResult) => {
    setDetectedGesture(result.gesture)

    // Map gestures to player controls
    switch (result.gesture) {
      case "wave_right":
        nextSong()
        break
      case "wave_left":
        prevSong()
        break
      case "fist":
        playPause()
        break
      // Additional gestures could be added for volume, etc.
    }

    // Clear the gesture after a short delay
    setTimeout(() => {
      setDetectedGesture(null)
    }, 1500)
  }

  // For demo purposes - simulate gestures without camera
  const simulateGesture = (gesture: string) => {
    handleGestureDetected({
      gesture,
      confidence: 0.9,
    })
  }

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-full aspect-video bg-slate-900 rounded-lg overflow-hidden mb-4">
        {isActive ? (
          <>
            <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover" />
            <canvas
              ref={canvasRef}
              width={640}
              height={480}
              className="absolute top-0 left-0 w-full h-full opacity-0"
            />
            {detectedGesture && (
              <div className="absolute bottom-4 left-4 bg-slate-800/80 px-3 py-2 rounded-md flex items-center">
                <Hand className="h-4 w-4 mr-2" />
                <span className="text-sm font-medium capitalize">{detectedGesture.replace("_", " ")}</span>
              </div>
            )}
          </>
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center">
            <CameraOff className="h-12 w-12 text-slate-600 mb-4" />
            <p className="text-slate-400 text-center">Camera is turned off</p>
            {cameraError && <p className="text-red-400 text-center text-sm mt-2 max-w-md px-4">{cameraError}</p>}
          </div>
        )}
      </div>

      <Button onClick={() => setIsActive(!isActive)} variant={isActive ? "destructive" : "default"} className="w-full">
        {isActive ? (
          <>
            <CameraOff className="mr-2 h-4 w-4" /> Turn Off Camera
          </>
        ) : (
          <>
            <Camera className="mr-2 h-4 w-4" /> Turn On Camera
          </>
        )}
      </Button>

      {cameraError && (
        <Alert variant="destructive" className="mt-4">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Camera Access Error</AlertTitle>
          <AlertDescription>{cameraError}</AlertDescription>
        </Alert>
      )}

      {/* Gesture guide and simulation buttons */}
      <div className="mt-6 p-4 bg-slate-700/50 rounded-lg w-full">
        <h3 className="font-medium mb-2">Gesture Guide</h3>
        <ul className="space-y-2 text-sm mb-4">
          <li className="flex items-center">
            <div className="w-24">Wave Right</div>
            <span className="text-slate-400">Next song</span>
          </li>
          <li className="flex items-center">
            <div className="w-24">Wave Left</div>
            <span className="text-slate-400">Previous song</span>
          </li>
          <li className="flex items-center">
            <div className="w-24">Palm Up</div>
            <span className="text-slate-400">Volume up</span>
          </li>
          <li className="flex items-center">
            <div className="w-24">Palm Down</div>
            <span className="text-slate-400">Volume down</span>
          </li>
          <li className="flex items-center">
            <div className="w-24">Fist</div>
            <span className="text-slate-400">Play/Pause</span>
          </li>
        </ul>

        {cameraError && (
          <>
            <Alert className="mb-4">
              <Info className="h-4 w-4" />
              <AlertTitle>Gesture Simulation</AlertTitle>
              <AlertDescription>
                Since camera access is not available, you can use these buttons to simulate gestures.
              </AlertDescription>
            </Alert>

            <div className="grid grid-cols-3 gap-2">
              <Button size="sm" variant="outline" onClick={() => simulateGesture("wave_left")}>
                Previous
              </Button>
              <Button size="sm" variant="outline" onClick={() => simulateGesture("fist")}>
                Play/Pause
              </Button>
              <Button size="sm" variant="outline" onClick={() => simulateGesture("wave_right")}>
                Next
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

