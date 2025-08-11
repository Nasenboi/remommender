"use client"

import {backend} from "~/lib/APIRequests"

type AudioResult = {

}

export default class AudioRecorder {
  private mediaStream: MediaStream | null
  private mediaRecorder: MediaRecorder | null
  private audioBuffer: Blob[]
  private recording: boolean

  private constructor() {
    this.mediaStream = null
    this.mediaRecorder = null
    this.audioBuffer = []
    this.recording = false
  }

  public static async createRecorder(): Promise<AudioRecorder> {
    const recorder = new AudioRecorder()
    await recorder.initAudio()
    return recorder
  }

  public async start(): Promise<void> {
    this.mediaRecorder?.start(500)
    this.recording = true
  }

  private async initAudio(): Promise<void> {
    try {
      this.mediaStream = await navigator.mediaDevices.getUserMedia(
        {audio: true}
      )
      this.mediaRecorder = new MediaRecorder(this.mediaStream)
      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          this.audioBuffer.push(e.data)
        }
      }
    } catch (e) {
      console.error(e) // TODO: implement proper error handling
    }
  }

  private static async sendAudioAndGetResult(audioBuffer: Blob[], mimeType: string): Promise<void> {
    const recordedBlob = new Blob(
      audioBuffer, { type: mimeType }
    )
    const url = URL.createObjectURL(recordedBlob);
    const audio = document.createElement('audio');
    audio.src = url;
    audio.controls = true;
    document.body.appendChild(audio);
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

  public async refreshAndGetResult(): Promise<void> {
    if(!this.mediaRecorder) {
      throw "MediaRecorder object does not exist - have you called initAudio() first?"
    }

    this.mediaRecorder.stop()
    const result = AudioRecorder.sendAudioAndGetResult(this.audioBuffer, this.mediaRecorder.mimeType)
    this.clearBuffer()
    this.mediaRecorder.start(500)
    return await result
  }

  public stop(): void {
    this.mediaRecorder?.stop()
    this.mediaStream?.getTracks().forEach((track) => {
      track.stop()
    })
    this.recording = false
  }

  public isRecording(): boolean {
    return this.recording
  }
}