import numpy as np

# Keep these identifiers stable when adding or reordering modules.
stream_ids = {
    "initialization": 0,
    "source_sink": 10,
    "collision": 20,
    "fragmentation": 30,
    "atmosphere": 40,
}


# Class that defines a random number generator function stream for each component
# random generator object can be accessed from the get() method, with the component token taken as a string argument
class RandomStreams:
    def __init__(self, seed: int):
        self._streams = {
            name: np.random.Generator(
                np.random.PCG64(np.random.SeedSequence([stream_id, seed]))
            )
            for name, stream_id in stream_ids.items()
        }

    def get(self, component: str) -> np.random.Generator:
        return self._streams[component]
