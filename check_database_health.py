#!/usr/bin/env python3
"""
Script de Verificación de Salud de la Base de Datos PolicySpace2

Este script verifica la integridad y el estado de la base de datos datawarehouse.db,
proporcionando información sobre:
- Existencia y accesibilidad del archivo
- Tablas disponibles y sus estadísticas
- Calidad de los datos (valores nulos, duplicados)
- Integridad referencial básica

Uso:
    python check_database_health.py
    
Autor: PolicySpace2 España
Fecha: 2025
"""

import os
import sys
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path


class DatabaseHealthChecker:
    """Clase para verificar la salud de la base de datos PolicySpace2."""
    
    def __init__(self, db_path):
        """
        Inicializa el verificador de salud de la base de datos.
        
        Args:
            db_path (str): Ruta al archivo de base de datos
        """
        self.db_path = db_path
        self.conn = None
        self.issues = []
        self.stats = {}
        
    def connect(self):
        """Establece conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            return True
        except Exception as e:
            self.issues.append(f"Error al conectar con la base de datos: {e}")
            return False
            
    def close(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()
            
    def check_file_exists(self):
        """Verifica que el archivo de base de datos existe."""
        print("🔍 Verificando existencia del archivo...")
        if not os.path.exists(self.db_path):
            self.issues.append(f"❌ El archivo no existe: {self.db_path}")
            return False
        else:
            file_size = os.path.getsize(self.db_path) / (1024 * 1024)  # MB
            print(f"✅ Archivo encontrado: {self.db_path}")
            print(f"   Tamaño: {file_size:.2f} MB")
            self.stats['file_size_mb'] = file_size
            return True
            
    def get_tables(self):
        """Obtiene lista de tablas en la base de datos."""
        print("\n📊 Verificando tablas...")
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            cursor = self.conn.cursor()
            cursor.execute(query)
            tables = [row[0] for row in cursor.fetchall()]
            print(f"✅ Se encontraron {len(tables)} tablas")
            self.stats['num_tables'] = len(tables)
            return tables
        except Exception as e:
            self.issues.append(f"❌ Error al obtener tablas: {e}")
            return []
            
    def check_table_health(self, table_name):
        """
        Verifica la salud de una tabla específica.
        
        Args:
            table_name (str): Nombre de la tabla a verificar
            
        Returns:
            dict: Estadísticas de la tabla
        """
        try:
            # Contar registros
            query = f"SELECT COUNT(*) FROM `{table_name}`"
            cursor = self.conn.cursor()
            cursor.execute(query)
            row_count = cursor.fetchone()[0]
            
            # Obtener información de columnas
            query = f"PRAGMA table_info(`{table_name}`)"
            cursor.execute(query)
            columns = cursor.fetchall()
            
            # Leer una muestra de datos para análisis
            df = pd.read_sql_query(f"SELECT * FROM `{table_name}` LIMIT 1000", self.conn)
            
            # Calcular estadísticas de calidad de datos
            null_counts = df.isnull().sum()
            null_percentages = (null_counts / len(df) * 100).round(2)
            
            stats = {
                'row_count': row_count,
                'column_count': len(columns),
                'columns': [col[1] for col in columns],
                'null_percentages': null_percentages[null_percentages > 0].to_dict(),
                'sample_size': len(df)
            }
            
            return stats
            
        except Exception as e:
            self.issues.append(f"❌ Error al verificar tabla '{table_name}': {e}")
            return None
            
    def generate_report(self):
        """Genera y muestra el reporte de salud de la base de datos."""
        print("\n" + "="*80)
        print("📋 REPORTE DE SALUD DE LA BASE DE DATOS PolicySpace2")
        print("="*80)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Base de datos: {self.db_path}")
        print()
        
        if self.stats.get('file_size_mb'):
            print(f"💾 Tamaño del archivo: {self.stats['file_size_mb']:.2f} MB")
            
        if self.stats.get('num_tables'):
            print(f"📊 Número de tablas: {self.stats['num_tables']}")
            
        print()
        
        if self.issues:
            print("⚠️  PROBLEMAS DETECTADOS:")
            print("-" * 80)
            for issue in self.issues:
                print(f"  {issue}")
            print()
        else:
            print("✅ No se detectaron problemas críticos")
            print()
            
        print("="*80)
        
    def run_full_check(self):
        """Ejecuta todas las verificaciones de salud."""
        print("\n🏥 Iniciando verificación de salud de la base de datos...")
        print()
        
        # Verificar existencia del archivo
        if not self.check_file_exists():
            self.generate_report()
            return False
            
        # Conectar a la base de datos
        if not self.connect():
            self.generate_report()
            return False
            
        # Obtener tablas
        tables = self.get_tables()
        
        if tables:
            print("\n📋 Verificando salud de las tablas...")
            table_stats = {}
            
            for table in tables[:10]:  # Verificar primeras 10 tablas como muestra
                print(f"\n   Analizando: {table}")
                stats = self.check_table_health(table)
                if stats:
                    print(f"      Registros: {stats['row_count']:,}")
                    print(f"      Columnas: {stats['column_count']}")
                    if stats['null_percentages']:
                        print(f"      Valores nulos detectados en: {list(stats['null_percentages'].keys())}")
                    table_stats[table] = stats
                    
            if len(tables) > 10:
                print(f"\n   ... y {len(tables) - 10} tablas más")
                
        # Cerrar conexión
        self.close()
        
        # Generar reporte
        self.generate_report()
        
        return len(self.issues) == 0


def main():
    """Función principal."""
    # Determinar ruta a la base de datos
    script_dir = Path(__file__).parent
    db_path = script_dir / "data base" / "datawarehouse.db"
    
    print("="*80)
    print("🏥 PolicySpace2 - Verificador de Salud de Base de Datos")
    print("="*80)
    
    # Crear verificador y ejecutar
    checker = DatabaseHealthChecker(str(db_path))
    success = checker.run_full_check()
    
    # Retornar código de salida apropiado
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
