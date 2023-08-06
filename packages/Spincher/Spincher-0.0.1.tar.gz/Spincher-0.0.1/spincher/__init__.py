"""
An own-created type reader for Spincher
accept .spincher file
can be run on Windows
"""
__name__ = "spincher"
from .constents import *


class FileError(Exception):
      def __init__(self, *args, **kwargs):
            pass


class KeyWordError(Exception):
      def __init__(self, *args, **kwargs):
            ...


def _read_spincher(path, encode):
      if path.endswith("spincher"):
            with open(file=path, mode="r",
                      encoding=encode) as r:
                  texts = r.read()
            return texts
      else:
            raise FileError("can't support this file type [ WinError 1345 ] no expectation")


def code(path, code, code_n=3, export=(False, "")):
      if path.endswith("spincher"):
            texts = _read_spincher(path, encode="utf-8")
            texts = list(texts)
            if code == "_ord":
                  for text in range(len(texts)):
                        texts[text] = ord(texts[text])
            elif code == "_kasa":
                  for text in range(len(texts)):
                        try:
                              now_text = texts[text]
                              idx = alphas.index(now_text)
                              texts[text] = alphas[idx + code_n]
                        except:
                              continue
            else:
                  raise KeyWordError("keyword in function 'code_spincher' can only be '_ord' or '_kasa'.")
            returnTxt = [str(i) for i in texts]
            if export[0]:
                  with open(export[1], "w") as f:
                        f.write(str(returnTxt))
            return returnTxt
      else:
            raise FileError("can't support this file type [ WinError 1345 ] no expectation")


def encode(texts: list, encode, kasa_n=3, export=(False, "")):
      text = texts
      if encode == "ord_":
            for i in range(len(text)):
                  text[i] = chr(text[i])
      elif encode == "kasa_":
            for i in range(len(text)):
                  now_text = text[i]
                  idx = alphas.index(now_text)
                  text[i] = alphas[idx - kasa_n]
      else:
            raise KeyWordError("keyword in function 'encode_spincher' can only be 'ord_' or 'kasa_'.")

      return text


class Spincher:
      def __init__(self, filename):
            self.zip_end_str = ""
            self.zip_list = []
            self.filename = filename

      def create(self, encoding):
            with open(file=self.filename, mode="w", encoding=encoding) as f:
                  pass
            return f

      def write(self, content, mode="a", encoding="utf-8"):
            if mode in "wa":
                  pass
            else:
                  raise KeyWordError(f"Incorrect keyword for {__name__} : {mode}")
            with open(self.filename, mode=mode, encoding=encoding) as f:
                  f.write(content)

      def zip(self, files: list, to_file):
            self.zip_list = []
            for file in files:
                  with open(file, mode="r", encoding="utf-8") as f:
                        self.zip_list.append(f.read() + "\n")
            self.zip_end_str = "".join(self.zip_list)
            with open(to_file + ".spincher", mode="w", encoding="utf-8") as w:
                  w.write(self.zip_end_str)

            return w

