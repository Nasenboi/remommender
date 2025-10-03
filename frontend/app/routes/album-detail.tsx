import type { Route } from "./+types/home";
import {RecorderCard} from "~/components/recorder-card";
import {Sidebar} from '~/components/ui/sidebar'

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Album details" },
    { name: "description", content: "This page shows the contents of an album" },
  ];
}

export default function AlbumDetailPage() {
  return (
    <div className="flex items-center justify-center w-full flex-1">
      Album detail page
    </div>
  )
}
