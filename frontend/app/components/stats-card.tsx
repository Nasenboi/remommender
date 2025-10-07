import type {AudioResult} from "~/lib/AudioRecorder"
import {Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle} from "~/components/ui/card"
import {type ChartConfig, ChartContainer, ChartTooltip } from "~/components/ui/chart"
import {Area, AreaChart, CartesianGrid, type TooltipProps, XAxis, YAxis} from "recharts"
import type {NameType, ValueType} from "recharts/types/component/DefaultTooltipContent"
import {Separator} from "~/components/ui/separator"

interface StatsCardProps {
  audioHistory: AudioResult[]
}

interface ChartDataItem {
  recommendationNumber: number
  speech: number
  song: number
  songTitle: string
}


interface TooltipWithSongProps extends TooltipProps<ValueType, NameType> {}

function TooltipWithSong({ active, payload }: TooltipWithSongProps) {
  if (!active || !payload || payload.length === 0) return null

  const recommendationNumber = payload[0].payload.recommendationNumber
  const songTitle = payload[0].payload.songTitle

  return (
    <div className="rounded-md border bg-background p-2 shadow-sm text-sm">
      <p className="font-medium text-foreground">Recommendation #{recommendationNumber}</p>
      <p className="text-muted-foreground text-xs">Song: {songTitle}</p>
      <Separator className="mt-2 mb-2"/>
      {payload.map((entry, index) => (
        <div key={`item-${index}`} className="flex justify-between gap-2 text-xs">
          <span>{entry.name}</span>
          <span>{(entry.value as number).toFixed(2)}</span>
        </div>
      ))}
    </div>
  )
}

export function StatsCard({ audioHistory }: StatsCardProps) {

  const arousalChartData: ChartDataItem[] = []
  const valenceChartData: ChartDataItem[] = []

  for(let i = audioHistory.length - 1; i >= 0; i--) {
    const result = audioHistory[i]
    arousalChartData.push({
      recommendationNumber: i+1,
      speech: result.features.arousal,
      song: result.song.features.arousal,
      songTitle: result.song.title
    })
    valenceChartData.push({
      recommendationNumber: i+1,
      speech: result.features.valence,
      song: result.song.features.valence,
      songTitle: result.song.title
    })
  }

  const arousalChartConfig = {
    speech: {
      label: "Speech",
      color: "var(--chart-1)",
    },
    song: {
      label: "Song",
      color: "var(--chart-2)",
    },
  } satisfies ChartConfig

  const valenceChartConfig = {
    speech: {
      label: "Speech",
      color: "var(--chart-3)",
    },
    song: {
      label: "Song",
      color: "var(--chart-4)",
    },
  } satisfies ChartConfig

  return (
    <div className="w-full flex flex-col md:flex-row gap-4">
      <Card className="w-full md:w-1/2">
        <CardHeader>
          <CardTitle>Arousal chart</CardTitle>
          <CardDescription>
            This chart shows the arousal values of the song and the recorded speech. The value on the right is the newest.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer config={arousalChartConfig}>
            <AreaChart
              accessibilityLayer
              data={arousalChartData}
              margin={{
                left: 12,
                right: 12,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="recommendationNumber"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                domain={[15, 1]}
              />
              <YAxis
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickCount={3}
                domain={[-1, 1]}
              />
              <ChartTooltip
                cursor={false}
                content={<TooltipWithSong />}
              />
              <Area
                dataKey="speech"
                type="linear"
                fill="var(--color-speech)"
                fillOpacity={0.4}
                stroke="var(--color-speech)"
              />
              <Area
                dataKey="song"
                type="linear"
                fill="var(--color-song)"
                fillOpacity={0.4}
                stroke="var(--color-song)"
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
        <CardFooter>
        </CardFooter>
      </Card>
      <Card className="w-full md:w-1/2">
        <CardHeader>
          <CardTitle>Valence chart</CardTitle>
          <CardDescription>
            This chart shows the valence values of the song and the recorded speech. The value on the right is the newest.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer config={valenceChartConfig}>
            <AreaChart
              accessibilityLayer
              data={valenceChartData}
              margin={{
                left: 12,
                right: 12,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="recommendationNumber"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                domain={[15, 1]}
              />
              <YAxis
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickCount={3}
                domain={[-1, 1]}
              />
              <ChartTooltip
                cursor={false}
                content={<TooltipWithSong />}
              />
              <Area
                dataKey="speech"
                type="linear"
                fill="var(--color-speech)"
                fillOpacity={0.4}
                stroke="var(--color-speech)"
              />
              <Area
                dataKey="song"
                type="linear"
                fill="var(--color-song)"
                fillOpacity={0.4}
                stroke="var(--color-song)"
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
        <CardFooter>
        </CardFooter>
      </Card>
    </div>
  )
}