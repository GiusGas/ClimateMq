import torch
import pickle
import importlib.util
from huggingface_hub import hf_hub_download

_MODEL = None
_SCALER = None

REPO_ID = "assix-research/gcc-weather-forecast-transformer"

def get_weather_model():
    """
    Returns the loaded model and scaler. 
    Loads them from disk ONLY if they are not already in memory.
    """
    global _MODEL, _SCALER

    if _MODEL is not None and _SCALER is not None:
        return _MODEL, _SCALER

    print("Loading Weather Model into memory (First run only)...")

    try:
        model_path = hf_hub_download(repo_id=REPO_ID, filename="weather_transformer.pt")
        scaler_path = hf_hub_download(repo_id=REPO_ID, filename="feature_scaler.pkl")
        code_path = hf_hub_download(repo_id=REPO_ID, filename="model.py")

        with open(scaler_path, "rb") as f:
            _SCALER = pickle.load(f)

        spec = importlib.util.spec_from_file_location("weather_model", code_path)
        weather_model_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(weather_model_module)

        _MODEL = weather_model_module.WeatherTransformer(input_dim=4, seq_len=72)
        if torch.cuda.is_available():
            _MODEL.load_state_dict(torch.load(model_path))
        else:
            _MODEL.load_state_dict(
                torch.load(model_path, map_location=torch.device('cpu'))
            )
        _MODEL.eval()
        
        print("Model loaded successfully!")

    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

    return _MODEL, _SCALER