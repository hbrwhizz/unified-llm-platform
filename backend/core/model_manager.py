import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages LLM models - loading, unloading, and inference"""
    
    def __init__(self):
        self.models: Dict[str, dict] = {}
        self.current_model: Optional[str] = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    async def initialize(self):
        """Initialize the model manager"""
        logger.info(f"🖥️  Device: {self.device}")
        if self.device == "cuda":
            logger.info(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
            total_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            logger.info(f"💾 GPU Memory: {total_memory:.2f}GB")
        else:
            logger.info("⚠️  No GPU detected, using CPU (will be slower)")
    
    async def load_model(self, model_id: str, quantization: str = "4bit"):
        """Load a model from HuggingFace"""
        if model_id in self.models:
            logger.info(f"✅ Model {model_id} already loaded")
            return self.models[model_id]
        
        logger.info(f"📥 Loading model: {model_id}")
        
        try:
            # Quantization config
            bnb_config = None
            if quantization == "4bit" and self.device == "cuda":
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                )
            elif quantization == "8bit" and self.device == "cuda":
                bnb_config = BitsAndBytesConfig(load_in_8bit=True)
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # Load model
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=bnb_config,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            if self.device == "cpu":
                model = model.to(self.device)
            
            self.models[model_id] = {
                "model": model,
                "tokenizer": tokenizer,
                "quantization": quantization
            }
            
            self.current_model = model_id
            logger.info(f"✅ Model {model_id} loaded successfully")
            
            return self.models[model_id]
            
        except Exception as e:
            logger.error(f"❌ Error loading model {model_id}: {e}")
            raise
    
    async def generate(self, model_id: str, prompt: str, max_tokens: int = 512, 
                      temperature: float = 0.7, stream: bool = False):
        """Generate text with a model"""
        if model_id not in self.models:
            await self.load_model(model_id)
        
        model_data = self.models[model_id]
        model = model_data["model"]
        tokenizer = model_data["tokenizer"]
        
        # Tokenize
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        
        # Decode
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove prompt from output
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):]
        
        return generated_text.strip()
    
    async def unload_model(self, model_id: str):
        """Unload a model from memory"""
        if model_id in self.models:
            del self.models[model_id]
            if self.device == "cuda":
                torch.cuda.empty_cache()
            logger.info(f"🗑️  Model {model_id} unloaded")
    
    async def list_loaded_models(self):
        """Get list of currently loaded models"""
        return list(self.models.keys())
    
    async def cleanup(self):
        """Cleanup all models"""
        for model_id in list(self.models.keys()):
            await self.unload_model(model_id)