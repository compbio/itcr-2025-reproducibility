# C. Savonen 2021

# https://alexslemonade.github.io/refinebio-py/quickstart.html

import os
from pathlib import Path
import pyrefinebio

data_dir = Path('data/SRP070849')

data_file = Path(os.path.join(data_dir, 'SRP070849.tsv'))

metadata_file = Path(os.path.join(data_dir, 'metadata_SRP070849.tsv'))

try:
  os.mkdir(data_dir, mode = 0o777)
except OSError as error:
  print(error)

if not data_file.exists() or not metadata_file.exists():

    print("Downloading SRP070849 from refine.bio")

    pyrefinebio.create_token(agree_to_terms=True, save_token=False)

    pyrefinebio.download_dataset(
      "data/dataset.zip",
      "cansav09@gmail.com",
      experiments=["SRP070849"],
      extract=True
    )
