#!/usr/bin/env python3
"""
Script para fazer commit e push - contorna o erro do exclude no OneDrive.
Execute: python fazer_commit.py
"""
import os
import subprocess
import sys

# Diretório do script = pasta do projeto
PASTA = os.path.dirname(os.path.abspath(__file__))
GIT = r"C:\Program Files\Git\bin\git.exe"

def run(cmd, cwd=PASTA):
    """Executa comando e retorna (sucesso, saida)"""
    args = [GIT] + (cmd if isinstance(cmd, list) else cmd.split())
    try:
        r = subprocess.run(
            args, cwd=cwd, capture_output=True, text=True, encoding="utf-8"
        )
        out = (r.stdout or "") + (r.stderr or "")
        return r.returncode == 0, out.strip()
    except Exception as e:
        return False, str(e)

def main():
    os.chdir(PASTA)
    print(f"Pasta: {PASTA}\n")

    # 1. Corrigir exclude (evita erro no OneDrive)
    exclude_path = os.path.join(PASTA, ".git", "info", "exclude")
    try:
        with open(exclude_path, "w", encoding="ascii") as f:
            f.write("#\n")
        print("[OK] Arquivo exclude corrigido")
    except Exception as e:
        print(f"[ERRO] Não foi possível corrigir exclude: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)

    # 2. Git add
    ok, out = run("add -A")
    if not ok and "exclude" in out.lower():
        print("[ERRO] O erro do exclude persiste. Tente mover o projeto para C:\\Projetos")
        print("       (arraste a pasta para fora do OneDrive)")
        input("Pressione Enter para sair...")
        sys.exit(1)
    elif not ok:
        print(f"[AVISO] git add: {out}")
    else:
        print("[OK] git add -A")

    # 3. Mensagem do commit
    msg = input("\nMensagem do commit (Enter = auto): ").strip()
    if not msg:
        from datetime import datetime
        msg = f"Update {datetime.now().strftime('%d/%m/%Y %H:%M')}"

    # 4. Git commit
    ok, out = run(["commit", "-m", msg])
    if not ok:
        if "nothing to commit" in out.lower() or "nada a commitar" in out.lower():
            print("\nNada para commitar. Working tree limpo.")
        else:
            print(f"[ERRO] git commit: {out}")
        input("Pressione Enter para sair...")
        sys.exit(1)
    print(f"[OK] git commit: {msg[:50]}...")

    # 5. Git push
    ok, out = run("push origin main")
    if not ok:
        print(f"[ERRO] git push: {out}")
        input("Pressione Enter para sair...")
        sys.exit(1)
    print("[OK] git push - GitHub atualizado!")
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
