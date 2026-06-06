from __future__ import annotations

import argparse
from pathlib import Path

import librosa
import numpy as np
import torch
import torch.nn as nn


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = REPO_ROOT / "models" / "merged_human_nonhuman_rubble_best.pt"
DEFAULT_WAV_PATH = REPO_ROOT / "demo_samples" / "demo_samples" / "nigens_quick_test" / "human" / "human_01_femaleSpeech.wav"


class SmallAudioCNN(nn.Module):
    def __init__(self, num_classes: int = 2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(p=0.25),
            nn.Linear(64, 32),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.15),
            nn.Linear(32, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def load_audio(path: Path, target_sr: int) -> np.ndarray:
    waveform, sr = librosa.load(path, sr=None, mono=True)
    waveform = waveform.astype(np.float32)
    if sr != target_sr:
        waveform = librosa.resample(waveform, orig_sr=sr, target_sr=target_sr)
    return waveform.astype(np.float32)


def crop_or_pad(waveform: np.ndarray, target_length: int) -> np.ndarray:
    current_length = len(waveform)
    if current_length > target_length:
        start = (current_length - target_length) // 2
        waveform = waveform[start : start + target_length]
    elif current_length < target_length:
        pad_total = target_length - current_length
        pad_left = pad_total // 2
        pad_right = pad_total - pad_left
        waveform = np.pad(waveform, (pad_left, pad_right), mode="constant")
    return waveform.astype(np.float32)


def waveform_to_logmel(
    waveform: np.ndarray,
    sr: int,
    n_mels: int,
    n_fft: int,
    hop_length: int,
) -> np.ndarray:
    mel = librosa.feature.melspectrogram(
        y=waveform,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0,
    )
    log_mel = librosa.power_to_db(mel, ref=np.max)
    return ((log_mel - log_mel.mean()) / (log_mel.std() + 1e-6)).astype(np.float32)


def load_checkpoint(model_path: Path, device: torch.device):
    try:
        checkpoint = torch.load(model_path, map_location=device, weights_only=False)
    except TypeError:
        checkpoint = torch.load(model_path, map_location=device)

    label_to_idx = checkpoint.get("label_to_idx", {"NON_HUMAN": 0, "HUMAN": 1})
    model = SmallAudioCNN(num_classes=len(label_to_idx)).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, checkpoint, label_to_idx


def predict_wav(wav_path: Path, model_path: Path, threshold_override: float | None = None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, checkpoint, label_to_idx = load_checkpoint(model_path, device)

    config = checkpoint.get("config", {})
    sample_rate = int(config.get("sample_rate", 16000))
    clip_seconds = float(config.get("clip_seconds", 1.5))
    n_mels = int(config.get("n_mels", 64))
    n_fft = int(config.get("n_fft", 1024))
    hop_length = int(config.get("hop_length", 256))
    threshold = float(threshold_override if threshold_override is not None else checkpoint.get("decision_threshold", 0.50))

    waveform = load_audio(wav_path, target_sr=sample_rate)
    waveform = crop_or_pad(waveform, target_length=int(sample_rate * clip_seconds))
    logmel = waveform_to_logmel(waveform, sr=sample_rate, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    feature = torch.tensor(logmel, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(feature)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    human_probability = float(probs[label_to_idx["HUMAN"]])
    non_human_probability = float(probs[label_to_idx["NON_HUMAN"]])
    predicted_label = "HUMAN" if human_probability >= threshold else "NON_HUMAN"

    return {
        "wav_path": str(wav_path),
        "model_path": str(model_path),
        "predicted_label": predicted_label,
        "human_probability": human_probability,
        "non_human_probability": non_human_probability,
        "decision_threshold": threshold,
        "device": str(device),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Echo Swarm 2 demo WAV inference")
    parser.add_argument("--wav", type=Path, default=DEFAULT_WAV_PATH, help="Test edilecek WAV dosyasi")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH, help=".pt model dosyasi")
    parser.add_argument("--threshold", type=float, default=None, help="Istege bagli karar esigi")
    args = parser.parse_args()

    if not args.model.exists():
        raise FileNotFoundError(f"Model bulunamadi: {args.model}")
    if not args.wav.exists():
        raise FileNotFoundError(f"WAV bulunamadi: {args.wav}")

    result = predict_wav(args.wav, args.model, threshold_override=args.threshold)
    print("Echo Swarm 2 inference sonucu")
    print(f"WAV: {result['wav_path']}")
    print(f"Model: {result['model_path']}")
    print(f"Device: {result['device']}")
    print(f"Prediction: {result['predicted_label']}")
    print(f"Human probability: {result['human_probability']:.6f}")
    print(f"Non-human probability: {result['non_human_probability']:.6f}")
    print(f"Decision threshold: {result['decision_threshold']:.3f}")


if __name__ == "__main__":
    main()
