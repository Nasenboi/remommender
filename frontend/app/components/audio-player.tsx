import {Pause, Volume2} from 'lucide-react'
import {Button} from '~/components/ui/button'
import React from 'react'
import {Slider} from '~/components/ui/slider'

export function AudioPlayer() {
  return (
    <div className="w-full h-20 sticky bottom-0 left-0 right-0 border-t-2 bg-background border-sidebar-border">
      <div className="absolute left-2 top-1/2 -translate-y-1/2 flex items-center h-full pt-2 pb-2">
        <div className="h-full aspect-square bg-zinc-300 dark:bg-zinc-800 mr-2"></div>
        <div>
          <p>Song name</p>
          <p className="text-zinc-700 text-xs">Artist</p>
        </div>
      </div>
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
        <Button className="rounded-full w-9 h-9" size="icon">
          <Pause className="size-5 text-white dark:text-zinc-600" />
        </Button>
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
