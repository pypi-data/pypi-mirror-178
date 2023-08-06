# pycooldown
[![pypi](https://github.com/TrigonDev/apgorm/actions/workflows/pypi.yml/badge.svg)](https://pypi.org/project/pycooldown)

[Documentation](https://github.com/circuitsacul/pycooldown/wiki) | [Support](https://discord.gg/dGAzZDaTS9)

A lightning-fast cooldown/ratelimit implementation.

## Example Usage
```py
from pycooldown import FixedCooldown


cooldown = FixedCooldown(period=10, capacity=5)


def handle_event(sender):
    retry_after = cooldown.update_ratelimit(sender)
    if retry_after is None:
        print("Event succeeded!")
    else:
        print(f"Too many events from {sender}. Retry in {retry_after} seconds.")
```
