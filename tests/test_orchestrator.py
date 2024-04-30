from pytest import fixture
import pandas as pd

from src.orchestrator import Orchestrator

@fixture
def sample_df() -> pd.DataFrame:
    data = {
        'A': ["F1", 2, 3, 4, 5],
        'Unnamed 1': ["F2", 2.1, 3.1, 4.1, 5.1],
        'Unnamed 2': ["F3", 2.2, 3.3, 4.4, 5.5],
        'B': ["F1", 2, 3, 4, 5],
        'Unnamed 3': ["F2", 2.1, 3.1, 4.1, 5.1],
    }
    df = pd.DataFrame(data)
    return df

@fixture
def sample_orchestrator() -> Orchestrator:
    return Orchestrator()

def test_get_sub_dfs(sample_df, sample_orchestrator):
    groups_df = sample_orchestrator.get_sub_dfs(sample_df)
    assert len(groups_df) == 2
    assert groups_df[0].shape == (4, 3)
    assert groups_df[1].shape == (4, 2)
    