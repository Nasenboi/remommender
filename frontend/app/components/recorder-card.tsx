"use client"

import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "./ui/card";
import {Button} from "~/components/ui/button";
import {Mic, Pause} from "lucide-react";
import React, {type MouseEventHandler, useState} from "react";
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
        <div className="w-full mt-4">
          <Tooltip>
            <TooltipTrigger className="w-full">
              <Select>
                <SelectTrigger className="w-full">
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
            </TooltipTrigger>
            <TooltipContent>
              <p>The number of seconds after which the emotion in your voice is re-evaluated</p>
            </TooltipContent>
          </Tooltip>
        </div>
      </CardContent>
    </Card>
  )
}