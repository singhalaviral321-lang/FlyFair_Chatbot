"""
LLM Service for FlyFair
Abstracted LLM layer supporting Ollama and LM Studio.
"""
import os
import httpx
from typing import Optional
from pydantic import BaseModel


class LLMConfig(BaseModel):
    """LLM configuration"""
    provider: str = "ollama"  # "ollama" or "lm_studio"
    base_url: str = "http://localhost:11434"  # Ollama default
    model_name: str = "llama2"  # or "mistral", "llama3", etc.
    timeout: float = 30.0


class LLMService:
    """Abstracted LLM service supporting multiple providers"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize LLM service.
        
        Args:
            config: LLM configuration. If None, reads from environment.
        """
        if config is None:
            config = LLMConfig(
                provider=os.getenv("LLM_PROVIDER", "ollama"),
                base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434"),
                model_name=os.getenv("LLM_MODEL", "llama2"),
                timeout=float(os.getenv("LLM_TIMEOUT", "30.0"))
            )
        self.config = config
        self.client = httpx.Client(timeout=config.timeout)
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate response from LLM.
        
        Args:
            system_prompt: System prompt
            user_prompt: User prompt
        
        Returns:
            Generated text
        """
        if self.config.provider == "ollama":
            return self._generate_ollama(system_prompt, user_prompt)
        elif self.config.provider == "lm_studio":
            return self._generate_lm_studio(system_prompt, user_prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    def _generate_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Generate using Ollama"""
        try:
            # Try chat API first (newer models)
            try:
                response = self.client.post(
                    f"{self.config.base_url}/api/chat",
                    json={
                        "model": self.config.model_name,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "stream": False
                    }
                )
                response.raise_for_status()
                return response.json().get("message", {}).get("content", "")
            except:
                # Fallback to generate API (older models)
                response = self.client.post(
                    f"{self.config.base_url}/api/generate",
                    json={
                        "model": self.config.model_name,
                        "prompt": f"{system_prompt}\n\nUser: {user_prompt}\n\nAssistant:",
                        "stream": False,
                        "system": system_prompt
                    }
                )
                response.raise_for_status()
                return response.json().get("response", "")
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Ollama: {e}")
    
    def _generate_lm_studio(self, system_prompt: str, user_prompt: str) -> str:
        """Generate using LM Studio"""
        try:
            response = self.client.post(
                f"{self.config.base_url}/v1/chat/completions",
                json={
                    "model": self.config.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 500
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to LM Studio: {e}")
    
    def close(self):
        """Close HTTP client"""
        self.client.close()
