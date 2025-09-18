'use client'

import {backend} from '~/lib/APIRequests'
import type {Song} from '~/lib/AudioTypes'
import type {AxiosResponse} from 'axios'
import { FFmpeg } from '@ffmpeg/ffmpeg'
import { fetchFile } from '@ffmpeg/util'
import coreURL from '@ffmpeg/core?url'
import wasmURL from '@ffmpeg/core/wasm?url'

type AudioResult = {
  song: Song
  features: any //TODO
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
      if(!this.oggSupported) {
        await this.converter.load()
      }
    } catch (e) {
      console.error(e) // TODO: implement proper error handling
    }
  }

  private async sendAudioAndGetResult(audioBuffer: Blob[], mimeType: string): Promise<AudioResult> {
    const recordedBlob = new Blob(
      audioBuffer, { type: mimeType }
    )
    let resultBlob: Blob = recordedBlob
    if(!this.oggSupported) {
      resultBlob = await this.converter.convertToWav(recordedBlob)
    }
    const formData = new FormData()
    formData.append('file', resultBlob)
    const response = await backend.post<FormData, AxiosResponse<AudioResult>>('/recommend/from-speech', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  }

  private clearBuffer(): void {
    this.audioBuffer = []
  }

  public async refreshAndGetResult(): Promise<AudioResult> {
    if (!this.mediaRecorder) {
      throw "MediaRecorder object does not exist - have you called initAudio() first?"
    }

    return new Promise<AudioResult>((resolve, reject) => {
      this.mediaRecorder!.onstop = async () => {
        let resultPromise: Promise<AudioResult>
        try {
          resultPromise = this.sendAudioAndGetResult(this.audioBuffer, this.mediaRecorder!.mimeType)
          this.clearBuffer()
          this.initMediaRecorder()
          this.mediaRecorder!.start(500)
          let result = await resultPromise
          resolve(result)
        } catch (error) {
          console.error("Error sending audio:", error)
          reject(error)
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