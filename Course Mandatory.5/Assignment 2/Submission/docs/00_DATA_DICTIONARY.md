# Data Dictionary

This document provides detailed descriptions of all variables in the Rolling Stones Spotify dataset, as referenced in the data dictionary XLSX file.

## Audio Features
- **acousticness**: Confidence measure (0.0 to 1.0) indicating if a track is acoustic. 1.0 represents high confidence.
- **danceability**: Measure (0.0 to 1.0) of track's suitability for dancing based on tempo, rhythm stability, beat strength, and regularity.
- **energy**: Measure (0.0 to 1.0) of intensity and activity. High energy tracks are typically fast, loud, and noisy.
- **instrumentalness**: Predicts absence of vocals (0.0 to 1.0). Values above 0.5 likely indicate instrumental tracks.
- **liveness**: Detects presence of audience (0.0 to 1.0). Values above 0.8 strongly suggest live recording.
- **loudness**: Overall track loudness in decibels (dB). Values typically range from -60 to 0 dB.
- **speechiness**: Detects spoken words (0.0 to 1.0):
  - > 0.66: Likely entirely spoken
  - 0.33-0.66: May contain both music and speech
  - < 0.33: Likely music without speech
- **tempo**: Estimated tempo in beats per minute (BPM)
- **valence**: Musical positivity measure (0.0 to 1.0). Higher values indicate more positive sound.

## Track Metadata
- **name**: Song title
- **album**: Album name
- **release_date**: Album release date
- **track_number**: Song's position in album
- **id**: Unique Spotify ID
- **uri**: Spotify URI for the track
- **popularity**: Song popularity score (0-100)
- **duration_ms**: Track duration in milliseconds

## Usage in Analysis
This data dictionary is used to:
1. Interpret feature meanings correctly in EDA
2. Guide feature selection for clustering
3. Provide context for cluster interpretation
4. Ensure accurate reporting of results

Reference: Data dictionary from `1722506509_datadictionarycreatingcohortsofsongs.xlsx`
