from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dateutil import parser


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Calcula el porcentaje de valores faltantes en cada columna de un DataFrame.

    Args:
    df (DataFrame): El DataFrame a analizar.

    Returns:
    pd.Series: Una Serie de pandas con el porcentaje de valores faltantes por columna.
    """
    return df.isnull().mean().round(4) * 100


def check_duplicates(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Cuenta las filas duplicadas para cada valor de una columna específica y devuelve una tabla ordenada.

    Args:
    df (DataFrame): El DataFrame a analizar.
    column (str): La columna en la que contar duplicados.

    Returns:
    DataFrame: Un DataFrame con el recuento de duplicados por valor, ordenado de mayor a menor.
    """
    duplicates = df[df.duplicated(column, keep=False)]
    return duplicates.groupby(column).size().sort_values(ascending=False).reset_index(name='duplicated')


def validate_key_to_value_consistency(df: pd.DataFrame, key_value_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
    """
    Valida que cada clave primaria en el DataFrame se asocie con un único valor en otra columna y retorna los valores inconsistentes.

    Args:
    df (DataFrame): El DataFrame a analizar.
    key_value_pairs (list of tuple): Lista de tuplas, donde cada tupla contiene una clave primaria y una columna a comparar.

    Returns:
    DataFrame: Un DataFrame con las filas que no cumplen la condición de consistencia.
    """
    inconsistent_values = pd.DataFrame()
    for key, value in key_value_pairs:
        grouped = df.groupby(key)[value].nunique()
        inconsistent_keys = grouped[grouped > 1].index.tolist()

        if inconsistent_keys:
            inconsistent_rows = df[df[key].isin(inconsistent_keys)]
            print(f"Inconsistencias encontradas en '{key}' respecto a '{value}':")
            # print(inconsistent_rows[[key, value]].drop_duplicates()) # No los imprimiré, solo los retorno

            inconsistent_values = pd.concat([inconsistent_values, inconsistent_rows])
        else:
            print(f"No se encontraron inconsistencias en '{key}' respecto a '{value}':")

    return inconsistent_values.drop_duplicates()


def infer_type(value) -> str:
    """
    Infiere el tipo de dato de un valor dado.

    Esta función intenta determinar el tipo de dato de un valor. Los tipos posibles incluyen
    'NaN' para valores no numéricos, 'boolean' para valores booleanos, 'numeric_positive'
    o 'numeric_negative' para números, 'date' para fechas, y 'str' para cualquier otro
    tipo de cadena de texto.

    Args:
    value: El valor a evaluar. Puede ser de cualquier tipo.

    Returns:
    str: Una cadena que describe el tipo de dato inferido del valor.
    """
    try:
        if pd.isna(value):
            return 'NaN'
        elif value in ['True', 'False']:
            return 'boolean'

        float_value = float(value)
        int_value = int(float_value)
        # return 'int' if float_value == int_value else 'float' # Si quisieramos dividir float e int
        return 'numeric_positive' if float_value >= 0 else 'numeric_negative'
    except ValueError:
        try:
            parsed_date = parser.parse(value)
            return 'date'
        except (ValueError, TypeError):
            return 'str'


def infer_and_validate_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida los tipos de datos de cada columna en un DataFrame y devuelve una matriz con el conteo de tipos de datos.

    Args:
    df (DataFrame): El DataFrame a analizar.

    Returns:
    DataFrame: Una matriz con el conteo de tipos de datos por columna.
    """

    type_matrix = {}

    for column in df.columns:
        types_count = df[column].apply(infer_type).value_counts()
        type_matrix[column] = types_count

    return pd.DataFrame(type_matrix).fillna(0).T


def graph_data_types(df: pd.DataFrame) -> None:
    """
    Genera un gráfico de barras apiladas de los conteos de tipos de datos por variable.

    Args:
    df (pandas.DataFrame): DataFrame que contiene el resumen de conteos por tipo de dato.
    """
    colormap = plt.cm.viridis

    ax = df.plot(kind='barh', stacked=True, figsize=(10, 8), colormap=colormap)

    ax.set_xlabel('Conteo')
    ax.set_ylabel('Variables')
    ax.set_title('Conteo de Tipos de Datos por Variable')

    plt.legend(title='Tipos de datos')
    plt.tight_layout()
    plt.show()


def check_ranges(df: pd.DataFrame, constraints: List[Tuple[str, Union[int, float], Union[int, float]]]) -> pd.DataFrame:
    """
    Verifica si los valores de las columnas especificadas en un DataFrame de pandas
    se encuentran dentro de los rangos dados.

    Args:
    df (pd.DataFrame): DataFrame de pandas.
    constraints (list of tuples): Lista de tuplas, donde cada tupla contiene el nombre de la columna
                                  (variable_name), el valor mínimo (minimum) y el valor máximo (maximum).

    Returns:
    pd.DataFrame: DataFrame que indica con True si los valores están en el rango y False si no lo están.
    """
    results = pd.DataFrame(index=df.index)
    for variable_name, minimum, maximum in constraints:
        if variable_name in df.columns:
            column = pd.to_numeric(df[variable_name], errors='coerce')
            results[variable_name] = column.between(minimum, maximum, inclusive='both') & ~column.isna()
        else:
            results[variable_name] = False  # Si la columna no existe, llena con False
    return results


def plot_outliers_and_return_df(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Grafica un boxplot para una columna específica y retorna un DataFrame con los datos atípicos.

    Args:
    df (pd.DataFrame): DataFrame de entrada.
    column_name (str): Nombre de la columna para analizar los datos atípicos.

    Returns:
    pd.DataFrame: DataFrame conteniendo solo los datos atípicos de la columna especificada.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column_name])
    plt.title(f'{column_name} Boxplot')
    plt.show()

    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_df = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)]
    return outliers_df
