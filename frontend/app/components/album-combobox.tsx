"use client"

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"
import {Popover, PopoverContent, PopoverTrigger} from "~/components/ui/popover"
import {Button} from "~/components/ui/button"
import {Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList} from "~/components/ui/command"
import {cn} from "~/lib/utils"
import {useEffect, useState} from "react"
import {sendBackendRequest} from "~/lib/APIRequests"
import type {AlbumShort} from "~/lib/AudioTypes"

interface SetAlbumFunction {
  (album: AlbumShort | null): void
}

export interface AlbumComboboxProps {
  album: AlbumShort | null
  setAlbum: SetAlbumFunction
}


export function AlbumCombobox({ album, setAlbum }: AlbumComboboxProps) {
  const [open, setOpen] = useState(false)
  const [value, setValue] = useState(album?.id ? album.id : "")

  const [albums, setAlbums] = useState<AlbumShort[]>([])

  useEffect(() => {
    sendBackendRequest<AlbumShort[]>({
      url: "/albums/all",
      method: "GET"
    }).then((res) => {
      setAlbums(res.data)
    })
  }, [])

  const searchAlbums = (value: string, search: string, keywords: string[] | undefined) => {
    // The toLowerCase is necessary to make searching case-insensitive
    if(keywords?.join(' ').toLowerCase().includes(search.toLowerCase())) {
      return 1
    }
    return 0
  }

  const handleValueChange = (currentValue: string) => {
    setValue(currentValue)
    const albumSearchResult = albums.find((a) => a.id === currentValue)
    if(albumSearchResult) {
      setAlbum(albumSearchResult)
    }
    setOpen(false)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-xl justify-between"
        >
          {value
            ? `${albums.find((a) => a.id === value)?.artist} - ${albums.find((a) => a.id === value)?.album}`
            : "Select album..."}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-xl p-0">
        <Command
          filter={searchAlbums}
        >
          <CommandInput placeholder="Search albums..." className="h-9" />
          <CommandList>
            <CommandEmpty>No albums found.</CommandEmpty>
            <CommandGroup>
              {albums.map((album) => (
                <CommandItem
                  key={album.id}
                  value={album.id}
                  onSelect={handleValueChange}
                  keywords={[album.album, album.artist]}
                >
                  {album.artist} - {album.album}
                  <Check
                    className={cn(
                      "ml-auto",
                      value === album.id ? "opacity-100" : "opacity-0"
                    )}
                  />
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
