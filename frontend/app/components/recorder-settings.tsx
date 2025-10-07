"use client"

import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger
} from '~/components/ui/sheet'
import { Button } from '~/components/ui/button'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Switch } from '~/components/ui/switch'
import { Slider } from '~/components/ui/slider'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '~/components/ui/select'
import React from 'react'
import {ArrowLeft, Info, Settings} from 'lucide-react'
import {Separator} from "~/components/ui/separator"
import {sendBackendRequest} from "~/lib/APIRequests"
import {toast} from "sonner"
import {Tooltip, TooltipContent, TooltipTrigger} from "~/components/ui/tooltip"

export enum RefreshOption {
  FIVE = 5,
  TEN = 10,
  FIFTEEN = 15,
  TWENTY = 20,
  THIRTY = 30
}

export enum Genre {
  ROCK = "Rock",
  POP = "Pop",
  ALTERNATIVE = "Alternative",
  INDIE = "Indie",
  ELECTRONIC = "Electronic",
  DANCE = "Dance",
  ALTERNATIVE_ROCK = "Alternative Rock",
  JAZZ = "Jazz",
  METAL = "Metal",
  CHILLOUT = "Chillout",
  CLASSIC_ROCK = "Classic Rock",
  SOUL = "Soul",
  INDIE_ROCK = "Indie Rock",
  ELECTRONICA = "Electronica",
  FOLK = "Folk",
  CHILL = "Chill",
  INSTRUMENTAL = "Instrumental",
  PUNK = "Punk",
  BLUES = "Blues",
  HARD_ROCK = "Hard Rock",
  AMBIENT = "Ambient",
  ACOUSTIC = "Acoustic",
  EXPERIMENTAL = "Experimental",
  HIP_HOP = "Hip-Hop",
  COUNTRY = "Country",
  EASY_LISTENING = "Easy Listening",
  FUNK = "Funk",
  ELECTRO = "Electro",
  HEAVY_METAL = "Heavy Metal",
  PROGRESSIVE_ROCK = "Progressive Rock",
  RNB = "RnB",
  INDIE_POP = "Indie Pop",
  HOUSE = "House"
}

export interface RecorderSettingsState {
  refreshTime: RefreshOption
  switchThreshold: number
  arousalWeight: number
  valenceWeight: number
  invertArousal: boolean
  invertValence: boolean
  sessionEnabled: boolean
  genreEnabled: boolean
  genre: Genre | null
  authenticityEnabled: boolean
  authenticity: number
  timelinessEnabled: boolean
  timeliness: number
  complexityEnabled: boolean
  complexity: number
  danceabilityEnabled: boolean
  danceability: number
  tonalEnabled: boolean
  tonal: number
  voiceEnabled: boolean
  voice: number
  bpmEnabled: boolean
  bpm: number
}

export interface RecorderSettingsProps {
  settings: RecorderSettingsState
  setSettings: React.Dispatch<React.SetStateAction<RecorderSettingsState>>
}

export function RecorderSettings({ settings, setSettings }: RecorderSettingsProps) {

  const refreshOptions = Object.values(RefreshOption).filter(
    (v) => typeof v === "number"
  ) as RefreshOption[]
  const genres = Object.values(Genre)

  function setWeights(value: number[]) {
    setSettings(s => ({ ...s, arousalWeight: 1 - value[0], valenceWeight: value[0] }))
  }

  function handleSessionChange(checked: boolean): void {
    if(checked) {
      sendBackendRequest({
        url: "/session/start",
        method: "POST",
      }).then((response) => {
        toast("A new session was started.")
      })
    } else {
      sendBackendRequest({
        url: "/session/clear",
        method: "POST",
      }).then(() => sendBackendRequest({
        url: "/session/end",
        method: "POST",
      })).then((response) => {
        toast("The session was terminated.")
      })
    }

    setSettings(s => ({
      ...s,
      sessionEnabled: checked
    }))
  }

  function handleClearSession() {
    if(settings.sessionEnabled) {
      sendBackendRequest({
        url: "/session/clear",
        method: "POST",
      }).then((response) => {
        toast("The session was cleared successfully.")
      })
    }
  }

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" className="text-sm"><Settings />Adjust settings</Button>
      </SheetTrigger>
      <SheetContent className="overflow-y-auto">
        <SheetHeader>
          <SheetTitle>Recommendation Settings</SheetTitle>
          <SheetDescription>
            Adjust settings and filter recommendations based on your preferences.
            The switches enable or disable the respective filter.
            Changes are applied upon the next refresh.
          </SheetDescription>
        </SheetHeader>

        <div className="grid flex-1 auto-rows-min gap-6 px-4">
          <div className="grid gap-3">
            <Label>Refresh Time (seconds)</Label>
            <Select value={settings.refreshTime.toString()} onValueChange={(val) => setSettings(s => ({
              ...s,
              refreshTime: Number(val) as RefreshOption
            }))}>
              <SelectTrigger>
                <SelectValue placeholder="Select refresh time..." />
              </SelectTrigger>
              <SelectContent>
                {refreshOptions.map((option) => (
                  <SelectItem key={option} value={option.toString()}>
                    {option}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <div>
                <Label className="inline">Switch Threshold</Label>
                <Tooltip>
                  <TooltipTrigger>
                    <Info className="inline text-muted-foreground size-5 ml-2"/>
                  </TooltipTrigger>
                  <TooltipContent>
                    The backend calculates how likely the currently playing song should change. This is based on the<br />
                    difference between the currently recorded emotion and the previously recorded emotion, i.e. when<br />
                    the emotion changes drastically, it is more likely that the song should change and the value is<br />
                    therefore higher. This switch probability lies between 0 and 100%. With the slider below, you can<br />
                    determine at which switch probability value the song should change.
                  </TooltipContent>
                </Tooltip>
              </div>

              <span className="text-sm text-muted-foreground w-[50px] text-right">
                {(settings.switchThreshold * 100).toFixed(0)}%
              </span>
            </div>
            <Slider
              min={0}
              max={1}
              step={0.01}
              value={[settings.switchThreshold]}
              onValueChange={(val) => setSettings(s => ({ ...s, switchThreshold: val[0] }))}
            />
          </div>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <Label>Arousal / Valence Weight</Label>
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground w-[100px] text-right">
                  Arousal: {settings.arousalWeight.toFixed(2)},<br />
                  Valence: {settings.valenceWeight.toFixed(2)}
                </span>
              </div>
            </div>
            <Slider
              min={0}
              max={1}
              step={0.01}
              value={[settings.valenceWeight]}
              onValueChange={(val) => setWeights(val)}
            />
          </div>

          <div className="flex justify-between mt-4">
            <div>
              <Label>Invert arousal</Label>
              <p className="text-xs text-muted-foreground mt-4 mb-4">This will invert the arousal value, e.g., when your
                speech yields a low arousal value, a song with a high arousal value will be recommended.</p>
            </div>
            <Switch
              checked={settings.invertArousal}
              onCheckedChange={(checked) => {
                setSettings(s => ({
                  ...s,
                  invertArousal: checked
                }))
              }}
            />
          </div>

          <div className="flex justify-between mt-2">
            <div>
              <Label>Invert valence</Label>
              <p className="text-xs text-muted-foreground mt-4 mb-4">This will invert the valence value, e.g., when your
                speech yields a low valence value, a song with a high valence value will be recommended.</p>
            </div>
            <Switch
              checked={settings.invertValence}
              onCheckedChange={(checked) => {
                setSettings(s => ({
                  ...s,
                  invertValence: checked
                }))
              }}
            />
          </div>

          <Separator className="mt-2 mb-2" />

          <div className="flex justify-between">
            <div>
              <Label>Session</Label>
              <p className="text-xs text-muted-foreground mt-4 mb-4">Turning this setting on will ensure that no song is
              played twice during this session.</p>
              <Button
                variant="outline"
                onClick={handleClearSession}
                disabled={!settings.sessionEnabled}
                className="text-xs p-3"
              >
                Clear session
              </Button>
            </div>
            <Switch
              checked={settings.sessionEnabled}
              onCheckedChange={handleSessionChange}
            />
          </div>

          <Separator className="mt-2 mb-2" />

          <h2 className="text-xl font-semibold tracking-tight">Filters</h2>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <Label>Genre</Label>
              <Switch
                checked={settings.genreEnabled}
                onCheckedChange={(checked) => {
                  setSettings(s => ({
                    ...s,
                    genreEnabled: checked,
                    genre: checked ? s.genre : null
                  }))
                }}
              />
            </div>
            <Select
              disabled={!settings.genreEnabled}
              value={settings.genre ?? ''}
              onValueChange={(val) => setSettings(s => ({ ...s, genre: val as Genre }))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select genre..." />
              </SelectTrigger>
              <SelectContent className="max-h-60 overflow-y-auto">
                {genres.map((g) => (
                  <SelectItem key={g} value={g}>
                    {g}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <Label>Authenticity</Label>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground w-[50px] text-right">
                  {settings.authenticity.toFixed(2)}
                </span>
                <Switch
                  checked={settings.authenticityEnabled}
                  onCheckedChange={(checked) => {
                    setSettings(s => ({
                      ...s,
                      authenticityEnabled: checked,
                      authenticity: checked ? s.authenticity : 0
                    }))
                  }}
                />
              </div>
            </div>
            <Slider
              min={-1}
              max={1}
              step={0.01}
              value={[settings.authenticity]}
              onValueChange={(val) => setSettings(s => ({ ...s, authenticity: val[0] }))}
              disabled={!settings.authenticityEnabled}
            />
          </div>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <Label>Timeliness</Label>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground w-[50px] text-right">
                  {settings.timeliness.toFixed(2)}
                </span>
                <Switch
                  checked={settings.timelinessEnabled}
                  onCheckedChange={(checked) => {
                    setSettings(s => ({
                      ...s,
                      timelinessEnabled: checked,
                      timeliness: checked ? s.timeliness : 0
                    }))
                  }}
                />
              </div>
            </div>
            <Slider
              min={-1}
              max={1}
              step={0.01}
              value={[settings.timeliness]}
              onValueChange={(val) => setSettings(s => ({ ...s, timeliness: val[0] }))}
              disabled={!settings.timelinessEnabled}
            />
          </div>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <Label>Complexity</Label>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground w-[50px] text-right">
                  {settings.complexity.toFixed(2)}
                </span>
                <Switch
                  checked={settings.complexityEnabled}
                  onCheckedChange={(checked) => {
                    setSettings(s => ({
                      ...s,
                      complexityEnabled: checked,
                      complexity: checked ? s.complexity : 0
                    }))
                  }}
                />
              </div>
            </div>
            <Slider
              min={-1}
              max={1}
              step={0.01}
              value={[settings.complexity]}
              onValueChange={(val) => setSettings(s => ({ ...s, complexity: val[0] }))}
              disabled={!settings.complexityEnabled}
            />
          </div>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <Label>Danceability</Label>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground w-[50px] text-right">
                  {settings.danceability.toFixed(2)}
                </span>
                <Switch
                  checked={settings.danceabilityEnabled}
                  onCheckedChange={(checked) => {
                    setSettings(s => ({
                      ...s,
                      danceabilityEnabled: checked,
                      danceability: checked ? s.danceability : 0
                    }))
                  }}
                />
              </div>
            </div>
            <Slider
              min={-1}
              max={1}
              step={0.01}
              value={[settings.danceability]}
              onValueChange={(val) => setSettings(s => ({ ...s, danceability: val[0] }))}
              disabled={!settings.danceabilityEnabled}
            />
          </div>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <Label>Tonal</Label>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground w-[50px] text-right">
                  {settings.tonal.toFixed(2)}
                </span>
                <Switch
                  checked={settings.tonalEnabled}
                  onCheckedChange={(checked) => {
                    setSettings(s => ({
                      ...s,
                      tonalEnabled: checked,
                      tonal: checked ? s.tonal : 0
                    }))
                  }}
                />
              </div>
            </div>
            <Slider
              min={-1}
              max={1}
              step={0.01}
              value={[settings.tonal]}
              onValueChange={(val) => setSettings(s => ({ ...s, tonal: val[0] }))}
              disabled={!settings.tonalEnabled}
            />
          </div>

          <div className="grid gap-3">
            <div className="flex justify-between items-center">
              <Label>Voice</Label>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground w-[50px] text-right">
                  {settings.voice.toFixed(2)}
                </span>
                <Switch
                  checked={settings.voiceEnabled}
                  onCheckedChange={(checked) => {
                    setSettings(s => ({
                      ...s,
                      voiceEnabled: checked,
                      voice: checked ? s.voice : 0
                    }))
                  }}
                />
              </div>
            </div>
            <Slider
              min={-1}
              max={1}
              step={0.01}
              value={[settings.voice]}
              onValueChange={(val) => setSettings(s => ({ ...s, voice: val[0] }))}
              disabled={!settings.voiceEnabled}
            />
          </div>

          <div className="grid gap-3 mt-3">
            <div className="flex justify-between items-center">
              <Label>BPM</Label>
              <Switch
                checked={settings.bpmEnabled}
                onCheckedChange={(checked) => {
                  setSettings(s => ({
                    ...s,
                    bpmEnabled: checked,
                    bpm: checked ? s.bpm : 120
                  }))
                }}
              />
            </div>
            <Input
              type="number"
              min={40}
              max={200}
              value={settings.bpmEnabled ? settings.bpm : ''}
              placeholder="..."
              onChange={(e) => setSettings(s => ({ ...s, bpm: Number(e.target.value) }))}
              disabled={!settings.bpmEnabled}
            />
          </div>
        </div>

        <SheetFooter>
          <SheetClose asChild>
            <Button variant="outline">Close settings</Button>
          </SheetClose>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  )
}
