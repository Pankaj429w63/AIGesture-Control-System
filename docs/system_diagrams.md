# Diagrams

## System Architecture (Mermaid)
```mermaid
graph LR
  Camera[Webcam] -->|frames| Detection[Hand Tracker (MediaPipe)]
  Detection -->|landmarks| Inference[Model Predictor]
  Inference -->|gesture| Controller[Controls (volume, media, brightness)]
  Camera -->|face frames| Auth[Face Auth]
  Auth -->|authorized| Inference
  Training -->|model| Inference
```

## Data Flow
- Capture frames → extract landmarks → flatten → model → action

## UML Class Diagram (text)
- `HandTracker`: process_frame()
- `InferenceEngine`: predict()
- `VolumeController`: increase(), decrease(), mute()
- `BrightnessController`: increase(), decrease()
- `MediaController`: play_pause(), next_track()
