import joblib
import logging
from functools import lru_cache
from .config import MODEL_PATHS

logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Singleton-like Model Loader to ensure machine learning models
    are loaded into memory only once during the application's lifecycle.
    """

    @staticmethod
    @lru_cache(maxsize=10)
    def get_model(disease_name: str):
        """
        Loads and caches a scikit-learn pipeline/model by disease name.
        Uses lru_cache to prevent repeated I/O operations and memory leaks.
        """
        if disease_name not in MODEL_PATHS:
            raise ValueError(f"Unknown disease model requested: {disease_name}")

        model_path = MODEL_PATHS[disease_name]
        
        try:
            logger.info(f"Loading {disease_name} model into memory from {model_path}...")
            model = joblib.load(model_path)
            return model
        except FileNotFoundError:
            logger.error(f"Model file not found: {model_path}")
            raise RuntimeError(f"Could not find trained model for {disease_name} at {model_path}. Ensure training notebooks were executed.")
        except Exception as e:
            logger.error(f"Error loading {disease_name} model: {str(e)}")
            raise RuntimeError(f"Failed to load {disease_name} model. Error: {str(e)}")
