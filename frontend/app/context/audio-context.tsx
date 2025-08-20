import {createContext, type Dispatch, type ReactNode, type SetStateAction, useContext, useState} from 'react'
import type { Song } from '~/lib/AudioTypes'

type AudioContextType = {
  currentSong: Song | null
  setCurrentSong: Dispatch<SetStateAction<Song | null>>
}
const AudioContext = createContext<AudioContextType | undefined>(undefined)
export const AudioProvider = ({
  children
}: {
  children: ReactNode
}) =>{
  const [currentSong, setCurrentSong] = useState<Song | null>(null)
  const contextValue= {
    currentSong,
    setCurrentSong
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