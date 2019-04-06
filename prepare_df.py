import pandas as pd


def prepare_df(population_csv: str = 'population.csv',
               refugees_csv: str = 'refugees.csv',
               years=range(1990, 2018)) -> pd.DataFrame:
    df_p = pd.read_csv(population_csv, skiprows=3)
    df_r = pd.read_csv(refugees_csv, skiprows=3)
    years = [str(year) for year in years]
    df_prop = df_r.loc[:, ['Country Name', 'Country Code'] + years]
    df_prop[years] /= df_p[years]
    return df_prop


if __name__ == '__main__':
    df = prepare_df()

    # to save:
    df.to_csv('density.csv')

    print(df[df["Country Code"] == "PAK"])

    print(df.sort_values(by='2017', na_position='last').head(20))

    # print(df['2017'].sort())
