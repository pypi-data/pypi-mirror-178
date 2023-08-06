import time
from tqdm import tqdm

from deci_lab_client.models import AccuracyMetricKey, DeepLearningTask


def wait_until(predicate, timeout, period=15, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        return_value = predicate(*args, **kwargs)
        if return_value:
            return return_value
        time.sleep(period)
    return False


class TqdmUpTo(tqdm):
    DOWNLOAD_PARAMS = {
        "unit": "B",
        "unit_scale": True,
        "unit_divisor": 1024,
        "miniters": 1,
        "bar_format": "{l_bar}{bar:20}{r_bar}",
    }

    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize


_DL_TASK_TO_LABEL = {
    DeepLearningTask.CLASSIFICATION: AccuracyMetricKey.MAP,
    DeepLearningTask.SEMANTIC_SEGMENTATION: AccuracyMetricKey.MIOU,
}


def get_accuracy_metric_key(dl_task: str) -> str:
    return _DL_TASK_TO_LABEL.get(dl_task, AccuracyMetricKey.TOP_1)
