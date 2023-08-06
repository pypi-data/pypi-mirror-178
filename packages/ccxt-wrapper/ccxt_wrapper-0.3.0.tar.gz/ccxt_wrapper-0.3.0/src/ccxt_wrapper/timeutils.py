import asyncio
import warnings
from datetime import datetime, timedelta
from math import ceil

from tqdm import tqdm


def round_time(t: datetime, interval: timedelta) -> datetime:
    return t - (t - datetime.min) % interval


async def wait_until(t: datetime, enable_tqdm: bool = False) -> None:
    """Wait until the given time.

    Parameters
    ----------
    t : datetime
        The time to wait until
    enable_tqdm : bool, optional
        Whether to enable the tqdm progress bar, by default False
    """

    if datetime.now() > t:
        warnings.warn(
            RuntimeWarning(
                f"Time is in the past, now:{datetime.now()}, t:{t}, delta:{datetime.now() - t}"
            )
        )

    pbar = tqdm(
        total=ceil((t - datetime.now()).total_seconds()),
        disable=not enable_tqdm,
        bar_format="|{bar}| {percentage:.2f}% [{elapsed}<{remaining}]",
    )
    last_update = datetime.now()
    while datetime.now() < t:
        await asyncio.sleep(min((t - datetime.now()).total_seconds(), 0.1))
        pbar.update((datetime.now() - last_update).total_seconds())
        last_update = datetime.now()
    pbar.n = pbar.total


if __name__ == "__main__":
    asyncio.run(
        wait_until(
            round_time(datetime.now(), timedelta(seconds=1)) + timedelta(seconds=10),
            enable_tqdm=True,
        )
    )
