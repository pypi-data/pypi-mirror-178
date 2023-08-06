import time

from deci_lab_client.models import AccuracyMetricKey, DeepLearningTask


def wait_until(predicate, timeout, period=15, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        return_value = predicate(*args, **kwargs)
        if return_value:
            return return_value
        time.sleep(period)
    return False


_DL_TASK_TO_LABEL = {
    DeepLearningTask.CLASSIFICATION: AccuracyMetricKey.MAP,
    DeepLearningTask.SEMANTIC_SEGMENTATION: AccuracyMetricKey.MIOU,
}


def get_accuracy_metric_key(dl_task: str) -> str:
    return _DL_TASK_TO_LABEL.get(dl_task, AccuracyMetricKey.TOP_1)
