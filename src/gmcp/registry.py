from pathlib import Path
import importlib.util, sys
from types import ModuleType
TOOLS_DIR = Path(__file__).resolve().parent.parent.parent / "tools"
TOOLS_DIR.mkdir(parents=True, exist_ok=True)
class ToolRegistry:
    def __init__(self) -> None:
        self.dir = TOOLS_DIR
    def has(self, tool_name: str) -> bool:
        file_name = tool_name.replace(".", "_") + ".py"
        return (self.dir / file_name).exists()
    def path_for(self, tool_name: str) -> Path:
        return self.dir / (tool_name.replace(".", "_") + ".py")
    def load_tool_module(self, path: Path) -> ModuleType:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if not spec or not spec.loader:
            raise RuntimeError(f"Cannot load generated tool at {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        return module