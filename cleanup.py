
#!/usr/bin/env python3
"""
Script para limpiar la cache de Python y Node del repositorio.
Acepta parámetros para limpiar selectivamente.
"""

import argparse
import shutil
import sys
from pathlib import Path

# Patrones de cache de Python
PYTHON_CACHE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".mypy_cache",
    "*.egg-info",
    "dist",
    "build",
]

# Patrones de cache de Node
NODE_CACHE_PATTERNS = [
    "node_modules",
    ".npm",
    "package-lock.json",
]

# Directorios de reportes
REPORT_PATTERNS = [
    "reports/allure-results",
]

# Directorios a excluir por defecto
EXCLUDE_PATTERNS = [
    ".venv",
    "venv",
]


def delete_path(path: Path, verbose: bool = True) -> bool:
    """
    Elimina un archivo o directorio.
    Retorna True si se eliminó exitosamente.
    """
    try:
        if path.is_dir():
            shutil.rmtree(path)
            if verbose:
                print(f"✓ Eliminado directorio: {path}")
            return True
        elif path.is_file():
            path.unlink()
            if verbose:
                print(f"✓ Eliminado archivo: {path}")
            return True
    except Exception as e:
        print(f"✗ Error al eliminar {path}: {e}", file=sys.stderr)
        return False
    return False


def is_excluded(path: Path) -> bool:
    """
    Verifica si una ruta está dentro de un directorio excluido.
    """
    # Verificar si alguna parte de la ruta coincide con un patrón excluido
    for exclude_pattern in EXCLUDE_PATTERNS:
        if exclude_pattern in path.parts:
            return True
    return False


def clean_cache(repo_root: Path, verbose: bool = True) -> int:
    """Limpia la cache de Python y Node."""
    deleted_count = 0
    
    # Limpiar cache de Python
    print("\n🧹 Limpiando cache de Python...")
    for pattern in PYTHON_CACHE_PATTERNS:
        for path in repo_root.rglob(pattern):
            if is_excluded(path):
                continue
            if delete_path(path, verbose):
                deleted_count += 1
    
    # Limpiar cache de Node
    print("\n🧹 Limpiando cache de Node...")
    for pattern in NODE_CACHE_PATTERNS:
        for path in repo_root.rglob(pattern):
            if is_excluded(path):
                continue
            # Evitar eliminar dentro de node_modules mismo
            if path.is_dir() and path.name == "node_modules":
                if delete_path(path, verbose):
                    deleted_count += 1
            elif path.is_file():
                if delete_path(path, verbose):
                    deleted_count += 1
    
    return deleted_count


def clean_reports(repo_root: Path, verbose: bool = True) -> int:
    """Limpia los directorios de reportes."""
    deleted_count = 0
    
    print("\n📊 Limpiando reportes...")
    for pattern in REPORT_PATTERNS:
        path = repo_root / pattern
        if path.exists():
            if delete_path(path, verbose):
                deleted_count += 1
    
    return deleted_count


def main():
    parser = argparse.ArgumentParser(
        description="Limpia la cache de Python y Node del repositorio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python cleanup.py                    # Limpia todo (cache + reports)
  python cleanup.py --only-cache       # Limpia solo la cache
  python cleanup.py --only-reports     # Limpia solo los reports
  python cleanup.py -v                 # Modo verbose (mostrar todos los archivos)
        """,
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--only-cache",
        action="store_true",
        help="Limpiar solo la cache de Python y Node",
    )
    group.add_argument(
        "--only-reports",
        action="store_true",
        help="Limpiar solo los reportes",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostrar todos los archivos siendo eliminados",
    )
    
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent
    total_deleted = 0
    
    print(f"📁 Repositorio: {repo_root}")
    
    # Determinar qué limpiar
    if args.only_cache:
        total_deleted = clean_cache(repo_root, args.verbose)
    elif args.only_reports:
        total_deleted = clean_reports(repo_root, args.verbose)
    else:
        # Limpiar todo
        total_deleted += clean_cache(repo_root, args.verbose)
        total_deleted += clean_reports(repo_root, args.verbose)
    
    print(f"\n✨ Limpieza completada. {total_deleted} elemento(s) eliminado(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
