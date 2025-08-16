export type Song = {
  id: string
  title: string
  album: string
  artist: string
  duration_s: number
  features: SongFeatures
  genres: SongGenres
  song_url: string
  artwork_url: string
}

export type SongFeatures = {
  valence: number
  arousal: number
  authenticity: number
  timeliness: number
  complexity: number
  danceability: number
  tonal: number
  voice: number
  bpm: number
}

export type SongGenres = {
  top3_genres: {
    [genre: string]: number
  }
  all_genres: AllGenres
}

export type AllGenres = {
  Rock: number
  Pop: number
  Alternative: number
  Indie: number
  Electronic: number
  Dance: number
  "Alternative Rock": number
  Jazz: number
  Metal: number
  Chillout: number
  "Classic Rock": number
  Soul: number
  "Indie Rock": number
  Electronica: number
  Folk: number
  Chill: number
  Instrumental: number
  Punk: number
  Blues: number
  "Hard Rock": number
  Ambient: number
  Acoustic: number
  Experimental: number
  "Hip-Hop": number
  Country: number
  "Easy Listening": number
  Funk: number
  Electro: number
  "Heavy Metal": number
  "Progressive Rock": number
  RnB: number
  "Indie Pop": number
  House: number
}


