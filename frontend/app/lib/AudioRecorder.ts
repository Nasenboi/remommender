"use client"

export default class AudioRecorder {
  private mediaStream: MediaStream | null
  private mediaRecorder: MediaRecorder | null
  private audioBuffer: Blob[]

  private refreshIntervalID: number | null
  private readonly refreshSeconds: number
  private recording: boolean

  private constructor(refreshSeconds: number) {
    this.mediaStream = null
    this.mediaRecorder = null
    this.audioBuffer = []
    this.refreshIntervalID = null
    this.refreshSeconds = refreshSeconds
    this.recording = false
  }

  public static async createRecorder(refreshSeconds: number): Promise<AudioRecorder> {
    const recorder = new AudioRecorder(refreshSeconds)
    await recorder.initAudio()
    return recorder
  }

  public async start(): Promise<void> {
    this.setupRefreshing()
    this.mediaRecorder?.start()
    this.recording = true
  }

  private async initAudio(): Promise<void> {
    try {
      this.mediaStream = await navigator.mediaDevices.getUserMedia(
        {audio: true}
      )
      if (this.mediaStream) {
        this.mediaRecorder = new MediaRecorder(this.mediaStream)
        this.mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) {
            this.audioBuffer.push(e.data)
          }
        }
        this.mediaRecorder.onstop = (e) => {
          this.sendAudioAndGetResult()
          this.clearBuffer()
        }
      }
    } catch (e) {
      console.error(e) // TODO: implement proper error handling
    }
  }

  private async sendAudioAndGetResult(): Promise<void> {
    const recordedBytes = await new Blob(
      this.audioBuffer, { type: 'audio/wav' }
    ).bytes()
    //TODO: implement sending audio
  }

  private clearBuffer(): void {
    this.audioBuffer = []
  }

  private setupRefreshing(): void  {
    this.refreshIntervalID = window.setInterval(this.refresh, this.refreshSeconds)
  }

  private refresh(): void {
    this.mediaRecorder?.stop()
    this.mediaRecorder?.start()
  }

  public stop(): void {
    this.mediaRecorder?.stop()
    if(this.refreshIntervalID) {
      clearInterval(this.refreshIntervalID)
      this.refreshIntervalID = null
    }
    this.mediaStream?.getTracks().forEach((track) => {
      track.stop()
    })
    this.recording = false
  }

  public isRecording(): boolean {
    return this.recording
  }
}