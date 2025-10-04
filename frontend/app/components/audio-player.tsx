import {Pause, Play, SkipBack, SkipForward, Volume2} from 'lucide-react'
import { Button } from '~/components/ui/button'
import React, { useEffect, useRef, useState } from 'react'
import { Slider } from '~/components/ui/slider'
import { useAudioContext } from '~/context/audio-context'
import type { Song } from '~/lib/AudioTypes'
import { getAbsoluteBackendURL } from '~/lib/APIRequests'

export function AudioPlayer() {
  const { playlist, playlistPosition, setPlaylistPosition } = useAudioContext()

  const [isPlaying, setIsPlaying] = useState<boolean>(false)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const prevSongRef = useRef<Song | null>(null)
  const [currentSong, setCurrentSong] = useState<Song | null>(null)

  useEffect(() => {
    if (!playlist || playlist.length === 0 || playlistPosition === null) return

    const newSong = playlist[playlistPosition]

    if (!prevSongRef.current || prevSongRef.current.id !== newSong.id) {
      setCurrentSong(newSong)

      const handleCanPlay = () => {
        audioRef.current?.play().then(() => {
          setIsPlaying(true)
        }).catch((error) => {
          console.error('Error while starting playback:', error)
        })
      }

      prevSongRef.current = newSong

      audioRef.current?.addEventListener('canplay', handleCanPlay)
      audioRef.current?.addEventListener('ended', nextSong)

      return () => {
        audioRef.current?.removeEventListener('canplay', handleCanPlay)
        audioRef.current?.removeEventListener('ended', nextSong)
      }
    }
  }, [playlist, playlistPosition])

  useEffect(() => {
    if (!playlist) {
      audioRef.current?.pause()
      setCurrentSong(null)
      setIsPlaying(false)
    }
  }, [playlist])

  function playToggle(e: React.MouseEvent<HTMLElement>) {
    if (isPlaying) {
      setIsPlaying(false)
      audioRef.current?.pause()
    } else {
      setIsPlaying(true)
      audioRef.current?.play()
    }
  }

  function nextSong() {
    if(!playlist || playlistPosition === null) return

    const nextPosition = playlistPosition + 1

    if(nextPosition < playlist.length) {
      setPlaylistPosition(nextPosition)
    }
  }

  function previousSong() {
    if(!playlist || playlistPosition === null) return

    const prevPosition = playlistPosition - 1
    if(prevPosition >= 0) {
      setPlaylistPosition(prevPosition)
    }
  }

  function handleVolumeChange(value: any) {
    if(audioRef.current) {
      audioRef.current.volume = value[0]
    }
  }

  function Artwork() {
    if (!currentSong) return null
    return (
      <img
        src={getAbsoluteBackendURL(currentSong.artwork_url)}
        className="h-full w-full"
        alt={currentSong.title}
      />
    )
  }

  function SongInfo() {
    let title = "..."
    let artist = "..."

    if (currentSong) {
      title = currentSong.title
      artist = currentSong.artist
    }

    return (
      <>
        <p>{title}</p>
        <p className="text-zinc-700 text-xs">{artist}</p>
      </>
    )
  }

  return (
    <div className="w-full h-20 sticky bottom-0 left-0 right-0 border-t-2 bg-background border-sidebar-border">
      <div className="absolute left-2 top-1/2 -translate-y-1/2 flex items-center h-full pt-2 pb-2">
        <div className="h-full aspect-square bg-zinc-300 dark:bg-zinc-800 mr-2">
          <Artwork />
        </div>
        <div>
          <SongInfo />
        </div>
      </div>

      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
        <audio
          ref={audioRef}
          src={currentSong ? getAbsoluteBackendURL(currentSong.song_url) : undefined}
        />
        { playlist && playlist.length > 1
        ? <Button className="p-1 mr-2" size="icon" variant="ghost" onClick={previousSong}>
            <SkipBack className="size-4" />
          </Button>
        : null }
        <Button className="rounded-full w-9 h-9" size="icon" onClick={playToggle}>
          {isPlaying
            ? <Pause className="size-5 text-white dark:text-zinc-600" />
            : <Play className="size-5 text-white dark:text-zinc-600" />}
        </Button>
        { playlist && playlist.length > 1
        ? <Button className="p-1 ml-2" size="icon" variant="ghost" onClick={nextSong}>
            <SkipForward className="size-4" />
          </Button>
        : null }
      </div>

      <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center h-full">
        <Volume2 className="size-5 text-primary mr-2" />
        <Slider
          defaultValue={[1]}
          min={0}
          max={1}
          step={0.01}
          onValueChange={handleVolumeChange}
          className="w-30"
        />
      </div>
    </div>
  )
}
