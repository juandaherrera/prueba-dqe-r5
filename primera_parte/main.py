import json
import os

import pandas as pd

""" El SETTINGS tiene todas las configuraciones necesarias para la extracción y transformación del json a csv.
    la variable 'json_path' es un string con la ruta absoluta en donde se encuentra el json a leer.
    la variable 'csv_path' es un string con la ruta absoluta en donde será puesto el csv con la información procesada.
    la variable 'artist_keys' son las columnas que queremos extraer de la información del artista.
    la variable 'album_keys' son las columnas que queremos extraer de la información de cada álbum.
    la variable 'track_keys' son las columnas que queremos extraer de la información del cada track.
    la variable 'nested_keys' son las columnas que pertenecen al track y contienen información anidada (son diccionarios)."""
SETTINGS = {
    'json_path': os.path.join(os.path.dirname(__file__), 'data', 'raw', 'taylor_swift_spotify.json'),
    'csv_path': os.path.join(os.path.dirname(__file__), 'data', 'processed', 'output.csv'),
    'artist_keys': ['artist_id', 'artist_name', 'artist_popularity'],
    'album_keys': ['album_id', 'album_name', 'album_release_date', 'album_total_tracks'],
    'track_keys': [
        'disc_number',
        'duration_ms',
        'explicit',
        'track_number',
        'track_popularity',
        'track_id',
        'track_name',
    ],
    'nested_keys': ['audio_features'],
}


def get_json_data(json_path: str) -> dict:
    """
    Lee un archivo JSON y devuelve los datos.

    Args:
    json_path (str): La ruta al archivo JSON.

    Returns:
    dict: Los datos leídos del archivo JSON.
    """
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data


def extract_info(data: dict, keys: list) -> dict:
    """
    Extrae información específica de un diccionario.

    Args:
    data (dict): Diccionario del cual se extraerán los datos.
    keys (list): Lista de claves para extraer del diccionario.

    Returns:
    dict: Diccionario con los datos extraídos.
    """
    return {key: data.get(key) for key in keys}


def transform_data(data: dict, artist_keys: list, album_keys: list, track_keys: list, nested_keys: list) -> list:
    """
    Transforma datos de JSON anidados en una lista de diccionarios.

    Args:
    data (dict): Datos originales en formato JSON.
    artist_keys (list): Claves para extraer del artista.
    album_keys (list): Claves para extraer del álbum.
    track_keys (list): Claves para extraer de los tracks.
    nested_keys (list): Claves para datos anidados en los tracks.

    Returns:
    list: Lista de diccionarios con los datos transformados.
    """
    extracted_data = []

    artist_info = extract_info(data, artist_keys)

    for album in data.get('albums', []):
        album_info = extract_info(album, album_keys)

        for track in album.get('tracks', []):
            track_info = extract_info(track, track_keys)

            for nested_key in nested_keys:
                nested_data = track.get(nested_key, {})
                track_info.update({f'{nested_key}.{key}': value for key, value in nested_data.items()})

            combined_info = {**track_info, **artist_info, **album_info}
            extracted_data.append(combined_info)

    return extracted_data


def json_to_csv(
    json_path: str, csv_path: str, artist_keys: list, album_keys: list, track_keys: list, nested_keys: list
) -> None:
    """
    Convierte datos de un archivo JSON en un archivo CSV.

    Args:
    json_path (str): Ruta del archivo JSON.
    csv_path (str): Ruta donde se guardará el archivo CSV.
    artist_keys (list): Claves para extraer del artista.
    album_keys (list): Claves para extraer del álbum.
    track_keys (list): Claves para extraer de los tracks.
    nested_keys (list): Claves para datos anidados en los tracks.
    """
    data = get_json_data(json_path)
    transformed_data = transform_data(data, artist_keys, album_keys, track_keys, nested_keys)

    pd.DataFrame(transformed_data).to_csv(csv_path, index=False)


if __name__ == '__main__':
    json_to_csv(**SETTINGS)
