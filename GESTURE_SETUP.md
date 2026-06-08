# 🎯 Hand Gesture Control System - Setup & Run Guide

## System Ready ✓

Your hand gesture system is configured with these mappings:

| Gesture | Action | Purpose |
|---------|--------|---------|
| 👍 Thumbs Up | `volume_increase` | Raise system volume |
| 👎 Thumbs Down | `volume_decrease` | Lower system volume |
| ✊ Fist | `mute` | Toggle mute |
| ✋ Open Palm | `play_pause` | Play/pause media |
| ✌️ Victory | `next_track` | Next song |
| 🤟 Three Fingers | `previous_track` | Previous song |
| 👌 OK | `brightness_increase` | Increase screen brightness |
| 👌 Closed OK | `brightness_decrease` | Decrease screen brightness |

---

## ⚡ Quick Start (3 steps)

### Step 1: Train the Model
```powershell
python scripts/run_train_and_verify.py
```
✓ Trains RandomForest/SVM/KNN/MLP and saves best model  
✓ Creates confusion matrix visualization  
✓ Output: `models/trained_models/best_model.joblib`

### Step 2: Run the Demo
```powershell
python main.py --no-auth
```
✓ Opens camera window  
✓ Detects hand gestures in real-time  
✓ Executes volume/brightness/media actions  
✓ Press `Q` to quit

### Step 3: Test Without Camera (Optional)
```powershell
python scripts/auto_demo.py --delay 1.5
```
✓ Simulates all gestures automatically  
✓ No camera required  
✓ Tests all controllers

---

## 🧪 Manual Testing (Keyboard Control)

For troubleshooting controllers without ML:

```powershell
python scripts/manual_control.py
```

**Key Controls:**
- `U` → Volume Up
- `J` → Volume Down
- `M` → Mute
- `I` → Brightness Up
- `K` → Brightness Down
- `Q` → Quit

---

## 📋 Full Command Reference

### Training
```bash
# Train and verify model
python scripts/run_train_and_verify.py

# Check training logs
cat logs/app.log | grep "Training"
```

### Running Main App
```bash
# With camera + auth
python main.py

# With camera, no auth
python main.py --no-auth

# With custom MediaPipe model
python main.py --mp-model models/mediapipe/hand_landmarker.task --no-auth
```

### Testing
```bash
# Automated gesture demo
python scripts/auto_demo.py --delay 1.5

# Manual keyboard test
python scripts/manual_control.py

# Download MediaPipe model (if needed)
python scripts/download_hand_landmarker.py
```

---

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
# Gesture recognition settings
model:
  confidence_threshold: 0.65  # Min confidence to trigger action
  gesture_cooldown_seconds: 0.5  # Cooldown between gestures

# Change gesture-to-action mapping
controls:
  gestures:
    thumbs_up: volume_increase
    ok: brightness_increase
    # Add custom mappings here...

# Enable/disable face authentication
auth:
  face_required: false
```

---

## 🐛 Troubleshooting

### Volume not changing?
1. Run manual test: `python scripts/manual_control.py`
2. Press `U` - check console for volume logs
3. Verify Windows audio permissions

### Brightness not changing?
- Check system brightness control is enabled
- Run: `python scripts/manual_control.py` → Press `I`

### Camera not detected?
- Verify webcam is plugged in
- Check Windows camera permissions
- Run: `python -c "import cv2; print(cv2.__version__)"`

### No model file?
- Run: `python scripts/run_train_and_verify.py` first
- Ensure dataset has landmark data
- Check: `models/trained_models/best_model.joblib`

---

## 📊 Project Structure

```
AI-Gesture-Control-System/
├── main.py                          # Main gesture recognition app
├── config/config.yaml               # Configuration file
├── dataset/gesture_landmarks.csv    # Training data
├── models/
│   ├── mediapipe/hand_landmarker.task
│   └── trained_models/best_model.joblib
├── scripts/
│   ├── run_train_and_verify.py     # Train model
│   ├── manual_control.py            # Keyboard test
│   └── auto_demo.py                 # Automated demo
├── src/
│   ├── gesture_detection/           # Hand tracking
│   ├── inference/                   # ML prediction
│   ├── controls/                    # Volume/Brightness/Media
│   ├── training/                    # Training pipeline
│   └── preprocessing/               # Data loading
└── logs/app.log                     # Runtime logs
```

---

## 🎓 Understanding the Flow

1. **Capture**: Camera captures hand frame
2. **Detect**: MediaPipe extracts 21 hand landmarks (normalized to 63-dim vector)
3. **Predict**: Trained ML model predicts gesture label + confidence
4. **Execute**: If confidence > threshold, execute mapped action
5. **Cooldown**: Wait 0.5s before next gesture
6. **Control**: Volume/Brightness/Media controller updates system state
7. **Feedback**: Console logs and on-screen display show what happened

---

## ✨ Features

✓ Real-time hand gesture recognition (30+ FPS)  
✓ Multi-classifier training (RandomForest/SVM/KNN/MLP)  
✓ Automatic best model selection (by F1 score)  
✓ Windows 10/11 system control integration  
✓ Optional face authentication  
✓ Comprehensive logging  
✓ Keyboard fallback testing  
✓ Automated demo mode  

---

## 📝 Next Steps

1. ✅ Run training: `python scripts/run_train_and_verify.py`
2. ✅ Test manually: `python scripts/manual_control.py`
3. ✅ Run gesture app: `python main.py --no-auth`
4. ✅ Collect more gesture samples to improve accuracy
5. ✅ Customize gesture mappings in `config.yaml`

---

**Ready to go! 🚀 Start with Step 1 above.**
