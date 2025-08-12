"use client"

import {backend} from "~/lib/APIRequests"

type AudioResult = {

}

export default class AudioRecorder {
  private mediaStream: MediaStream | null
  private mediaRecorder: MediaRecorder | null
  private audioBuffer: Blob[]

  private constructor() {
    this.mediaStream = null
    this.mediaRecorder = null
    this.audioBuffer = []
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

    this.mediaRecorder = new MediaRecorder(this.mediaStream)
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
    } catch (e) {
      console.error(e) // TODO: implement proper error handling
    }
  }

  private static async sendAudioAndGetResult(audioBuffer: Blob[], mimeType: string): Promise<void> {
    const recordedBlob = new Blob(
      audioBuffer, { type: mimeType }
    )
    const formData = new FormData()
    formData.append('file', recordedBlob)
    const response = await backend.post('/recommend/from-speech', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
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
        let result: AudioResult
        try {
          result = AudioRecorder.sendAudioAndGetResult(this.audioBuffer, this.mediaRecorder!.mimeType)
          this.clearBuffer()
          this.initMediaRecorder()
          this.mediaRecorder!.start(500)
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