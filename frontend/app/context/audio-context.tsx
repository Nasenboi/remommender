import {createContext, type Dispatch, type ReactNode, type SetStateAction, useContext, useState} from 'react'
import type { Song } from '~/lib/AudioTypes'

type AudioContextType = {
  playlist: Song[] | null
  setPlaylist: Dispatch<SetStateAction<Song[] | null>>
  playlistPosition: number | null
  setPlaylistPosition: Dispatch<SetStateAction<number | null>>
}
const AudioContext = createContext<AudioContextType | undefined>(undefined)
export const AudioProvider = ({
  children
}: {
  children: ReactNode
}) =>{
  const [playlist, setPlaylist] = useState<Song[] | null>(null)
  const [playlistPosition, setPlaylistPosition] = useState<number | null>(null)
  const contextValue= {
    playlist,
    setPlaylist,
    playlistPosition,
    setPlaylistPosition
  }
  return (
    <AudioContext.Provider value={contextValue}>
      {children}
    </AudioContext.Provider>
  )
}
export const useAudioContext = (): AudioContextType => {
  const context = useContext(AudioContext)
  if (context === undefined) {
    throw new Error(
      'useAudioContext must be used within an AudioProvider'
    )
  }
  return context
}