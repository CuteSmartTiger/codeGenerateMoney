import pandas as pd


def has_at_most_one_positive(df, column, start, end):
    # 获取第 start 到 end 的数据（不包含 end）
    subset = pd.to_numeric(df[column].iloc[start:end], errors='coerce').dropna()

    # 统计正数数量
    positive_count = (subset > 0).sum()

    return positive_count <= 1


def first_two_positive(df, column):
    values = pd.to_numeric(df[column].iloc[0:2], errors='coerce')
    return (values > 0).all()


def meet_strategy_one(k_data_df):
    if not first_two_positive(k_data_df, 'profit'):
        return False

    if not has_at_most_one_positive(k_data_df, 'profit',2,7):
        return False

    return True


if __name__ == '__main__':
    mock_df = pd.DataFrame({'profit': [1, 2, -2, -3, 1, -4, -5]})
    assert meet_strategy_one(mock_df)==True
    mock_df = pd.DataFrame({'profit': [1, 2, -2, -3, -1, -4, -5]})
    assert meet_strategy_one(mock_df)==True

    mock_df = pd.DataFrame({'profit': [-1, 2, -2, -3, -1, -4, -5]})
    assert meet_strategy_one(mock_df) == False