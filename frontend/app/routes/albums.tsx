import type { Route } from "./+types/home";
import {RecorderCard} from "~/components/recorder-card";
import {Sidebar} from '~/components/ui/sidebar'

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Album library" },
    { name: "description", content: "This page shows the albums currently saved within the library." },
  ];
}

export default function AlbumsPage() {
  return (
    <div className="flex items-center justify-center w-full flex-1">
      Album list
    </div>
  )
}
