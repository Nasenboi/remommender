import type { Route } from "./+types/home";
import {RecorderCard} from "~/components/recorder-card";
import {Sidebar} from '~/components/ui/sidebar'

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Remommender" },
    { name: "description", content: "Start talking and we'll play the music!" },
  ];
}

export default function Home() {
  return (
    <div className="flex items-center justify-center w-full flex-1">
      <RecorderCard></RecorderCard>
    </div>
  )
}
