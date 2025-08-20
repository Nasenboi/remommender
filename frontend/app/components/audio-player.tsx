import {Pause, Play, Volume2} from 'lucide-react'
import {Button} from '~/components/ui/button'
import React, {useEffect, useRef, useState} from 'react'
import {Slider} from '~/components/ui/slider'
import {useAudioContext} from '~/context/audio-context'


export function AudioPlayer() {

  const { currentSong } = useAudioContext()

  const [ isPlaying, setIsPlaying ] = useState<boolean>(false)
  const audioRef = useRef<HTMLAudioElement | null>(null)

  function getAbsoluteBackendURL(relativeURL: string) {
    return import.meta.env.VITE_BACKEND_BASE_URL + relativeURL
  }

  useEffect(() => {
    if(!currentSong) {
      setIsPlaying(false)
    } else {
      if(isPlaying) {
        audioRef.current?.play()
      }
    }
  }, [currentSong])

  function playToggle(e : React.MouseEvent<HTMLElement>) {
    if (isPlaying) {
      setIsPlaying(false)
      audioRef.current?.pause()
    } else {
      setIsPlaying(true)
      audioRef.current?.play()
    }
  }

  function Artwork() {
    if(!currentSong) {
      return null
    }
    return (
      <img src={getAbsoluteBackendURL(currentSong.artwork_url)} className="h-full w-full"  alt={currentSong.title}/>
    )
  }

  function SongInfo() {
    let title = "..."
    let artist = "..."

    if(currentSong) {
      title = currentSong.title
      artist = currentSong.artist
    }

    return (
      <><p>{title}</p><p className="text-zinc-700 text-xs">{artist}</p></>
    )
  }

  function ControlsAndAudio() {
    if (currentSong) {
      return (
        <>
          <audio src={getAbsoluteBackendURL(currentSong?.song_url)} loop ref={audioRef}></audio>
          <Button className="rounded-full w-9 h-9" size="icon" onClick={playToggle}>
            {isPlaying
              ? <Pause className="size-5 text-white dark:text-zinc-600"/>
              : <Play className="size-5 text-white dark:text-zinc-600"/>}
          </Button>
        </>
      )
    } else {
      return (
        <Button className="rounded-full w-9 h-9" disabled size="icon">
          <Play className="size-5 text-white dark:text-zinc-600"/>
        </Button>
      )
    }
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
        <ControlsAndAudio />
      </div>
      <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center h-full">
        <Volume2 className="size-5 text-primary mr-2" />
        <Slider
          defaultValue={[100]}
          max={100}
          step={1}
          className="w-30"
        />
      </div>
    </div>
  )
}
