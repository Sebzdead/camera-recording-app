# Camera Recording App Guidelines

## Commands
- Install dependencies: `pip install -r requirements.txt`
- Run application: `python src/main.py`

## Code Structure
- Camera control logic: `src/camera_controller.py`
- Video recording: `src/video_recorder.py`
- Main UI: `src/ui/main_window.py`
- Settings panel: `src/ui/settings_panel.py`
- Default settings: `config/default_settings.json`

## Style Guidelines
- **Imports**: System libraries → third-party → project modules
- **Naming**: Classes (PascalCase), methods/variables (snake_case)
- **Structure**: Class-based, modular design with separation of concerns
- **Error handling**: Check camera status before operations
- **Dependencies**: EasyPySpin, OpenCV, NumPy, PyQt5
- **Organization**: Maintain separation between controller, model, and view components

## Development Next Steps
- Add type hints to function signatures
- Implement unit tests
- Add docstrings to classes and methods