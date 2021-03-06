import argparse
import os
import yaml

from subprocess import Popen
from time import sleep


DADOS = yaml.safe_load(open('teste.yml'))
PATH_ROOT = DADOS['root']['path']
DIRETORIOS = {diretorio.name: diretorio.path
    for diretorio in os.scandir(PATH_ROOT)
    if diretorio.is_dir()}


diretorio_correto = lambda name, patterns: any(
    pattern in name for pattern in patterns)


def rodar_cenario(nome):
    for step in DADOS['cenario'][nome]:
        patterns_step = DADOS[step]['pattern']
        for diretorio, path in DIRETORIOS.items():
            if (diretorio_correto(diretorio, patterns_step)):
                process = Popen(
                    DADOS[step]['command'][0],
                    cwd=path,
                    shell=True,
                )
                with open('processos.PIDS', 'a') as arquivo_pids:
                    arquivo_pids.write('{}\n'.format(process.pid))
        sleep(DADOS[step].get('delay', 1))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('cenario', help='Nome do cenário que será utiilizado!')
    args = parser.parse_args()
    rodar_cenario(args.cenario)
