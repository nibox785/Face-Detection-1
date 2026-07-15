import numpy as np
import torch
from .config import FACE_CLASSES

# Precompute 1D lookup table for fast mapping
FACE_LUT = np.zeros(256, dtype=np.uint8)
FACE_LUT[FACE_CLASSES] = 255

def logits_to_binary_mask(logits):
    """
    Convert model output logits to a binary mask where face components are 255 and background/others are 0.
    
    Args:
        logits (torch.Tensor or np.ndarray): Raw logits from U-Net model of shape (19, H, W) or (1, 19, H, W)
        
    Returns:
        np.ndarray: Binary mask of shape (H, W) with values 0 or 255 (np.uint8)
    """
    if isinstance(logits, np.ndarray):
        if len(logits.shape) == 4:  # (1, 19, H, W)
            logits = logits[0]
        preds = np.argmax(logits, axis=0)  # (H, W)
        binary_mask = FACE_LUT[preds]
    else:
        # Assuming PyTorch Tensor
        if len(logits.shape) == 4:  # (1, 19, H, W)
            logits = logits.squeeze(0)
        
        with torch.no_grad():
            preds = torch.argmax(logits, dim=0).cpu().numpy()  # (H, W)
            
        binary_mask = FACE_LUT[preds]
            
    return binary_mask
