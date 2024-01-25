from typer import Typer
from torch_snippets import *
os.chdir('/home/ubuntu/code/Moore-AnimateAnyone')
sys.path.append('/home/ubuntu/code/Moore-AnimateAnyone')
from tools.vid2pose import main as worker
cli = Typer()

def phasify(items, n_phases: int):
    iterators = defaultdict(L)
    [iterators[ix % n_phases].append(item) for ix, item in enumerate(items)]
    return L(iterators.values())

@cli.command()
def main(phase:int, n_phases:int):
    phase = int(phase)
    n_phases = int(n_phases)
    def try_do(video):
        try:
            out = str(video.parent/f'dwpose_{video.name}')
            if os.path.exists(out): return
            worker(str(video.resolve()), out)
        except Exception as e:
            Warn(f'Failure @ {video}:: {e}')
            import traceback
            traceback.print_exc()
    videos = Glob("/home/ubuntu/data/anime/downloads/*/*.mp4")
    videos = [v for v in videos if 'dwpose' not in v.name]
    videos = [v for v in videos if 'Scene' in v.name]
    videos = phasify(videos, n_phases)[phase]
    for video in videos:
        try_do(video)
        
if __name__ == '__main__':
    cli()