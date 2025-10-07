import type { Route } from "./+types/home";
import {RecorderCard} from "~/components/recorder-card";
import {Sidebar} from '~/components/ui/sidebar'
import React, {useState} from "react"
import type {AudioResult} from "~/lib/AudioRecorder"
import {Label} from "~/components/ui/label"
import {Switch} from "~/components/ui/switch"
import {StatsCard} from "~/components/StatsCard"

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Remommender" },
    { name: "description", content: "Start talking and we'll play the music!" },
  ];
}

export default function Home() {
  const [ audioResultHistory, setAudioResultHistory ] = useState<AudioResult[]>([])
  const [ showStats, setShowStats ] = useState<boolean>(false)

  return (
    <div className="flex items-center justify-center w-full flex-1 flex-col">
      <div className="w-full max-w-sm">
        <RecorderCard
          audioHistory={audioResultHistory}
          setAudioHistory={setAudioResultHistory}
        ></RecorderCard>
        <div className="flex justify-between p-5">
          <Label htmlFor="show-stats" className="inline text-xs">Show statistics</Label>
          <Switch
            checked={showStats}
            onCheckedChange={setShowStats}
            id="show-stats"
          />
        </div>
      </div>

      { showStats
        ? <div className="w-full max-w-6xl pr-5 pl-5 pb-5">
            <StatsCard audioHistory={audioResultHistory}></StatsCard>
          </div>
        : null
      }
    </div>
  )
}
