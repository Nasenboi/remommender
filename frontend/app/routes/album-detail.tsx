import type { Route } from "./+types/album-detail"
import type {Album, AlbumShort, Song} from "~/lib/AudioTypes"
import {useEffect, useState} from "react"
import {Button} from "~/components/ui/button"
import {ArrowLeft, MoreVertical, Play, Trash2} from "lucide-react"
import {DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger} from "~/components/ui/dropdown-menu"
import {Spinner} from "~/components/ui/spinner"
import {useNavigate, useParams} from "react-router"
import {toast} from "sonner"
import {getAbsoluteBackendURL, sendBackendRequest} from "~/lib/APIRequests"
import {useAudioContext} from "~/context/audio-context"

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Album details" },
    { name: "description", content: "This page shows the contents of an album" },
  ];
}

export default function AlbumDetailsPage() {
  const [album, setAlbum] = useState<Album | null>(null)
  const params = useParams()
  const navigate = useNavigate()
  const { playlist, setPlaylist, setPlaylistPosition } = useAudioContext()

  const fetchAlbum = () => {
    setAlbum(null)
    if(!params.albumId) {
      toast.error("No album ID was specified. Please check your URL.")
      return
    }
    sendBackendRequest({
      url: `/albums/${params.albumId}`,
      method: "GET",
    }).then((response) => {
      setAlbum(response.data as Album)
    })
  }

  useEffect(() => {
    fetchAlbum()
  }, []);

  const handleDeleteSong = (song: Song) => {
    sendBackendRequest({
      url: `/songs/${song.id}`,
      method: "DELETE",
    }).then((response) => {
      toast(`The song "${song.title}" was deleted successfully.`)
      fetchAlbum()
    })
  }

  const handlePlayAlbum = () => {
    if(album) {
      setPlaylistPosition(null)
      setPlaylist(album.songs)
      setPlaylistPosition(0)
    }
  }

  const handlePlaySong = (song: Song) => {
    if(album) {
      setPlaylistPosition(null)
      setPlaylist(album.songs)
      setPlaylistPosition(album.songs.indexOf(song))
    }
  }

  const handleBack = () => {
    navigate(-1)
  }

  if (album) {
    return (
      <div className="xl:w-6xl w-full max-w-full mx-auto p-6 space-y-8">
        <Button
          variant="outline"
          onClick={handleBack}
          className="flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </Button>
        <div className="flex gap-6 items-start">
          <img
            src={getAbsoluteBackendURL(album.artwork_url)}
            alt={album.album}
            className="w-48 h-48 object-cover rounded-md shadow"
          />
          <div className="flex flex-col justify-between h-full">
            <div>
              <h1 className="text-3xl font-bold">{album.album}</h1>
              <p className="text-muted-foreground text-sm mt-2">{album.artist}</p>
              <p className="text-muted-foreground text-sm mt-1">
                {album.songs.length} Song{album.songs.length !== 1 ? "s" : ""}
              </p>
            </div>
            <Button
              className="mt-4"
              onClick={handlePlayAlbum}
            >
              <Play className="w-4 h-4 mr-2"/>
              Play album
            </Button>
          </div>
        </div>

        <div className="space-y-4">
          {album.songs.map((song, index) => (
            <div
              key={song.id}
              className="flex items-center justify-between p-4 rounded-md border hover:bg-muted transition"
            >
              <div className="flex items-center gap-4">
                <span className="text-muted-foreground w-6">{index + 1}</span>
                <div>
                  <p className="font-medium">{song.title}</p>
                  <p className="text-sm text-muted-foreground">{song.artist}</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => handlePlaySong(song)}
                >
                  <Play className="w-4 h-4"/>
                </Button>

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button size="icon" variant="ghost">
                      <MoreVertical className="w-4 h-4"/>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem
                      className="cursor-pointer"
                      onClick={() => handleDeleteSong(song)}
                    >
                      <Trash2 className="w-4 h-4"/>
                      Delete song
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }
  return (
    <div className="flex items-center justify-center w-full flex-1">
      <Spinner className="size-10" />
    </div>
  )
}
