import type { Route } from "./+types/home";
import {RecorderCard} from "~/components/recorder-card";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Remommender" },
    { name: "description", content: "Start talking and we'll play the music!" },
  ];
}

export default function Home() {
  return (
    <div className="flex items-center justify-center h-screen">
      <RecorderCard></RecorderCard>
    </div>
  )
}
