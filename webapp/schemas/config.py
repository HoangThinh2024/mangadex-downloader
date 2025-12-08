"""Config related schemas"""

from pydantic import BaseModel
from typing import Optional, List


class ConfigSchema(BaseModel):
    """Application configuration"""
    language: Optional[str] = "en"
    save_as: Optional[str] = None
    path: Optional[str] = None
    replace: bool = False
    no_track: bool = False
    use_alt_details: bool = False
    log_level: Optional[str] = "info"
    cover: Optional[str] = None
    use_chapters_alternative_names: bool = False
    no_oneshot_chapter: bool = False
    
    class Config:
        from_attributes = True
