# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import os
import zipfile
import pandas as pd

def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    zip_path = os.path.join("files", "input.zip")
    unzip_base = "input"

    # 1. Descomprimir solo si no existe la carpeta 'input'
    if not os.path.exists(unzip_base):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(unzip_base)

    # 2. Detectar si hay una subcarpeta intermedia (input/input)
    contenido = os.listdir(unzip_base)
    if len(contenido) == 1 and os.path.isdir(os.path.join(unzip_base, contenido[0])):
        real_input_path = os.path.join(unzip_base, contenido[0])  # input/input
    else:
        real_input_path = unzip_base

    # 3. Cargar archivos desde subdirectorios
    def cargar_dataset(ruta_base):
        datos = []
        base_path = os.path.join(real_input_path, ruta_base)
        for sentimiento in ['positive', 'negative', 'neutral']:
            ruta = os.path.join(base_path, sentimiento)
            for archivo in os.listdir(ruta):
                archivo_path = os.path.join(ruta, archivo)
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    frase = f.read().strip()
                    datos.append({"phrase": frase, "target": sentimiento})
        return pd.DataFrame(datos)

    # 4. Crear y guardar datasets
    df_train = cargar_dataset("train")
    df_test = cargar_dataset("test")

    os.makedirs("files/output", exist_ok=True)
    df_train.to_csv("files/output/train_dataset.csv", index=False)
    df_test.to_csv("files/output/test_dataset.csv", index=False)
    