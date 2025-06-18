"use client"

import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "./ui/card";
import {Button} from "~/components/ui/button";
import {Mic, Pause} from "lucide-react";
import React, {type MouseEventHandler, useState} from "react";
import AudioRecorder from "~/lib/AudioRecorder";


export function RecorderCard() {
  const [ isRecording, setIsRecording ] = useState<boolean>(false)

  let audioRecorder: AudioRecorder | null = null


  async function recordToggle(e : React.MouseEvent<HTMLElement>) {
    if(!audioRecorder) {
      audioRecorder = await AudioRecorder.createRecorder(10)
    }

    if(isRecording) {
      audioRecorder.stop()
    } else {
      await audioRecorder.start()
    }

    setIsRecording(audioRecorder.isRecording())
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
              : <Mic className="size-6 text-zinc-600"></Mic>
            }
          </Button>
        </div>

      </CardContent>
    </Card>
  )
}