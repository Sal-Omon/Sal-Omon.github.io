# scripts/validate_fks.py
import sys
from app.extensions import db
# importa i modelli (caricherà i moduli dei model files)
from app.models import Artifact, Format, Creator, Location, Material, Tag, Image, ConservationReport  # importa il package models (eseguirà i file dei modelli)

def main():
    meta = db.metadata
    print("Tabelle registrate nel metadata:", sorted(meta.tables.keys()))
    problems = []
    for table_name, table in meta.tables.items():
        for fk in table.foreign_key_constraints:
            try:
                # prova a risolvere la colonna referenziata
                remote = fk.elements[0].column
                # se qui non solleva eccezioni, la FK è risolta
            except Exception as e:
                problems.append((table_name, str(fk), repr(e)))
    if problems:
        print("\nProblemi trovati nelle FK:")
        for p in problems:
            print(p)
        sys.exit(2)
    print("\nNessun problema di FK rilevato.")

if __name__ == "__main__":
    main()
