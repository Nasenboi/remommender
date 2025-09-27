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
import {Settings} from 'lucide-react'

export enum RefreshOption {
  FIVE = 5,
  TEN = 10,
  FIFTEEN = 15,
  TWENTY = 20,
  THIRTY = 30
}

export enum Genre {
  ROCK = "rock",
  POP = "pop",
  ALTERNATIVE = "alternative",
  INDIE = "indie",
  ELECTRONIC = "electronic",
  DANCE = "dance",
  ALTERNATIVE_ROCK = "alternative rock",
  JAZZ = "jazz",
  METAL = "metal",
  CHILLOUT = "chillout",
  CLASSIC_ROCK = "classic rock",
  SOUL = "soul",
  INDIE_ROCK = "indie rock",
  ELECTRONICA = "electronica",
  FOLK = "folk",
  CHILL = "chill",
  INSTRUMENTAL = "instrumental",
  PUNK = "punk",
  BLUES = "blues",
  HARD_ROCK = "hard rock",
  AMBIENT = "ambient",
  ACOUSTIC = "acoustic",
  EXPERIMENTAL = "experimental",
  HIP_HOP = "Hip-Hop",
  COUNTRY = "country",
  EASY_LISTENING = "easy listening",
  FUNK = "funk",
  ELECTRO = "electro",
  HEAVY_METAL = "heavy metal",
  PROGRESSIVE_ROCK = "Progressive rock",
  RNB = "rnb",
  INDIE_POP = "indie pop",
  HOUSE = "House"
}

export interface RecorderSettingsState {
  refreshTime: RefreshOption
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
