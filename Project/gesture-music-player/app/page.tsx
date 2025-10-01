import { Button } from "@/components/ui/button"
import Link from "next/link"
import { MusicPlayer } from "@/components/music-player"
import { GestureCamera } from "@/components/gesture-camera"
import { PlaylistProvider } from "@/components/playlist-context"
import { UserNav } from "@/components/user-nav"

export default function Home() {
  return (
    <PlaylistProvider>
      <main className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 text-white">
        <div className="container mx-auto px-4 py-8">
          <header className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold">Gesture Music Player</h1>
            <div className="flex items-center gap-4">
              <Link href="/manage">
                <Button variant="default" className="bg-purple-600 hover:bg-purple-700">
                  Manage Songs
                </Button>
              </Link>
              <UserNav />
            </div>
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-slate-800 rounded-xl p-6 shadow-lg">
              <h2 className="text-2xl font-semibold mb-4">Camera Controls</h2>
              <p className="text-slate-300 mb-6">
                Use hand gestures to control your music. Wave right to skip, left to previous, palm up to increase
                volume, palm down to decrease volume, and make a fist to play/pause.
              </p>
              <GestureCamera />
            </div>

            <div className="bg-slate-800 rounded-xl p-6 shadow-lg">
              <h2 className="text-2xl font-semibold mb-4">Music Player</h2>
              <p className="text-slate-300 mb-6">Traditional controls if you prefer not to use gestures.</p>
              <MusicPlayer />
            </div>
          </div>
        </div>
      </main>
    </PlaylistProvider>
  )
}

