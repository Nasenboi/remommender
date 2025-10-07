'use client'

import {sendBackendRequest} from '~/lib/APIRequests'
import type {Song, SongFeatures} from '~/lib/AudioTypes'
import { FFmpeg } from '@ffmpeg/ffmpeg'
import { fetchFile } from '@ffmpeg/util'
import coreURL from '@ffmpeg/core?url'
import wasmURL from '@ffmpeg/core/wasm?url'
import type {RecorderSettingsState} from '~/components/recorder-settings'
import {toast} from "sonner"

export type AudioResult = {
  song: Song
  features: {
    valence: number
    arousal: number
    authenticity: number | null
    timeliness: number | null
    complexity: number | null
    danceability: number | null
    tonal: number | null
    voice: number | null
    bpm: number | null
  }
  switch_probability: number
}

class AudioConverter {
  private ffmpeg: FFmpeg
  public constructor() {
    this.ffmpeg = new FFmpeg()
  }

  public async load() {
    if(!this.ffmpeg.loaded) {
      await this.ffmpeg.load({coreURL, wasmURL})
    }
  }

  public async convertToWav(audio: Blob): Promise<Blob> {
    if(!this.ffmpeg.loaded) {
      throw new Error("converter has not been loaded yet!")
    }

    const audioUrl = URL.createObjectURL(audio)
    await this.ffmpeg.writeFile("input.webm", await fetchFile(audioUrl))
    await this.ffmpeg.exec(["-i", "input.webm", "output.wav"])
    const data = (await this.ffmpeg.readFile("output.wav")) as any

    return new Blob([data.buffer], { type: "audio/wav" })
  }
}

export default class AudioRecorder {
  private mediaStream: MediaStream | null
  private mediaRecorder: MediaRecorder | null
  private audioBuffer: Blob[]
  private readonly oggSupported: boolean
  private readonly converter: AudioConverter

  private constructor() {
    this.mediaStream = null
    this.mediaRecorder = null
    this.audioBuffer = []
    this.oggSupported = MediaRecorder.isTypeSupported("audio/ogg;codecs=opus")
    this.converter = new AudioConverter()
  }

  public static async createRecorder(): Promise<AudioRecorder> {
    const recorder = new AudioRecorder()
    await recorder.initAudio()
    return recorder
  }

  public async start(): Promise<void> {
    if(!this.mediaStream!.active) {
      await this.initAudio()
    }
    this.mediaRecorder?.start(500)
  }

  private initMediaRecorder(): void {
    if(!this.mediaStream) {
      throw "MediaStream object does not exist - have you called initAudio() first?"
    }

    let options = {}
    if(this.oggSupported) {
      options = {
        mimeType: "audio/ogg;codecs=opus"
      }
    } else {
      options = {
        mimeType: "audio/webm"
      }
    }

    this.mediaRecorder = new MediaRecorder(this.mediaStream, options)
    this.mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        this.audioBuffer.push(e.data)
      }
    }
  }

  private async initAudio(): Promise<void> {
    try {
      this.mediaStream = await navigator.mediaDevices.getUserMedia(
        {audio: true}
      )
      this.initMediaRecorder()
    } catch (error: any) {
      toast.error(
        "Error while initializing audio recording", {
        description: error.message
      })
    }
    try {
      if(!this.oggSupported) {
        await this.converter.load()
      }
    } catch (error: any) {
      toast.error(
        "Error while initializing audio conversion", {
        description: error.message
      })
    }
  }

  private static buildSettingsQueryString(settings: RecorderSettingsState): string {
    const params = new URLSearchParams()
    params.append('arousal_weight', settings.arousalWeight.toString())
    params.append('valence_weight', settings.valenceWeight.toString())
    params.append('invert_arousal', settings.invertArousal.toString())
    params.append('invert_valence', settings.invertArousal.toString())
    if (settings.authenticityEnabled) params.append('authenticity', settings.authenticity.toString())
    if (settings.genreEnabled && settings.genre !== null) params.append('genre', settings.genre)
    if (settings.timelinessEnabled) params.append('timeliness', settings.timeliness.toString())
    if (settings.complexityEnabled) params.append('complexity', settings.complexity.toString())
    if (settings.danceabilityEnabled) params.append('danceability', settings.danceability.toString())
    if (settings.tonalEnabled) params.append('tonal', settings.tonal.toString())
    if (settings.voiceEnabled) params.append('voice', settings.voice.toString())
    if (settings.bpmEnabled) params.append('bpm', settings.bpm.toString())
    return params.toString()
  }

  private async sendAudioAndGetResult(audioBuffer: Blob[], mimeType: string, settings: RecorderSettingsState): Promise<AudioResult> {
    const recordedBlob = new Blob(
      audioBuffer, { type: mimeType }
    )
    let resultBlob: Blob = recordedBlob
    if(!this.oggSupported) {
      resultBlob = await this.converter.convertToWav(recordedBlob)
    }
    const formData = new FormData()
    // send audio
    formData.append('file', resultBlob)

    const queryString = AudioRecorder.buildSettingsQueryString(settings)

    const response = await sendBackendRequest<AudioResult>({
      method: 'post',
      url: `/recommend/from-speech?${queryString}`,
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  }

  private clearBuffer(): void {
    this.audioBuffer = []
  }

  public async refreshAndGetResult(settings: RecorderSettingsState): Promise<AudioResult> {
    if (!this.mediaRecorder) {
      throw "MediaRecorder object does not exist - have you called initAudio() first?"
    }

    return new Promise<AudioResult>((resolve, reject) => {
      this.mediaRecorder!.onstop = async () => {
        let resultPromise: Promise<AudioResult>
        try {
          resultPromise = this.sendAudioAndGetResult(this.audioBuffer, this.mediaRecorder!.mimeType, settings)
          this.clearBuffer()
          this.initMediaRecorder()
          this.mediaRecorder!.start(500)
          let result = await resultPromise
          resolve(result)
        } catch (_error) {
          reject(_error)
        }
      }
      this.mediaRecorder!.stop()
    })
  }

  public stop(): void {
    this.mediaRecorder?.stop()
    this.mediaStream?.getTracks().forEach((track) => {
      track.stop()
    })
  }
}