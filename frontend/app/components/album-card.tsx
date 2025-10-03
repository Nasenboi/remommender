import type {Album} from "~/lib/AudioTypes"
import {Link} from "react-router"
import {Card, CardContent, CardTitle} from "~/components/ui/card"
import {getAbsoluteBackendURL} from "~/lib/APIRequests"
import React from "react"

interface AlbumCardProps {
  album: Album
}

function Artwork({ url, title }: { url: string, title: string }) {
  if(!url || url === "") {
    return null
  }
  return (
    <img src={getAbsoluteBackendURL(url)} className="h-full w-full"  alt={title}/>
  )
}

export function AlbumCard({ album }: AlbumCardProps) {
  return (
    <Link
      to={`/albums/${album.id}`}
      className="group hover:scale-[1.02] transition-transform"
    >
      <Card className="overflow-hidden border-0 bg-transparent shadow-none">
        <CardContent className="p-4">
          <div className="w-full aspect-square bg-zinc-300 dark:bg-zinc-800 mb-4">
            <Artwork url={album.artwork_url} title={album.album} />
          </div>
          <CardTitle className="text-base font-semibold group-hover:underline">
            {album.album}
          </CardTitle>
          <p className="text-sm text-muted-foreground">{album.artist}</p>
        </CardContent>
      </Card>
    </Link>
  )
}