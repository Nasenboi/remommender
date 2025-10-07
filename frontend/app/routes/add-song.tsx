import React, {useState} from 'react'
import {useForm} from 'react-hook-form'
import {zodResolver} from '@hookform/resolvers/zod'
import {z} from 'zod'
import {Label} from "~/components/ui/label"
import {Input} from "~/components/ui/input"
import {Tabs, TabsContent, TabsList, TabsTrigger} from "~/components/ui/tabs"
import {Button} from "~/components/ui/button"
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "~/components/ui/card"
import type {AlbumShort} from "~/lib/AudioTypes"
import {AlbumCombobox} from "~/components/album-combobox"
import {sendBackendRequest} from "~/lib/APIRequests"
import {toast} from "sonner"
import {Spinner} from "~/components/ui/spinner"
import {useNavigate} from "react-router"
import type {Route} from "../../.react-router/types/app/routes/+types/home"

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Add song" },
    { name: "description", content: "Add a new song to the library." },
  ];
}

const audioFileTypes = ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/aac']
const imageFileTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/tiff']

const albumSchema = z.object({
  title: z
    .string()
    .min(1, 'Album title is required')
    .max(255, 'Album title cannot exceed 255 characters'),
  artist: z
    .string()
    .min(1, 'Album artist is required')
    .max(255, 'Album artist cannot exceed 255 characters'),
  cover: z
    .custom<File>((file) => file instanceof File && imageFileTypes.includes(file.type), {
      message: 'Invalid image file'
    })
})

const formSchema = z.object({
  songTitle: z.string().min(1).max(255),
  albumOption: z.discriminatedUnion('type', [
    z.object({
      type: z.literal('existing'),
      albumId: z.string()
    }),
    z.object({
      type: z.literal('new'),
      albumData: albumSchema
    })
  ]),
  artist: z.string().max(255),
  audioFile: z
    .custom<File>((file) => file instanceof File && audioFileTypes.includes(file.type), {
      message: 'Invalid audio file'
    })
})

type FormValues = z.infer<typeof formSchema>

export default function UploadSongPage() {
  const [albumTab, setAlbumTab] = useState<'existing' | 'new'>('existing')
  const [existingAlbum, setExistingAlbum] = useState<AlbumShort | null>(null)
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false)

  // For redirecting the user after the song has been uploaded
  const navigate = useNavigate()

  const {
    register,
    control,
    handleSubmit,
    setValue,
    formState: {errors}
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      albumOption: {
        type: 'existing',
        albumId: ''
      }
    }
  })

  const onSubmit = async (data: FormValues) => {
    // This will show a spinner and set the submit button to disabled.
    setIsSubmitting(true)

    let albumId: string

    // If a new album has to be created, create the album first
    if (data.albumOption.type === 'new') {
      const albumFormData = new FormData()
      albumFormData.append("album_name", data.albumOption.albumData.title)
      albumFormData.append("artist", data.albumOption.albumData.artist)
      albumFormData.append("artwork_file", data.albumOption.albumData.cover)
      const response = await sendBackendRequest({
        method: 'post',
        url: '/albums/',
        data: albumFormData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      albumId = response.data.id
    } else {
      // If we're using an existing album, use its album id for the new song instead
      if(!existingAlbum) {
        toast.error("Please select an album.")
        setIsSubmitting(false)
        return
      }
      albumId = data.albumOption.albumId
    }

    // Now, we can upload the song itself
    const songFormData = new FormData()
    songFormData.append("title", data.songTitle)

    // If no artist is given, use the artist from the new / existing album
    if(data.artist == "" && data.albumOption.type === 'new') {
      songFormData.append("artist", data.albumOption.albumData.artist)
    } else if(data.artist == "" && data.albumOption.type === 'existing' && existingAlbum) {
      songFormData.append("artist", existingAlbum.artist)
    } else {
      songFormData.append("artist", data.artist)
    }

    songFormData.append("album_id", albumId)
    songFormData.append("audio_file", data.audioFile)

    const response = await sendBackendRequest({
      method: 'post',
      url: '/songs/',
      data: songFormData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    toast.success(`The song "${data.songTitle}" was uploaded successfully.`)

    setIsSubmitting(false)

    // Redirect the user to the album
    navigate(`/library/albums/${albumId}`)

  }

  function handleAlbumTabChange(
    tab: 'existing' | 'new'
  ) {
    setAlbumTab(tab)
    if (tab === 'new') {
      setValue('albumOption', {
        type: 'new',
        albumData: {
          title: '',
          artist: '',
          cover: undefined as unknown as File, // empty placeholder (ugly, i know)
        }
      });
    } else {
      setValue('albumOption', {
        type: 'existing',
        albumId: existingAlbum?.id ?? '',
      })
    }
  }

  return (
    <div className="flex justify-center w-full flex-1">
      <div className="xl:w-6xl w-full max-w-full p-6 space-y-6">
        <h1 className="text-2xl font-bold">Upload New Song</h1>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Song Title */}
          <div className="space-y-2">
            <Label htmlFor="songTitle">Song Title</Label>
            <Input id="songTitle" {...register('songTitle')} />
            {errors.songTitle && <p className="text-red-500 text-sm">{errors.songTitle.message}</p>}
          </div>

          <Tabs defaultValue="existing" onValueChange={(val) => handleAlbumTabChange(val as 'existing' | 'new')}>
            <TabsList>
              <TabsTrigger value="existing">Select Album</TabsTrigger>
              <TabsTrigger value="new">Create Album</TabsTrigger>
            </TabsList>

            <TabsContent value="existing">
              <Card>
                <CardHeader>
                  <CardTitle>Choose existing album</CardTitle>
                  <CardDescription>
                    Select an existing album which this song belongs to.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Label>Album</Label>
                  <AlbumCombobox
                    album={existingAlbum}
                    setAlbum={(album) => {
                      setExistingAlbum(album)
                      setValue('albumOption', {
                        type: 'existing',
                        albumId: album?.id ?? ''
                      })
                    }}
                  />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="new">
              <Card>
                <CardHeader>
                  <CardTitle>Create new album</CardTitle>
                  <CardDescription>
                    Add the details of the album which this song belongs to below.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Label>Album Title</Label>
                  <Input
                    {...register('albumOption.albumData.title')}
                    placeholder="Enter album title"
                  />
                  {(errors.albumOption as any)?.albumData?.title && (
                    <p className="text-red-500 text-sm">
                      {(errors.albumOption as any).albumData.title.message}
                    </p>
                  )}

                  <Label>Album Artist</Label>
                  <Input
                    {...register('albumOption.albumData.artist')}
                    placeholder="Enter album artist"
                  />
                  {(errors.albumOption as any)?.albumData?.artist && (
                    <p className="text-red-500 text-sm">
                      {(errors.albumOption as any).albumData.artist.message}
                    </p>
                  )}

                  <Label>Album Cover</Label>
                  <Input
                    type="file"
                    accept={imageFileTypes.join(',')}
                    onChange={(e) =>
                      setValue(
                        'albumOption.albumData.cover',
                        e.target.files?.[0] || (null as any)
                      )
                    }
                  />
                  {console.log(errors.albumOption)}
                  {(errors.albumOption as any)?.albumData?.cover && (
                    <p className="text-red-500 text-sm">
                      {(errors.albumOption as any).albumData.cover.message}

                    </p>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          <div className="space-y-4">
            <div>
              <Label htmlFor="artist">Song Artist</Label>
              <p className="text-xs text-muted-foreground mt-3">Optional if the song artist matches the album artist</p>
            </div>
            <Input id="artist" {...register('artist')} />
            {errors.artist && <p className="text-red-500 text-sm">{errors.artist.message}</p>}
          </div>

          <div className="space-y-4">
            <Label htmlFor="audioFile">Audio File</Label>
            <Input
              type="file"
              accept={audioFileTypes.join(',')}
              onChange={(e) => setValue('audioFile', e.target.files?.[0] || (null as any))}
            />
            {errors.audioFile && (
              <p className="text-red-500 text-sm">{errors.audioFile.message}</p>
            )}
          </div>

          <Button type="submit" className="mt-4" disabled={isSubmitting}>
            Upload Song
          </Button>

          {isSubmitting
            ? <Spinner className="ml-4 size-10 inline"/>
            : null}

        </form>
      </div>
    </div>
  )
}
