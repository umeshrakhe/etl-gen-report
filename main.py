import sys
import functions as f
import config as cfg


def run(cmd):
   prm = f.parse_parameter(cmd)
   if prm.command.startswith("gen"):
       ss = f.get_config(prm)
   else : 
       ss =00

def entrypoint():
    run(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(entrypoint())