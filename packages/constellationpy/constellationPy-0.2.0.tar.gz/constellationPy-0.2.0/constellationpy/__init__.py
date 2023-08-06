import pkg_resources

from .client import ouvrir_client, Client
from .serveur import Serveur, lancer_serveur, mettre_constellation_à_jour, désinstaller_constellation
from .sync import ClientSync
from .utils import fais_rien, une_fois

try:
    __version__ = pkg_resources.get_distribution('constellationPy').version
except pkg_resources.DistributionNotFound:
    __version__ = None
