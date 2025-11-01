#!/usr/bin/env python3
"""
Script de Validación de Datos PolicySpace2 España

Este script ejecuta validaciones básicas sobre los datos cargados en la base de datos
para asegurar su calidad e integridad. Realiza verificaciones como:
- Rangos de valores válidos
- Consistencia temporal
- Completitud de datos críticos
- Detección de anomalías

Uso:
    python validate_data.py [--table NOMBRE_TABLA] [--verbose]
    
Opciones:
    --table NOMBRE_TABLA    Validar solo una tabla específica
    --verbose               Mostrar información detallada
    --export-report         Exportar reporte a archivo JSON
    
Ejemplos:
    python validate_data.py
    python validate_data.py --table poblacion_municipio --verbose
    python validate_data.py --export-report
    
Autor: PolicySpace2 España
Fecha: 2025
"""

import argparse
import sqlite3
import pandas as pd
import json
from datetime import datetime
from pathlib import Path


class DataValidator:
    """Clase para validar datos en la base de datos PolicySpace2."""
    
    def __init__(self, db_path, verbose=False):
        """
        Inicializa el validador de datos.
        
        Args:
            db_path (str): Ruta al archivo de base de datos
            verbose (bool): Si True, muestra información detallada
        """
        self.db_path = db_path
        self.verbose = verbose
        self.conn = None
        self.validation_results = {
            'timestamp': datetime.now().isoformat(),
            'database': str(db_path),
            'tables_validated': [],
            'issues_found': [],
            'warnings': [],
            'summary': {}
        }
        
    def connect(self):
        """Establece conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            if self.verbose:
                print(f"✅ Conectado a: {self.db_path}")
            return True
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            return False
            
    def close(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()
            
    def validate_table(self, table_name):
        """
        Ejecuta validaciones en una tabla específica.
        
        Args:
            table_name (str): Nombre de la tabla a validar
            
        Returns:
            dict: Resultados de la validación
        """
        if self.verbose:
            print(f"\n🔍 Validando tabla: {table_name}")
            
        results = {
            'table': table_name,
            'checks_passed': 0,
            'checks_failed': 0,
            'issues': [],
            'warnings': []
        }
        
        try:
            # Cargar datos de la tabla
            df = pd.read_sql_query(f"SELECT * FROM `{table_name}`", self.conn)
            
            if self.verbose:
                print(f"   Registros: {len(df):,}")
                print(f"   Columnas: {len(df.columns)}")
            
            # Validación 1: Verificar valores nulos en columnas críticas
            null_counts = df.isnull().sum()
            critical_null_cols = null_counts[null_counts > 0]
            
            if len(critical_null_cols) > 0:
                for col, count in critical_null_cols.items():
                    pct = (count / len(df)) * 100
                    if pct > 10:  # Más del 10% de valores nulos es un problema
                        results['issues'].append({
                            'type': 'high_null_percentage',
                            'column': col,
                            'count': int(count),
                            'percentage': round(pct, 2),
                            'severity': 'high' if pct > 50 else 'medium'
                        })
                        results['checks_failed'] += 1
                    else:
                        results['warnings'].append({
                            'type': 'some_nulls',
                            'column': col,
                            'count': int(count),
                            'percentage': round(pct, 2)
                        })
                        results['checks_passed'] += 1
            else:
                results['checks_passed'] += 1
                if self.verbose:
                    print("   ✅ Sin valores nulos críticos")
            
            # Validación 2: Verificar duplicados en columnas de identificación
            id_columns = [col for col in df.columns if 'id' in col.lower() or 'code' in col.lower()]
            for id_col in id_columns:
                if id_col in df.columns:
                    duplicates = df[id_col].duplicated().sum()
                    if duplicates > 0:
                        results['warnings'].append({
                            'type': 'duplicates',
                            'column': id_col,
                            'count': int(duplicates)
                        })
                    else:
                        results['checks_passed'] += 1
                        
            # Validación 3: Verificar rangos de valores numéricos
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            for col in numeric_cols:
                # Detectar valores negativos donde no deberían existir
                if col.lower() in ['population', 'poblacion', 'empresas', 'companies']:
                    negative_count = (df[col] < 0).sum()
                    if negative_count > 0:
                        results['issues'].append({
                            'type': 'negative_values',
                            'column': col,
                            'count': int(negative_count),
                            'severity': 'high'
                        })
                        results['checks_failed'] += 1
                    else:
                        results['checks_passed'] += 1
                        
                # Detectar outliers extremos usando IQR
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[col] < (Q1 - 3 * IQR)) | (df[col] > (Q3 + 3 * IQR))).sum()
                
                if outliers > len(df) * 0.05:  # Más del 5% son outliers
                    results['warnings'].append({
                        'type': 'high_outlier_count',
                        'column': col,
                        'count': int(outliers),
                        'percentage': round((outliers / len(df)) * 100, 2)
                    })
                    
            # Validación 4: Verificar columnas temporales (year, fecha, etc.)
            year_cols = [col for col in df.columns if 'year' in col.lower() or 'año' in col.lower()]
            for year_col in year_cols:
                if year_col in df.columns:
                    min_year = df[year_col].min()
                    max_year = df[year_col].max()
                    
                    # Verificar que los años estén en un rango razonable
                    if min_year < 1900 or max_year > 2030:
                        results['issues'].append({
                            'type': 'invalid_year_range',
                            'column': year_col,
                            'min': int(min_year),
                            'max': int(max_year),
                            'severity': 'medium'
                        })
                        results['checks_failed'] += 1
                    else:
                        results['checks_passed'] += 1
                        if self.verbose:
                            print(f"   ✅ Rango de años válido: {int(min_year)}-{int(max_year)}")
                            
        except Exception as e:
            results['issues'].append({
                'type': 'validation_error',
                'message': str(e),
                'severity': 'high'
            })
            print(f"   ❌ Error en validación: {e}")
            
        # Resumen de la tabla
        total_checks = results['checks_passed'] + results['checks_failed']
        if total_checks > 0:
            results['success_rate'] = round((results['checks_passed'] / total_checks) * 100, 2)
        else:
            results['success_rate'] = 0
            
        return results
        
    def validate_all_tables(self):
        """Valida todas las tablas en la base de datos."""
        print("\n" + "="*80)
        print("🔍 INICIANDO VALIDACIÓN DE DATOS")
        print("="*80)
        
        # Obtener lista de tablas
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📊 Tablas encontradas: {len(tables)}")
        
        # Validar cada tabla
        for table in tables:
            results = self.validate_table(table)
            self.validation_results['tables_validated'].append(results)
            
            # Agregar issues y warnings al resumen global
            self.validation_results['issues_found'].extend(results['issues'])
            self.validation_results['warnings'].extend(results['warnings'])
            
        # Generar resumen
        self.generate_summary()
        
    def validate_specific_table(self, table_name):
        """
        Valida una tabla específica.
        
        Args:
            table_name (str): Nombre de la tabla a validar
        """
        print("\n" + "="*80)
        print(f"🔍 VALIDANDO TABLA: {table_name}")
        print("="*80)
        
        results = self.validate_table(table_name)
        self.validation_results['tables_validated'].append(results)
        self.validation_results['issues_found'].extend(results['issues'])
        self.validation_results['warnings'].extend(results['warnings'])
        
        self.generate_summary()
        
    def generate_summary(self):
        """Genera un resumen de los resultados de validación."""
        total_checks = sum(t['checks_passed'] + t['checks_failed'] 
                          for t in self.validation_results['tables_validated'])
        total_passed = sum(t['checks_passed'] 
                          for t in self.validation_results['tables_validated'])
        total_failed = sum(t['checks_failed'] 
                          for t in self.validation_results['tables_validated'])
        
        self.validation_results['summary'] = {
            'total_tables': len(self.validation_results['tables_validated']),
            'total_checks': total_checks,
            'checks_passed': total_passed,
            'checks_failed': total_failed,
            'total_issues': len(self.validation_results['issues_found']),
            'total_warnings': len(self.validation_results['warnings']),
            'success_rate': round((total_passed / total_checks * 100), 2) if total_checks > 0 else 0
        }
        
    def print_report(self):
        """Imprime el reporte de validación."""
        print("\n" + "="*80)
        print("📋 REPORTE DE VALIDACIÓN")
        print("="*80)
        
        summary = self.validation_results['summary']
        print(f"\n📊 Resumen General:")
        print(f"   Tablas validadas: {summary['total_tables']}")
        print(f"   Validaciones totales: {summary['total_checks']}")
        print(f"   ✅ Pasadas: {summary['checks_passed']}")
        print(f"   ❌ Fallidas: {summary['checks_failed']}")
        print(f"   Tasa de éxito: {summary['success_rate']}%")
        
        if self.validation_results['issues_found']:
            print(f"\n⚠️  Problemas encontrados: {len(self.validation_results['issues_found'])}")
            for issue in self.validation_results['issues_found'][:10]:  # Mostrar primeros 10
                print(f"   - {issue.get('type', 'unknown')}: {issue}")
                
        if self.validation_results['warnings']:
            print(f"\n⚡ Advertencias: {len(self.validation_results['warnings'])}")
            if self.verbose:
                for warning in self.validation_results['warnings'][:10]:
                    print(f"   - {warning.get('type', 'unknown')}: {warning}")
                    
        print("\n" + "="*80)
        
    def export_report(self, output_path='validation_report.json'):
        """
        Exporta el reporte de validación a un archivo JSON.
        
        Args:
            output_path (str): Ruta del archivo de salida
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Reporte exportado a: {output_path}")


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Valida la calidad e integridad de datos en PolicySpace2',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python validate_data.py
  python validate_data.py --table poblacion_municipio --verbose
  python validate_data.py --export-report
        """
    )
    
    parser.add_argument('--table', type=str, help='Validar solo una tabla específica')
    parser.add_argument('--verbose', action='store_true', help='Mostrar información detallada')
    parser.add_argument('--export-report', action='store_true', help='Exportar reporte a JSON')
    
    args = parser.parse_args()
    
    # Determinar ruta a la base de datos
    script_dir = Path(__file__).parent
    db_path = script_dir / "data base" / "datawarehouse.db"
    
    # Verificar que existe la base de datos
    if not db_path.exists():
        print(f"❌ Error: No se encontró la base de datos en: {db_path}")
        return 1
    
    # Crear validador
    validator = DataValidator(db_path, verbose=args.verbose)
    
    # Conectar a la base de datos
    if not validator.connect():
        return 1
        
    try:
        # Ejecutar validación
        if args.table:
            validator.validate_specific_table(args.table)
        else:
            validator.validate_all_tables()
            
        # Mostrar reporte
        validator.print_report()
        
        # Exportar si se solicita
        if args.export_report:
            validator.export_report()
            
    finally:
        validator.close()
        
    # Retornar código de error si hay problemas críticos
    return 1 if validator.validation_results['summary'].get('checks_failed', 0) > 0 else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
