from tqdm import tqdm
import time
import urllib
from time import sleep
import threading

def my_hook(t):
    """Wraps tqdm instance.
    Don't forget to close() or __exit__()
    the tqdm instance once you're done with it (easiest using `with` syntax).
    Example
    -------
    >>> with tqdm(...) as t:
    ...     reporthook = my_hook(t)
    ...     urllib.urlretrieve(..., reporthook=reporthook)
    """
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] or -1,
            remains unchanged.
        """
        if tsize not in (None, -1):
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b
        sleep(0.2)

    return update_to

#la posicion es el numero de hebra para el multihebrado
def descargarFicheroconBarra(url, nombrefichero, posicion_barra):
    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=nombrefichero.split('/')[-1], position=posicion_barra) as t: 
            urllib.urlretrieve(url, filename=nombrefichero, reporthook=my_hook(t), data=None)