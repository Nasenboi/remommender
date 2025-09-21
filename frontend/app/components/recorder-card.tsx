"use client"

import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "./ui/card";
import {Button} from "~/components/ui/button";
import {Mic, Pause} from "lucide-react";
import React, {useEffect, useRef, useState} from 'react'
import AudioRecorder from "~/lib/AudioRecorder";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue
} from "~/components/ui/select";
import {Tooltip, TooltipContent, TooltipTrigger} from "~/components/ui/tooltip";
import {Label} from "~/components/ui/label";
import {useAudioContext} from '~/context/audio-context'

export function RecorderCard() {
  const [ isRecording, setIsRecording ] = useState<boolean>(false)
  const [ refreshTime, setRefreshTime ] = useState<number>(10)
  const audioRecorder = useRef<AudioRecorder | null>(null)
  const [ refreshInterval, setRefreshInterval ] = useState<any>(null)
  const { currentSong, setCurrentSong } = useAudioContext()

  function recordToggle(e : React.MouseEvent<HTMLElement>) {
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
      setRefreshInterval(setInterval(() => refresh(), refreshTime * 1000))
    }
  }, [isRecording, refreshTime])

  // This ref is necessary because when the refresh() function runs in a set interval, the value of currentSong
  // does not get updated. This is because variables are captured when creating the interval, i.e. the variable values
  // are copied and not referenced. To solve this, we have to create a ref which updates alongside the currentSong within
  // the AudioContext. We can access this ref in the refresh function to check whether the value of currentSong needs to
  // be updated.
  const currentSongRef = useRef(currentSong)
  useEffect(() => {
    currentSongRef.current = currentSong
  }, [currentSong])

  function refresh() {
    audioRecorder.current?.refreshAndGetResult().then((result) => {
      if(result.song.id !== currentSongRef.current?.id) {
        setCurrentSong(result.song)
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
        <div className="w-full mt-4">
          <Tooltip>
            <TooltipTrigger className="w-full">
              <Label htmlFor="refresh-time" className="mb-4 font-normal text-muted-foreground">Refresh time:</Label>
            </TooltipTrigger>
            <TooltipContent>
              <p>The number of seconds after which the emotion in your voice is re-evaluated</p>
            </TooltipContent>
          </Tooltip>
          <Select value={refreshTime.toString()} onValueChange={(newTime) => setRefreshTime(parseInt(newTime))}>
            <SelectTrigger className="w-full" id="refresh-time">
              <SelectValue placeholder="Refresh time" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectLabel>Seconds</SelectLabel>
                <SelectItem value="5">5</SelectItem>
                <SelectItem value="10">10</SelectItem>
                <SelectItem value="15">15</SelectItem>
                <SelectItem value="20">20</SelectItem>
                <SelectItem value="30">30</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
    </Card>
  )
}