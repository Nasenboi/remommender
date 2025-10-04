import { AlbumCard } from "~/components/album-card"
import { useEffect, useState } from "react"
import { sendBackendRequest } from "~/lib/APIRequests"
import type { AlbumShort } from "~/lib/AudioTypes"
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationPrevious,
  PaginationNext,
  PaginationLink,
} from "~/components/ui/pagination"
import type {Route} from "../../.react-router/types/app/routes/+types/albums"
import {useSearchParams} from "react-router"
import {Spinner} from "~/components/ui/spinner"

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Album library" },
    { name: "description", content: "This page shows the albums currently saved within the library." },
  ]
}

function AlbumList({ albums, count }: { albums: AlbumShort[] | null, count: number }) {
  if (albums === null) {
    return (
      <div className="flex items-center justify-center w-full flex-1">
        <Spinner className="size-10" />
      </div>
    )
  }
  if (albums.length === 0) {
    return <p>No albums are currently in your library.</p>
  }

  return (
    <>
      <p className="ml-4 text-sm text-muted-foreground">{count} albums found.</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {albums.map((album) => (
          <AlbumCard key={album.id} album={album} />
        ))}
      </div>
    </>
  )
}

export default function AlbumOverview() {
  const [albums, setAlbums] = useState<AlbumShort[] | null>(null)
  const [numberOfAlbums, setNumberOfAlbums] = useState<number>(0)
  const pageSize = 24
  const [searchParams, setSearchParams] = useSearchParams()
  const currentPage = Math.max(parseInt(searchParams.get("page") || "1", 10), 1)
  const totalPages = Math.max(Math.ceil(numberOfAlbums / pageSize), 1)


  useEffect(() => {
    setAlbums(null)
    sendBackendRequest({
      url: `/albums/?page=${currentPage}&page_size=${pageSize}`,
      method: "GET",
    }).then((response) => {
      setAlbums(response.data.items as AlbumShort[])
      setNumberOfAlbums(response.data.count as number)
    })
  }, [currentPage])

  const handlePageChange = (page: number) => {
    setSearchParams({ page: String(page) })
  }

  const PageNumbers = () => {
    const pages = []

    for (let i = 1; i <= totalPages; i++) {

      if (i === 1 || i === totalPages || Math.abs(i - currentPage) <= 2) {
        pages.push(
          <PaginationItem key={i}>
            <PaginationLink
              isActive={i === currentPage}
              onClick={() => handlePageChange(i)}
            >
              {i}
            </PaginationLink>
          </PaginationItem>
        )
      } else if (i === currentPage - 3 || i === currentPage + 3) {
        pages.push(
          <PaginationItem key={`ellipsis-${i}`}>
            <span className="px-2 text-muted-foreground">...</span>
          </PaginationItem>
        )
      }
    }

    return pages
  }

  const FullPagination = () => {
    if(totalPages <= 1) {
      return null
    }

    return <Pagination className="mt-4">
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            onClick={() => handlePageChange(Math.max(currentPage - 1, 1))}
            aria-disabled={currentPage === 1}
          />
        </PaginationItem>

        <PageNumbers />

        <PaginationItem>
          <PaginationNext
            onClick={() => handlePageChange(Math.min(currentPage + 1, totalPages))}
            aria-disabled={currentPage === totalPages}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  }

  return (
    <div className="m-8 h-full">
      <h1 className="ml-4 text-3xl font-bold mb-4">Album Library</h1>
      <AlbumList albums={albums} count={numberOfAlbums} />
      <FullPagination />
    </div>
  )
}