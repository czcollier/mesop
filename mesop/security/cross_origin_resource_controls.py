from dataclasses import dataclass, field

@dataclass(kw_only=True)
class CrossOriginResourceControls:
  allowed_origis: list[str] = field(default_factory=list)