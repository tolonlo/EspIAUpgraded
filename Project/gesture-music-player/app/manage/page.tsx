"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useToast } from "@/hooks/use-toast"
import Link from "next/link"
import { usePlaylist, PlaylistProvider } from "@/components/playlist-context"
import { Music, Trash2, ArrowLeft, Upload, Plus } from "lucide-react"
import { UserNav } from "@/components/user-nav"

// Create a wrapper component that uses the context
function ManagePageContent() {
  const { toast } = useToast()
  const { songs, addSong, removeSong } = usePlaylist()
  const [newSong, setNewSong] = useState({ title: "", artist: "", url: "" })
  const [importUrl, setImportUrl] = useState("")

  const handleAddSong = () => {
    if (!newSong.title || !newSong.artist || !newSong.url) {
      toast({
        title: "Missing information",
        description: "Please fill in all fields",
        variant: "destructive",
      })
      return
    }

    addSong({
      ...newSong,
      id: Date.now().toString(),
    })

    setNewSong({ title: "", artist: "", url: "" })
    toast({
      title: "Song added",
      description: `${newSong.title} by ${newSong.artist} has been added to your playlist.`,
    })
  }

  const handleImportPlaylist = () => {
    toast({
      title: "Playlist imported",
      description: "Your playlist has been imported successfully.",
    })
    setImportUrl("")
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center">
            <Link href="/">
              <Button variant="ghost" size="icon" className="mr-4">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <h1 className="text-3xl font-bold">Manage Your Music</h1>
          </div>
          <UserNav />
        </header>

        <Tabs defaultValue="songs" className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-2 mb-8">
            <TabsTrigger value="songs">Your Songs</TabsTrigger>
            <TabsTrigger value="import">Import</TabsTrigger>
          </TabsList>

          <TabsContent value="songs">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle>Add New Song</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm font-medium mb-1 block">Song Title</label>
                      <Input
                        placeholder="Enter song title"
                        value={newSong.title}
                        onChange={(e) => setNewSong({ ...newSong, title: e.target.value })}
                        className="bg-slate-700 border-slate-600"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium mb-1 block">Artist</label>
                      <Input
                        placeholder="Enter artist name"
                        value={newSong.artist}
                        onChange={(e) => setNewSong({ ...newSong, artist: e.target.value })}
                        className="bg-slate-700 border-slate-600"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium mb-1 block">Audio URL</label>
                      <Input
                        placeholder="Enter audio file URL"
                        value={newSong.url}
                        onChange={(e) => setNewSong({ ...newSong, url: e.target.value })}
                        className="bg-slate-700 border-slate-600"
                      />
                    </div>
                    <Button onClick={handleAddSong} className="w-full">
                      <Plus className="mr-2 h-4 w-4" /> Add Song
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle>Your Playlist</CardTitle>
                </CardHeader>
                <CardContent>
                  {songs.length === 0 ? (
                    <p className="text-slate-400 text-center py-8">Your playlist is empty. Add some songs!</p>
                  ) : (
                    <ul className="space-y-3">
                      {songs.map((song) => (
                        <li key={song.id} className="flex items-center justify-between p-3 bg-slate-700 rounded-md">
                          <div className="flex items-center">
                            <Music className="h-5 w-5 mr-3 text-slate-400" />
                            <div>
                              <p className="font-medium">{song.title}</p>
                              <p className="text-sm text-slate-400">{song.artist}</p>
                            </div>
                          </div>
                          <Button variant="ghost" size="icon" onClick={() => removeSong(song.id)}>
                            <Trash2 className="h-4 w-4 text-red-400" />
                          </Button>
                        </li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="import">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle>Import Playlist</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium mb-1 block">Playlist URL</label>
                    <Input
                      placeholder="Enter Spotify or YouTube playlist URL"
                      value={importUrl}
                      onChange={(e) => setImportUrl(e.target.value)}
                      className="bg-slate-700 border-slate-600"
                    />
                  </div>
                  <Button onClick={handleImportPlaylist} className="w-full">
                    <Upload className="mr-2 h-4 w-4" /> Import Playlist
                  </Button>

                  <div className="mt-8 p-4 border border-dashed border-slate-600 rounded-md text-center">
                    <p className="text-slate-400 mb-2">Or upload a file</p>
                    <Button variant="outline" className="w-full">
                      Choose File
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </main>
  )
}

// Main component that wraps the content with the provider
export default function ManagePage() {
  return (
    <PlaylistProvider>
      <ManagePageContent />
    </PlaylistProvider>
  )
}

