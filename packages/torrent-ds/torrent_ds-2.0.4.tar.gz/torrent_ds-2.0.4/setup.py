# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torrent_ds', 'torrent_ds_tools']

package_data = \
{'': ['*']}

install_requires = \
['cryptography==3.3.2',
 'ncoreparser',
 'pyopenssl==19.1.0',
 'sqlalchemy==1.3.16',
 'transmissionrpc-ng==0.12.0']

entry_points = \
{'console_scripts': ['torrent-ds = torrent_ds.torrent_ds:main',
                     'torrent-ds-data = torrent_ds_tools.read_data:main']}

setup_kwargs = {
    'name': 'torrent-ds',
    'version': '2.0.4',
    'description': 'Manage downloads using ncoreparser package.',
    'long_description': '# Torrent-ds service\n\n## Leírás\nTorrentszerver applikáció Ncore-hoz. Képes kezelni az rss feed-eket illetve az Ncore ajánlott funkcióját.\nÖszekapcsolható a Transmisison-al, ami le tudja tölteni a torrent tartalmát.\n\nFunkciók:\n* Periódikusan megnyitja a torrenteket az rss feed linkeket használva, és a meghatározott kategóriákat képes külön könyvtárakba letölteni. (Bármennyi rss link megadható)\n* A konfigurációban meghatározott intervallum alatt leállítja az összes torrentet (pl.: napközben munka mellett) (opcionális)\n* Meghatározott időnként letölti a staff által ajánlottnak jelölt torrenteket, kategóriánként beállított könyvtárakba (opcionális)\n\n\n## Telepítés\n\n```\npip install torrent-ds --upgrade --user\n```\n```\necho "[Unit]\nDescription=Torrent-ds service\nAfter=multi-user.target\nConflicts=getty@tty1.service\n[Service]\nUser=${USER}\nType=simple\nEnvironment="LC_ALL=C.UTF-8"\nEnvironment="LANG=C.UTF-8"\nExecStart=${HOME}/.local/bin/torrent-ds\n[Install]\nWantedBy=multi-user.target" | sudo tee /etc/systemd/system/torrent-ds.service\n```\n```\nsudo systemctl daemon-reload\nsudo systemctl enable torrent-ds.service\nsudo systemctl start torrent-ds.service\n```\n\n## Konfiguráció\n\nKét fájl tartalmazza az összes konfigurációt a programhoz:\n* $HOME/.config/torrent_ds/config.ini\n* $HOME/.config/torrent_ds/credentials.ini\n\n### config.ini\nMinden szekció ([]-ben) kötelező mező (kivéve az rss), a többi lehet opcionális vagy kötelező.\n```\n[transmission]\nauthenticate = False  | Kötelező\n                      | A lehetséges értékek: True és False.\n                      | Értelemszerűen ha azonosításra van szükség: True.\n                      | A hozzá tartozó azonosító adatokat a credentials.ini fájl\n                      | [transmission] szekcióban kell definiálni\nip_address =          | Opcionális\n                      | A transmission remote ip_címe\nport =                | Opcionális\n                      | A transmission remote port-ja. Az alapértelmezett: 9091\nsleep_days =          | Opcionális\n                      | A megadott napokon fog érvénybe lépni a sleep_time értéke\n                      | 1:hétfő -> 7:vasárnap, ;-vel elválasztva. Pl.: 1;2;3;4;5\n                      | vagyis hétfő,kedd,szerda,csütörtök,péntek. Ezeken a napokon\n                      | fog végrehajtódni.\nsleep_time =          | Opcionális\n                      | A megadott intervallumban az aktuálisan futó torrenteket\n                      | szünetelteti. A formátum: 00:00:00-00:00:00\n\n[download]\nretry_interval = 10   | Kötelező\n                      | Az rss feed-ek ellenőrzési intervalluma másodperben\n\n[recommended]         | A staff által ajánlottnak jelölt torrentek letöltése\n                      | meghatározottan periódusonként.\nenable = False        | Kötelező\n                      | Lehetséges értékek True és False.\ncredential = cred1    | Kötelező\n                      | Azonosító szekció a credentials.ini fájlban\ncategories =          | Opcionális\n                      | ;-vel elválasztva a kategóriákat. A kategóriák az alábbiak lehetnek:\n                      | movies;series;musics;games;books;programs;xxx\nmax_size = 3 GiB      | Opcionális\n                      | Maximum limit. Az ennél nagyobb méretű torrenteket nem tölti le\n                      | ajánlott módban. Lehetséges dimenziók: KiB, MiB, GiB, TiB.\n                      | A helyes formátum: \'<érték> <dimenzió>\'\nretry_interval = 5    | Kötelező\n                      | Az ajánlott torrentek letöltésének gyakorisága (órában)\nmovies =              | A filmeket az itt megadott mappába tölti le pl: /home/osmc/Downloads/movies\nseries =              | A sorozatokat az itt megadott mappába tölti le pl: /home/osmc/Downloads/series\nmusics =              | A zenéket az itt megadott mappába tölti le pl: /home/osmc/Downloads/musics\ngames =               | A játékokat az itt megadott mappába tölti le pl: /home/osmc/Downloads/games\nbooks =               | A könyveket az itt megadott mappába tölti le pl: /home/osmc/Downloads/books\nprograms =            | A filmeket az itt megadott mappába tölti le pl: /home/osmc/Downloads/programs\nxxx =\n\n[rss bookmark1]       | Az rss-el kezdődő szekció: [rss <szekciónév>] pl: [rss Bela_rss]\ncredential = cred1    | Kötelező\n                      | Azonosító szekció a credentials.ini fájlban\nurl =                 | Kötelező, Rss url -> ncore könyvjelzők\nlimit =               | Letölthető torrentek száma havonta\nmovies =              | A filmeket az itt megadott mappába tölti le pl: /home/osmc/Downloads/movies\nseries =              | A sorozatokat az itt megadott mappába tölti le pl: /home/osmc/Downloads/series\nmusics =              | A zenéket az itt megadott mappába tölti le pl: /home/osmc/Downloads/musics\ngames =               | A játékokat az itt megadott mappába tölti le pl: /home/osmc/Downloads/games\nbooks =               | A könyveket az itt megadott mappába tölti le pl: /home/osmc/Downloads/books\nprograms =            | A filmeket az itt megadott mappába tölti le pl: /home/osmc/Downloads/programs\nxxx =\n\n[rss bookmark2]       | Bármennyi rss szekció használható\ncredential = cred2\nurl =\nmovies =\nseries =\nmusics =\nclips =\ngames =\nbooks =\nprograms =\nxxx =\n```\n\n### credentials.ini\nMinden szekció opcionális és bárhogy elnevezhető. Fontos: A config.ini \'credential\' neveit itt kell definiálni.\nA username értéke legyen a felhasználónév és a raw_password a jelszó. A jelszó automatikusan títkosítva lesz\nés visszakerül a password értékeként, a raw_password törlődik.\n```\n[transmission]      | Azonsító a Transmission-hoz. Ha az authenticate értéke True a config.ini-ben\nuser_name =         | Transmission felhasználónév\nraw_password =      | Transmission jelszó\npassword =          | Titkosított jelszó. Automatikusan íródik ki\n\n[cred1]             | Azonosító mező az Ncore-hoz. Bármilyen nevet kaphat pl.: [Bela]\nuser_name =         | Felhasználónév\nraw_password =      | Jelszó\npassword =          | Titkosított jelszó.\n\n[cred2]\nuser_name =\nraw_password =\npassword =\n```\n## Használat\n### torrent-ds service indítása\n```\nsudo systemctl start torrent-ds\n```\n### torrent-ds service megállítása\n```\nsudo systemctl stop torrent-ds\n```\n### logok megtekintése\n```\njournalctl -fu torrent-ds\n```\n### Bármilyen konfiguráció módosítása után újraindítás szükséges\n```\nsudo systemctl restart torrent-ds\n```\n',
    'author': 'Aron Radics',
    'author_email': 'aron.radics.jozsef@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/radaron/torrent-ds',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
