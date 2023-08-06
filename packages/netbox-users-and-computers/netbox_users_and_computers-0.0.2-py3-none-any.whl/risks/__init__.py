from extras.plugins import PluginConfig


class NetBoxRisksConfig(PluginConfig):
    name = 'users_and_computers'
    verbose_name = 'Users and Computers'
    description = 'Manage AD Users and Workstations'
    version = '0.0.2'
    base_url = 'risks'
    author = 'Artur Shamsiev'
    author_email = 'me@z-lab.me'


config = NetBoxRisksConfig
