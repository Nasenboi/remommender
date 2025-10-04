"use client"


import {useAudioContext} from '~/context/audio-context'
import {RecorderSettings, type RecorderSettingsState} from '~/components/recorder-settings'
import React, {useEffect, useRef, useState} from 'react'
import AudioRecorder from '~/lib/AudioRecorder'
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from '~/components/ui/card'
import {Button} from '~/components/ui/button'
import {Mic, Pause} from 'lucide-react'
import type {Song} from "~/lib/AudioTypes"

export function RecorderCard() {
  const [ isRecording, setIsRecording ] = useState<boolean>(false)
  const audioRecorder = useRef<AudioRecorder | null>(null)
  const [ refreshInterval, setRefreshInterval ] = useState<any>(null)
  const { playlist, setPlaylist, playlistPosition, setPlaylistPosition } = useAudioContext()

  const [settings, setSettings] = useState<RecorderSettingsState>({
    refreshTime: 20,
    arousalWeight: 0.5,
    valenceWeight: 0.5,
    genreEnabled: false,
    genre: null,
    authenticityEnabled: false,
    authenticity: 0,
    timelinessEnabled: false,
    timeliness: 0,
    complexityEnabled: false,
    complexity: 0,
    danceabilityEnabled: false,
    danceability: 0,
    tonalEnabled: false,
    tonal: 0,
    voiceEnabled: false,
    voice: 0,
    bpmEnabled: false,
    bpm: 120
  })

  function recordToggle() {
    if(!audioRecorder.current) {
      AudioRecorder.createRecorder().then((recorderInstance) => {
        audioRecorder.current = recorderInstance
        recorderInstance.start().then(() => {
          setIsRecording(true)
        })
      })
      return
    }
    if(isRecording) {
      audioRecorder.current?.stop()
      setIsRecording(false)
      setPlaylistPosition(null)
      setPlaylist(null)
    } else {
      audioRecorder.current?.start().then(() => {
        setIsRecording(true)
      })
    }
  }

  // This effect (re)sets the refreshInterval whenever the recording state or the refresh time changes.
  // This needs to be done with useEffect because refresh() (the refreshInterval callback) accesses the audioRecorder
  // state, which needs to be instantiated with a value before setting the interval.
  useEffect(() => {
    if(refreshInterval) {
      clearInterval(refreshInterval)
    }
    // if audioRecorder exists (i.e. the recording has been initiated at least once) and the audioRecorder is recording,
    // set the refresh interval
    if(audioRecorder && isRecording) {
      setRefreshInterval(setInterval(() => refresh(), settings.refreshTime * 1000))
    }
  }, [isRecording, settings.refreshTime])

  // This ref is necessary because when the refresh() function runs in a set interval, the value of playlist / position
  // does not get updated. This is because variables are captured when creating the interval, i.e. the variable values
  // are copied and not referenced. To solve this, we have to create a ref which updates alongside the currentSong within
  // the AudioContext. We can access this ref in the refresh function to check whether the value of currentSong needs to
  // be updated.
  const playlistRef = useRef(playlist)
  const playlistPositionRef = useRef(playlistPosition)
  useEffect(() => {
    playlistRef.current = playlist
  }, [playlist])
  useEffect(() => {
    playlistPositionRef.current = playlistPosition
  }, [playlistPosition])
  // same as above, but for the settings
  const settingsRef = useRef(settings)
  useEffect(() => {
    settingsRef.current = settings
  }, [settings])

  function refresh() {
    audioRecorder.current?.refreshAndGetResult(settingsRef.current).then((result) => {
      const newSong = result.song
      let playingSong: Song | null = null

      if(playlistRef.current && playlistPositionRef.current) {
        playingSong = playlistRef.current[playlistPositionRef.current]
      }
      
      if(newSong.id !== playingSong?.id) {
        setPlaylistPosition(null)
        setPlaylist([newSong])
        setPlaylistPosition(0)
      }
    })
  }

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Play music</CardTitle>
        <CardDescription>
          Click the button below to start recording your voice.
          After some seconds of speech, the music will start.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-center">
          <Button className="rounded-full w-14 h-14" size="icon" onClick={recordToggle}>
            { isRecording
              ? <Pause className="size-6 text-red-600"></Pause>
              : <Mic className="size-6 text-white dark:text-gray-600"></Mic>
            }
          </Button>
        </div>
        <div className="w-full mt-5 text-center">
          <RecorderSettings
            settings={settings}
            setSettings={setSettings}
          />
        </div>
      </CardContent>
    </Card>
  )
}