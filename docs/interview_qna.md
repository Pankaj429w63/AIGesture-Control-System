# Interview Questions & Answers

Q: How do you extract features from MediaPipe landmarks?
A: Capture normalized (x,y,z) of 21 landmarks and flatten to 63-d vector; optionally include angles/distances for scale invariance.

Q: How do you reduce false positives?
A: Confidence thresholding, gesture cooldown, temporal smoothing, ensemble models, augmentation and hard negatives.
