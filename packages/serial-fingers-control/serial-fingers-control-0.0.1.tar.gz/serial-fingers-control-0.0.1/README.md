# Serial-fingers-control [![old api](https://img.shields.io/badge/old-api-blue?style=for-the-badge&logoColor=white)](https://github.com/Adam-Software) [![Platforms](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white) [![Language](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) [![adam package](https://img.shields.io/badge/adam_package-red?style=for-the-badge&logo=python&logoColor=white)](https://github.com/Adam-Software)

[![License](https://img.shields.io/github/license/Adam-Software/Serial-fingers-control)](https://img.shields.io/github/license/Adam-Software/Serial-fingers-control)
[![Activity](https://img.shields.io/github/commit-activity/m/Adam-Software/Serial-fingers-control)](https://img.shields.io/github/commit-activity/m/Adam-Software/Serial-fingers-control)
[![LastStatus](https://img.shields.io/github/last-commit/Adam-Software/Serial-fingers-control)](https://img.shields.io/github/last-commit/Adam-Software/Serial-fingers-control)
[![CodeSize](https://img.shields.io/github/languages/code-size/Adam-Software/Serial-fingers-control)](https://img.shields.io/github/languages/code-size/Adam-Software/Serial-fingers-control)
[![Depencies](https://img.shields.io/librariesio/github/Adam-Software/Serial-fingers-control)](https://img.shields.io/librariesio/github/Adam-Software/Serial-fingers-control)

### What the library can do?

1. Finger control via the STM32 controller using an outdated API
2. Calculation of angles through interpolation

### How install?

```commandline
pip install serial-fingers-control
```

### How import?

For fingers control:
```python
from serial_fingers_control.FingersControl import *
```

For calculate interpolation:
```python
from serial_fingers_control.CalculateGoalPosition import *
```
