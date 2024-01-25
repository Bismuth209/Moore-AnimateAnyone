from torch_snippets import *
from gogoanime import (
    get_search_results, get_anime_details, 
    get_anime_episode, get_anime_popular, 
    get_anime_newseason, get_anime_recent
)

import requests
from typer import Typer

def download_file(url, destination):
    response = requests.get(url)
    makedir(parent(destination))
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully to {destination}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")



def phasify(items, n_phases: int):
    iterators = defaultdict(L)
    [iterators[ix % n_phases].append(item) for ix, item in enumerate(items)]
    return L(iterators.values())

cli = Typer()
uid = ''
destination_path = f"/home/ubuntu/data/anime/downloads/"
animes = readlines('/home/ubuntu/data/anime/meta/slice-of-life.txt')

@cli.command()
def try_do(phase:int, n_phases:int):
    def do(item):
        if os.path.exists(destination_path) and len(Glob(f'{destination_path}/*.mp4')) == 2:
            tracker.send(f"Skipping {item}")
            return
        urls = get_anime_episode(email=uid, password=uid, id=item, episode=2)
        urls =  {item['quality']: item['link'] for item in urls}
        k = sorted(urls.keys(), key=lambda x: abs(int(x[:-1])-480) ) [0]
        url = urls[k]
        _destination = f'{destination_path}/{item}/ep-2-{k}.mp4'
        tracker.send(f"Processing {item}@{k}")
        download_file(url, _destination)
        
    _animes = sorted(list(animes))
    _animes = phasify(_animes, n_phases)[phase]
    for item in (tracker:=track2(_animes)):
        try:
            do(item)
        except KeyboardInterrupt:
            Info("Interrupted!")
            break
        except Exception as e:
            Warn(f"Failure @ {item} @ {e}\n\n")
            import traceback
            traceback.print_exc(e)

if __name__ == '__main__':
    cli()
