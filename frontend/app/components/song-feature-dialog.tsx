"use client"

import type {Song} from "~/lib/AudioTypes"

import {Button} from "~/components/ui/button"
import {
  Dialog, DialogClose,
  DialogContent,
  DialogDescription, DialogFooter,
  DialogHeader,
  DialogTitle
} from "~/components/ui/dialog"
import React from "react"
import {DialogTrigger} from "@radix-ui/react-dialog"
import {Info} from "lucide-react"


export interface FeatureDialogProps {
  song: Song
}

export default function SongFeatureDialog({ song }: FeatureDialogProps) {

  const Genres = () => {
    const genreNames = Object.keys(song.genres.top3_genres)
    const genreValues: number[] = []
    genreNames.forEach((genre) => {
      genreValues.push(song.genres.top3_genres[genre])
    })

    return (
      <div>
        <p className="text-muted-foreground text-xs">{genreNames[0]}: {genreValues[0]}</p>
        <p className="text-muted-foreground text-xs">{genreNames[1]}: {genreValues[1]}</p>
        <p className="text-muted-foreground text-xs">{genreNames[2]}: {genreValues[1]}</p>
      </div>
    )
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost"><Info className="w-4 h-4"></Info></Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{song.title}</DialogTitle>
          <DialogDescription className="text-xs">
            Artist: { song.artist }<br />
            Album: { song.album.album_name }
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-2">
          <h4 className="text-s font-semibold tracking-tight">Top 3 Genres</h4>
          <Genres />
          <h4 className="text-s font-semibold tracking-tight">Features</h4>
          <div>
            <p className="text-muted-foreground text-xs">Arousal: {song.features.arousal}</p>
            <p className="text-muted-foreground text-xs">Valence: {song.features.valence}</p>
            <p className="text-muted-foreground text-xs">Authenticity: {song.features.authenticity}</p>
            <p className="text-muted-foreground text-xs">Timeliness: {song.features.timeliness}</p>
            <p className="text-muted-foreground text-xs">Complexity: {song.features.complexity}</p>
            <p className="text-muted-foreground text-xs">Danceability: {song.features.danceability}</p>
            <p className="text-muted-foreground text-xs">Tonal: {song.features.tonal}</p>
            <p className="text-muted-foreground text-xs">Voice: {song.features.voice}</p>
            <p className="text-muted-foreground text-xs">BPM: {song.features.bpm}</p>
          </div>
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Close</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
