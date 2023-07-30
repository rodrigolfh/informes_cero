import pandas as pd
from datetime import date
import msoffcrypto
import io
from .models import Paciente, Usuario, InformeFormularios, Establecimiento
from datetime import datetime
"""
registro=pd.read_excel('archivos/Informe_Formularios_RAYEN_4.xlsx', header=16) #los headers de las columnas comienzan en la fila 17

registro.head() #las primeras 5 filas
registro.tail() #las últimas 5 filas
registro.head(15) #las primeras 5 filas
headers = registro.loc[0] #fila 1
headers.to_list() # como lista
headers.to_string() #como string
diccionario = {'dato1' : 11}
df = pd.DataFrame(diccionario, index = ["day1", "day2", "day3"]) #índices con nombres. esto se usa al pasar un dict a un dataframe.
registro.loc["nombre de columna"] #serie por nombre de columna

"""



headers = [
    'SERVICIO SALUD',
    'ESTABLECIMIENTO',
    'RUT',
    'DV',
    'CODIGO FAMILIA',
    'NUMERO DE FICHA RAYEN',
    'NUMERO DE FICHA CODIGO ANTIGUO',
    'PACIENTE',
    'FECHA DE NACIMIENTO',
    'EDAD PACIENTE',
    'AÑO APLICACIÓN FORMULARIO',
    'MES APLICACIÓN FORMULARIO',
    'DÍAS APLICACIÓN FORMULARIO',
    'PUEBLO ORIGINARIO',
    'ALERTAS ADMINISTRATIVAS',
    'NACIONALIDAD',
    'SEXO',
    'SECTOR INSCRIPCION',
    'SECTOR CITA',
    'DIRECCIÓN',
    'COMUNA',
    'TELEFONO 1',
    'TELEFONO 2',
    'PREVISION',
    'CONVENIO',
    'SITUACION',
    'ESTADO',
    'FUNCIONARIO PASIVADOR',
    'ATEN ID',
    'FECHA ATENCION',
    'FECHA FORMULARIO',
    'FUNCIONARIO',
    'INSTRUMENTO',
    'ESTABLECIMIENTO INSCRIPCION',
    'FORMULARIO',
    'FUNCIONARIOS FORMULARIO',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '19',
    '20',
    '21',
    '22',
    '23',
    '24',
    '25',
    '26',
    '27',
    '28',
    '29',
    '30',
    '31',
    '32',
    '33',
    '34',
    '35',
    '36',
    '37',
    '38',
    '39',
    '40',
    '41',
    '42',
    '43',
    '44',
    '45',
    '46',
    '47',
    '48',
    '49',
    '50',
    '51',
    '52',
    '53'
]

preguntas = {
    '1': '¿EL NIÑO(A) PRESENTA UNA CONDICIÓN QUE DISMINUYA SU FLUJO SALIVAL (ENFERMEDADES, CONSUMO DE FÁRMACOS, ETC)?',
    '2': '¿EL NIÑO(A) PRESENTA UNA CONDICIÓN QUE DISMINUYA SU FLUJO SALIVAL? DE 6 A 9 AÑOS',
    '3': '¿EL O LA ADOLESCENTE PRESENTA UNA CONDICIÓN QUE DI',
    '4': '¿EL NIÑO(A) PRESENTA SITUACIÓN DE DISCAPACIDAD?',
    '5': '¿EL NIÑO(A) PRESENTA SITUACIÓN DE DISCAPACIDAD? DE 6 A 9 AÑOS',
    '6': '¿EL O LA ADOLESCENTE PRESENTA SITUACIÓN DE DISCAPA',
    '7': '¿EL NIÑO PRESENTA  LESIONES DE CARIES CAVITADAS O',
    '8': '¿EL NIÑO PRESENTA  LESIONES DE CARIES O COPD &AMP;GT;0?',
    '9': '¿EL/LA ADOLESCENTE PRESENTA  MANCHAS BLANCAS, COPD',
    '10': '¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL NIÑ(A)? DE 0 A 5 AÑOS',
    '11': '¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL NIÑ(A)? DE 6 A 9 AÑOS',
    '12': '¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL/LA ADOLESCENT',
    '13': 'LOS PADRES Y/O CUIDADORES, ¿LE LAVAN LOS DIENTES AL NIÑO(A)? DE 0 A 5 AÑOS',
    '14': 'LOS PADRES Y/O CUIDADORES, ¿SUPERVISAN EL LAVADO D',
    '15': '¿CUÁNTAS VECES AL DÍA SE LAVA LOS DIENTES EL/LA AD',
    '16': '¿CUÁNTAS VECES AL DÍA LE LAVAN LOS DIENTES AL NIÑO (A) EN LA CASA? DE 0 A 5 AÑOS',
    '17': '¿CUÁNTAS VECES AL DÍA LE LAVAN LOS DIENTES AL NIÑO (A) EN LA CASA? DE 6 A 9 AÑOS',
    '18': '¿EL/LA ADOLESCENTE, SE LAVA LOS DIENTES ANTES DE I',
    '19': '¿EL NIÑO O NIÑA, SE LAVA LOS DIENTES ANTES DE IR A DORMIR? DE 0 A 5 AÑOS',
    '20': '¿EL NIÑO O NIÑA, SE LAVA LOS DIENTES ANTES DE IR A DORMIR? DE 6 A 9 AÑOS',
    '21': '¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 0 A 2 AÑOS',
    '22': '¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 3 A 5 AÑOS',
    '23': '¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS',
    '24': '¿CUÁNTAS VECES AL DÍA EL/LA ADOLESCENTE INGIERE AL',
    '25': '¿EN QUÉ MOMENTO EL NIÑO(A) REALIZA LA INGESTA DE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 0 A 5 AÑOS',
    '26': '¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS',
    '27': '¿EN QUÉ MOMENTO EL/LA ADOLESCENTE REALIZA LA INGES',
    '28': 'SI EL NIÑO(A) TOMA LIQUIDOS AZUCARADOS EN MAMADERA',
    '29': '¿EN QUÉ MOMENTO EL NIÑO(A) REALIZA LA INGESTA DE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 6 A 9 AÑOS',
    '30': '¿EL ADOLESCENTE CONSUME ALIMENTOS O LÍQUIDOS AZUCA',
    '31': 'SI EL NIÑO(A) INGIERE LÍQUIDOS Y/O LIMENTOS DESPUÉ',
    '32': '¿UTILIZA EL NIÑO O NIÑA PASTA DE DIENTES CON 1.000',
    '33': '¿UTILIZA EL NIÑO O NIÑA PASTA DE DIENTES CON 1.000-1.500 PPM DE  FLÚOR? DE 6 A 9',
    '34': '¿UTILIZA EL/LA ADOLESCENTE PASTA DE DIENTES CON 1.',
    '35': '¿CUÁL CREE QUE ES LA MOTIVACIÓN DE LOS PADRES/CUIDADORES EN EL CUIDADO ORAL DEL NIÑO(A)? DE 0 A 5 AÑOS',
    '36': 'LUEGO DE LAS PREGUNTAS ANTERIORES, SEGÚN USTED (DE',
    '37': 'LUEGO DE LAS PREGUNTAS ANTERIORES, SEGÚN USTED (DE',
    '38': '¿EL NIÑO(A) SE SUCCIONA EL DEDO DE MANERA PERSISTENTE? DE 0 A 5 AÑOS',
    '39': '¿EL NIÑO(A) SE SUCCIONA EL DEDO DE MANERA PERSISTENTE? DE 6 A 9 AÑOS',
    '40': '¿EL/LA ADOLESCENTE PRESENTA MALOS HÁBITOS DE ONICO',
    '41': '¿EL NIÑO(A) OCUPA CHUPETE ENTRETENCIÓN, MAMADERA U OTRO OBJETO? DE 0 A 5 AÑOS',
    '42': '¿EL NIÑO(A) OCUPA CHUPETE ENTRETENCIÓN, MAMADERA U OTRO OBJETO? DE 6 A 9 AÑOS',
    '43': '¿EL/LA ADOLESCENTE MANIFIESTA CONSUMO DE TABACO, A',
    '44': '¿EL NIÑO(A) PRESENTA MAL OCLUSIONES? DE 0 A 5 AÑOS',
    '45': '¿EL NIÑO(A) PRESENTA MAL OCLUSIONES? DE 6 A 9 AÑOS',
    '46': '¿EL/LA ADOLESCENTE PRESENTA MAL OCLUSIONES?',
    '47': 'RESULTADO EVALUACIÓN DE RIESGO DE 0 A 5 AÑOS',
    '48': 'RESULTADO EVALUACIÓN DE RIESGO DE 6 A 9 AÑOS',
    '49': 'RESULTADO EVALUACIÓN DE RIESGO DE 10 A 19 AÑOS',
    '50': 'FECHA PRÓXIMO CONTROL DE 0 A 5 AÑOS',
    '51': 'RESULTADO EVALUACIÓN DE RIESGO FECHA PROXIMO CONTROL DE 6 A 9 ÑOS',
    '52': 'FECHA PRÓXIMO CONTROL DE 10 A 19 AÑOS',
    '53': 'ESTADO'
}


# LISTO: CORROBORAR QUE EL ARCHIVO SEA XLSX (doble, antes de subir en el view y después de subir en la función 'xslx')
# LISTO: Corroborar comuna

# TODO:  QUE TENGA EL NOMBRE DE UN CESFAM DE LA LISTA (PEDIRLE A CRISTIAN OTRAS PLANILLAS)

# LISTO: FECHA HASTA - DESDE = UN AÑO, CORROBORA QUE SEA UN INFORME DE UN AÑO Y UN MES CORRIDO 

# LISTO: FORMULARIO: QUE TENGA '(CER0)'
# LISTO: TODOS LOS METACAMPOS = tRUE, SITUACIÓN= TODOS, ESTADO: AMBOS EDAD INICIAL=0, FINAL MAYR A 20, SEXO AMBOS
# LISTO: CORROBORAR QUE ESTÉ CADA COLUMNA


# cambiar símbolos.


archivo = './archivos/Informe_Formularios_RAYEN_4.xlsx'
"""

class CargarInformeFormularios(BaseCommand):
    help = 'Load data from a pandas DataFrame into the SQLite database'

    def handle(self, *args, **kwargs):

        df = pd.read_csv('your_dataframe.csv')

        # Convert DataFrame rows to Django objects and save them to the database
        for _, row in df.iterrows():
            obj = Infor(
                column1=row['column1'],
                column2=row['column2'],
                # Add other fields as needed
            )
            obj.save()

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
"""



class Validar(): 
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.archivo_df = pd.read_excel(nombre_archivo, nrows=16) #guardar dataframe del excel, sólo hasta la línea 16 para hacer las validaciones
        self.si = '✅'
        self.no = '❌'
        #self.contexto = {}
    
    try:
        def xlsx(self):
    
            if self.nombre_archivo.endswith(".xlsx"):
                return self.si
            else:
                return self.no
        
        def comuna(self):
            comuna = 'Vallenar'
            if comuna in str(self.archivo_df.iat[2, 1]):
                return self.si
            else:
                return self.no
    
        
        def cesfam(self):
            cesfam = ['Estación', 'Baquedano', 'Carrera', 'Joan Crawford']
            for centro in cesfam:
                if centro in str(self.archivo_df.iat[3,1].strip()):
                    return self.si
                else:
                    pass
            return self.no
    
        def formulario(self):
            formulario_valor = '(CERO)'
            if formulario_valor in str(self.archivo_df.iat[6,1]):
                return self.si
            else:
                return self.no
    
        def metacampos(self):
            metacampos_valor = 'True'
            if metacampos_valor in str(self.archivo_df.iat[7,1]):
                return self.si
            else:
                return self.no
    
        def situación(self):
            situacion_valor = 'Todos'
            if situacion_valor in str(self.archivo_df.iat[9,1]):
                return self.si
            else:
                return self.no
    
        def estado(self):
            estado_valor = 'Ambos'
            if estado_valor in str(self.archivo_df.iat[10,1]):
                return self.si
            else:
                return self.no
        
        def rango_tiempo(self):
            #convertir el string en lista, dar vuelta los valores y transformar en objetos date
            desde = str(self.archivo_df.iat[4, 1])
            desde.strip()
            if "/" in desde:
                desde = desde.split("/")
                desde.reverse()
      
                desde_día = int(desde[2])
                desde_mes = int(desde[1])
                desde_año = int(desde[0])

                desde = date(desde_año, desde_mes, desde_día)
            else:
                return self.no

            
            hasta = str(self.archivo_df.iat[5, 1])
            
            if "/" in hasta:
                hasta.strip()
                hasta = hasta.split("/")
                hasta.reverse()
                hasta_día = int(hasta[2])
                hasta_mes = int(hasta[1])
                hasta_año = int(hasta[0])

                hasta = date(hasta_año, hasta_mes, hasta_día)
        
                diferencia_fechas = hasta - desde #diferencia

                if diferencia_fechas.days >= 295: #si la diferencia de fechas es 1 año y 1 mes o más,
                    return self.si
            else:
                return self.no
        

        def edad(self):
            if isinstance(int(self.archivo_df.iat[11, 1]), int) and isinstance(int(self.archivo_df.iat[12, 1]), int):
                edad_inicial = int(self.archivo_df.iat[11, 1])
                edad_final = int(self.archivo_df.iat[12, 1])
            
            else:
                edad_inicial = 0
                edad_final = 0
                
            if ((edad_final - edad_inicial) >= 9) and (edad_inicial == 0): #siempre desde cero, y al menos hasta los 9 años
                return self.si
            else:
                return self.no
        

        def sexo(self):
            sexo_valor = 'Ambos'
            if sexo_valor in self.archivo_df.iat[13,1]:
                return self.si
            else:
                return self.no


#funcion pandas

        def columnas(self): # corrobora que estén todas las columnas, y en la línea que corresponde
            columnas_referencia = ['SERVICIO SALUD',
    'ESTABLECIMIENTO',
    'RUT',
    'DV',
    'CODIGO FAMILIA',
    'NUMERO DE FICHA RAYEN',
    'NUMERO DE FICHA CODIGO ANTIGUO',
    'PACIENTE',
    'FECHA DE NACIMIENTO',
    'EDAD PACIENTE',
    'AÑO APLICACIÓN FORMULARIO',
    'MES APLICACIÓN FORMULARIO',
    'DÍAS APLICACIÓN FORMULARIO',
    'PUEBLO ORIGINARIO',
    'ALERTAS ADMINISTRATIVAS',
    'NACIONALIDAD',
    'SEXO',
    'SECTOR INSCRIPCION',
    'SECTOR CITA',
    'DIRECCIÓN',
    'COMUNA',
    'TELEFONO 1',
    'TELEFONO 2',
    'PREVISION',
    'CONVENIO',
    'SITUACION',
    'ESTADO',
    'FUNCIONARIO PASIVADOR',
    'ATEN ID',
    'FECHA ATENCION',
    'FECHA FORMULARIO',
    'FUNCIONARIO',
    'INSTRUMENTO',
    'ESTABLECIMIENTO INSCRIPCION',
    'FORMULARIO',
    'FUNCIONARIOS FORMULARIO',
    '1.- ¿EL NIÑO(A) PRESENTA UNA CONDICIÓN QUE DISMINUYA SU FLUJO SALIVAL (ENFERMEDADES, CONSUMO DE FÁRMACOS, ETC)?',
    '2.- ¿EL NIÑO(A) PRESENTA UNA CONDICIÓN QUE DISMINUYA SU FLUJO SALIVAL? DE 6 A 9 AÑOS',
    '3.- ¿EL O LA ADOLESCENTE PRESENTA UNA CONDICIÓN QUE DI',
    '4.- ¿EL NIÑO(A) PRESENTA SITUACIÓN DE DISCAPACIDAD?',
    '5.- ¿EL NIÑO(A) PRESENTA SITUACIÓN DE DISCAPACIDAD? DE 6 A 9 AÑOS',
    '6.- ¿EL O LA ADOLESCENTE PRESENTA SITUACIÓN DE DISCAPA',
    '7.- ¿EL NIÑO PRESENTA  LESIONES DE CARIES CAVITADAS O ',
    '8.- ¿EL NIÑO PRESENTA  LESIONES DE CARIES O COPD &AMP;GT;0?',
    '9.- ¿EL/LA ADOLESCENTE PRESENTA  MANCHAS BLANCAS, COPD',
    '10.- ¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL NIÑ(A)? DE 0 A 5 AÑOS',
    '11.- ¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL NIÑ(A)? DE 6 A 9 AÑOS',
     '12.- ¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL/LA ADOLESCENT',
    '13.- LOS PADRES Y/O CUIDADORES, ¿LE LAVAN LOS DIENTES AL NIÑO(A)? DE 0 A 5 AÑOS',
    '14.- LOS PADRES Y/O CUIDADORES, ¿SUPERVISAN EL LAVADO D',
    '15.- ¿CUÁNTAS VECES AL DÍA SE LAVA LOS DIENTES EL/LA AD',
    '16.- ¿CUÁNTAS VECES AL DÍA LE LAVAN LOS DIENTES AL NIÑO (A) EN LA CASA? DE 0 A 5 AÑOS',
    '17.- ¿CUÁNTAS VECES AL DÍA LE LAVAN LOS DIENTES AL NIÑO (A) EN LA CASA? DE 6 A 9 AÑOS',
    '18.- ¿EL/LA ADOLESCENTE, SE LAVA LOS DIENTES ANTES DE I',
    '19.- ¿EL NIÑO O NIÑA, SE LAVA LOS DIENTES ANTES DE IR A DORMIR? DE 0 A 5 AÑOS',
    '20.- ¿EL NIÑO O NIÑA, SE LAVA LOS DIENTES ANTES DE IR A DORMIR? DE 6 A 9 AÑOS',
    '21.- ¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 0 A 2 AÑOS',
    '22.- ¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 3 A 5 AÑOS',
    '23.- ¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS',
    '24.- ¿CUÁNTAS VECES AL DÍA EL/LA ADOLESCENTE INGIERE AL',
    '25.- ¿EN QUÉ MOMENTO EL NIÑO(A) REALIZA LA INGESTA DE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 0 A 5 AÑOS',
    '26.- ¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS',
    '27.- ¿EN QUÉ MOMENTO EL/LA ADOLESCENTE REALIZA LA INGES',
    '28.- SI EL NIÑO(A) TOMA LIQUIDOS AZUCARADOS EN MAMADERA',
    '29.- ¿EN QUÉ MOMENTO EL NIÑO(A) REALIZA LA INGESTA DE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 6 A 9 AÑOS',
    '30.- ¿EL ADOLESCENTE CONSUME ALIMENTOS O LÍQUIDOS AZUCA',
    '31.- SI EL NIÑO(A) INGIERE LÍQUIDOS Y/O LIMENTOS DESPUÉ',
    '32.- ¿UTILIZA EL NIÑO O NIÑA PASTA DE DIENTES CON 1.000',
    '33.- ¿UTILIZA EL NIÑO O NIÑA PASTA DE DIENTES CON 1.000-1.500 PPM DE  FLÚOR? DE 6 A 9',
    '34.- ¿UTILIZA EL/LA ADOLESCENTE PASTA DE DIENTES CON 1.',
    '35.- ¿CUÁL CREE QUE ES LA MOTIVACIÓN DE LOS PADRES/CUIDADORES EN EL CUIDADO ORAL DEL NIÑO(A)? DE 0 A 5 AÑOS',
    '36.- LUEGO DE LAS PREGUNTAS ANTERIORES, SEGÚN USTED (DE',
    '37.- LUEGO DE LAS PREGUNTAS ANTERIORES, SEGÚN USTED (DE',
    '38.- ¿EL NIÑO(A) SE SUCCIONA EL DEDO DE MANERA PERSISTENTE? DE 0 A 5 AÑOS',
    '39.- ¿EL NIÑO(A) SE SUCCIONA EL DEDO DE MANERA PERSISTENTE? DE 6 A 9 AÑOS',
    '40.- ¿EL/LA ADOLESCENTE PRESENTA MALOS HÁBITOS DE ONICO',
    '41.- ¿EL NIÑO(A) OCUPA CHUPETE ENTRETENCIÓN, MAMADERA U OTRO OBJETO? DE 0 A 5 AÑOS',
    '42.- ¿EL NIÑO(A) OCUPA CHUPETE ENTRETENCIÓN, MAMADERA U OTRO OBJETO? DE 6 A 9 AÑOS',
    '43.- ¿EL/LA ADOLESCENTE MANIFIESTA CONSUMO DE TABACO, A',
    '44.- ¿EL NIÑO(A) PRESENTA MAL OCLUSIONES? DE 0 A 5 AÑOS',
    '45.- ¿EL NIÑO(A) PRESENTA MAL OCLUSIONES? DE 6 A 9 AÑOS',
    '46.- ¿EL/LA ADOLESCENTE PRESENTA MAL OCLUSIONES?',
    '47.- RESULTADO EVALUACIÓN DE RIESGO DE 0 A 5 AÑOS',
    '48.- RESULTADO EVALUACIÓN DE RIESGO DE 6 A 9 AÑOS',
    '49.- RESULTADO EVALUACIÓN DE RIESGO DE 10 A 19 AÑOS',
    '50.- FECHA PRÓXIMO CONTROL DE 0 A 5 AÑOS',
    '51.- RESULTADO EVALUACIÓN DE RIESGO FECHA PROXIMO CONTROL DE 6 A 9 ÑOS',
    '52.- FECHA PRÓXIMO CONTROL DE 10 A 19 AÑOS',
    '53.- ESTADO']
            columnas_referencia_b = ['SERVICIO SALUD',
    'ESTABLECIMIENTO',
    'RUT',
    'DV',
    'CODIGO FAMILIA',
    'NUMERO DE FICHA RAYEN',
    'NUMERO DE FICHA CODIGO ANTIGUO',
    'PACIENTE',
    'FECHA DE NACIMIENTO',
    'EDAD PACIENTE',
    'AÑO APLICACIÓN FORMULARIO',
    'MES APLICACIÓN FORMULARIO',
    'DÍAS APLICACIÓN FORMULARIO',
    'PUEBLO ORIGINARIO',
    'ALERTAS ADMINISTRATIVAS',
    'NACIONALIDAD',
    'SEXO',
    'SECTOR INSCRIPCION',
    'SECTOR CITA',
    'DIRECCIÓN',
    'COMUNA',
    'TELEFONO 1',
    'TELEFONO 2',
    'PREVISION',
    'CONVENIO',
    'SITUACION',
    'ESTADO',
    'FUNCIONARIO PASIVADOR',
    'ATEN ID',
    'FECHA ATENCION',
    'FECHA FORMULARIO',
    'FUNCIONARIO',
    'INSTRUMENTO',
    'ESTABLECIMIENTO INSCRIPCION',
    'FORMULARIO',
    'FUNCIONARIOS FORMULARIO',
    '1.- ¿EL NIÑO(A) PRESENTA UNA CONDICIÓN QUE DISMINUYA SU FLUJO SALIVAL (ENFERMEDADES, CONSUMO DE FÁRMACOS, ETC)?',
    '2.- ¿EL NIÑO(A) PRESENTA UNA CONDICIÓN QUE DISMINUYA SU FLUJO SALIVAL? DE 6 A 9 AÑOS',
    '3.- ¿EL O LA ADOLESCENTE PRESENTA UNA CONDICIÓN QUE DI',
    '4.- ¿EL NIÑO(A) PRESENTA SITUACIÓN DE DISCAPACIDAD?',
    '5.- ¿EL NIÑO(A) PRESENTA SITUACIÓN DE DISCAPACIDAD? DE 6 A 9 AÑOS',
    '6.- ¿EL O LA ADOLESCENTE PRESENTA SITUACIÓN DE DISCAPA',
    '7.- ¿EL NIÑO PRESENTA  LESIONES DE CARIES CAVITADAS O ',
    '8.- ¿EL NIÑO PRESENTA  LESIONES DE CARIES O COPD &AMP;GT;0?',
    '9.- ¿EL/LA ADOLESCENTE PRESENTA  MANCHAS BLANCAS, COPD',
    '10.- ¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL NIÑ(A)? DE 0 A 5 AÑOS',
    '11.- ¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL NIÑ(A)? DE 6 A 9 AÑOS',
    '12.- ¿CUÁL ES EL ESTADO DE LAS ENCÍAS DEL/LA ADOLESCENT',
    '13.- LOS PADRES Y/O CUIDADORES, ¿LE LAVAN LOS DIENTES AL NIÑO(A)? DE 0 A 5 AÑOS',
    '14.- LOS PADRES Y/O CUIDADORES, ¿SUPERVISAN EL LAVADO D',
    '15.- ¿CUÁNTAS VECES AL DÍA SE LAVA LOS DIENTES EL/LA AD',
    '16.- ¿CUÁNTAS VECES AL DÍA LE LAVAN LOS DIENTES AL NIÑO (A) EN LA CASA? DE 0 A 5 AÑOS',
    '17.- ¿CUÁNTAS VECES AL DÍA LE LAVAN LOS DIENTES AL NIÑO (A) EN LA CASA? DE 6 A 9 AÑOS',
    '18.- ¿EL/LA ADOLESCENTE, SE LAVA LOS DIENTES ANTES DE I',
    '19.- ¿EL NIÑO O NIÑA, SE LAVA LOS DIENTES ANTES DE IR A DORMIR? DE 0 A 5 AÑOS',
    '20.- ¿EL NIÑO O NIÑA, SE LAVA LOS DIENTES ANTES DE IR A DORMIR? DE 6 A 9 AÑOS',
    '21.- ¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 0 A 2 AÑOS',
    '22.- ¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 3 A 5 AÑOS',
    '23.- ¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS',
    '24.- ¿CUÁNTAS VECES AL DÍA EL/LA ADOLESCENTE INGIERE AL',
    '25.- ¿EN QUÉ MOMENTO EL NIÑO(A) REALIZA LA INGESTA DE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 0 A 5 AÑOS',
    '26.- ¿CUÁNTAS VECES AL DÍA EL NIÑO(A) INGIERE ALIMENTOS',
    '27.- ¿EN QUÉ MOMENTO EL/LA ADOLESCENTE REALIZA LA INGES',
    '28.- SI EL NIÑO(A) TOMA LIQUIDOS AZUCARADOS EN MAMADERA',
    '29.- ¿EN QUÉ MOMENTO EL NIÑO(A) REALIZA LA INGESTA DE ALIMENTOS Y/O LÍQUIDOS AZUCARADOS? DE 6 A 9 AÑOS',
    '30.- ¿EL ADOLESCENTE CONSUME ALIMENTOS O LÍQUIDOS AZUCA',
    '31.- SI EL NIÑO(A) INGIERE LÍQUIDOS Y/O LIMENTOS DESPUÉ',
    '32.- ¿UTILIZA EL NIÑO O NIÑA PASTA DE DIENTES CON 1.000',
    '33.- ¿UTILIZA EL NIÑO O NIÑA PASTA DE DIENTES CON 1.000-1.500 PPM DE  FLÚOR? DE 6 A 9',
    '34.- ¿UTILIZA EL/LA ADOLESCENTE PASTA DE DIENTES CON 1.',
    '35.- ¿CUÁL CREE QUE ES LA MOTIVACIÓN DE LOS PADRES/CUIDADORES EN EL CUIDADO ORAL DEL NIÑO(A)? DE 0 A 5 AÑOS',
    '36.- LUEGO DE LAS PREGUNTAS ANTERIORES, SEGÚN USTED (DE',
    '37.- LUEGO DE LAS PREGUNTAS ANTERIORES, SEGÚN USTED (DE',
    '38.- ¿EL NIÑO(A) SE SUCCIONA EL DEDO DE MANERA PERSISTENTE? DE 0 A 5 AÑOS',
    '39.- ¿EL NIÑO(A) SE SUCCIONA EL DEDO DE MANERA PERSISTENTE? DE 6 A 9 AÑOS',
    '40.- ¿EL/LA ADOLESCENTE PRESENTA MALOS HÁBITOS DE ONICO',
    '41.- ¿EL NIÑO(A) OCUPA CHUPETE ENTRETENCIÓN, MAMADERA U OTRO OBJETO? DE 0 A 5 AÑOS',
    '42.- ¿EL NIÑO(A) OCUPA CHUPETE ENTRETENCIÓN, MAMADERA U OTRO OBJETO? DE 6 A 9 AÑOS',
    '43.- ¿EL/LA ADOLESCENTE MANIFIESTA CONSUMO DE TABACO, A',
    '44.- ¿EL NIÑO(A) PRESENTA MAL OCLUSIONES? DE 0 A 5 AÑOS',
    '45.- ¿EL NIÑO(A) PRESENTA MAL OCLUSIONES? DE 6 A 9 AÑOS',
    '46.- ¿EL/LA ADOLESCENTE PRESENTA MAL OCLUSIONES?',
    '47.- RESULTADO EVALUACIÓN DE RIESGO DE 0 A 5 AÑOS',
    '48.- RESULTADO EVALUACIÓN DE RIESGO DE 6 A 9 AÑOS',
    '49.- RESULTADO EVALUACIÓN DE RIESGO DE 10 A 19 AÑOS',
    '50.- FECHA PRÓXIMO CONTROL DE 0 A 5 AÑOS',
    '51.- FECHA PRÓXIMO CONTROL DE 6 A 9 AÑOS',
    '52.- FECHA PRÓXIMO CONTROL DE 10 A 19 AÑOS',
    '53.- ESTADO']
            columnas_archivo = self.archivo_df.iloc[15].tolist()
        
            if (columnas_referencia == columnas_archivo) or (columnas_referencia_b == columnas_archivo):
                return self.si
            else:
                return self.no
    except TypeError:
        print("Archivo Incorrecto")
    
def generar_contexto_validacion(dataframe): 
    contexto = {}

    contexto['nombre'] = dataframe.nombre_archivo
    contexto['xlsx'] = dataframe.xlsx()
    contexto['comuna'] = dataframe.comuna()
    contexto['cesfam'] = dataframe.cesfam()
    contexto['formulario'] = dataframe.formulario()
    contexto['metacampos'] = dataframe.metacampos()
    contexto['situación'] = dataframe.situación()
    contexto['estado'] = dataframe.estado()
    contexto['rango_tiempo'] = dataframe.rango_tiempo()
    contexto['edad'] = dataframe.edad()
    contexto['sexo'] = dataframe.sexo()
    contexto['columnas'] = dataframe.columnas()


    if dataframe.no in contexto.values(): #para saber si hubo problemas
        contexto['validaciones'] = False
    else:
        contexto['validaciones'] = True

    contexto['hecho'] = True
    return contexto

columnas_referencia_c = ['SERVI',
 'ESTAB',
 'RUT',
 'DV',
 'CODIG',
 'NUMER',
 'NUMER',
 'PACIE',
 'FECHA',
 'EDAD ',
 'AÑO A',
 'MES A',
 'DÍAS ',
 'PUEBL',
 'ALERT',
 'NACIO',
 'SEXO',
 'SECTO',
 'SECTO',
 'DIREC',
 'COMUN',
 'TELEF',
 'TELEF',
 'PREVI',
 'CONVE',
 'SITUA',
 'ESTAD',
 'FUNCI',
 'ATEN ',
 'FECHA',
 'FECHA',
 'FUNCI',
 'INSTR',
 'ESTAB',
 'FORMU',
 'FUNCI',
 '1.- ¿',
 '2.- ¿',
 '3.- ¿',
 '4.- ¿',
 '5.- ¿',
 '6.- ¿',
 '7.- ¿',
 '8.- ¿',
 '9.- ¿',
 '10.- ',
 '11.- ',
 '12.- ',
 '13.- ',
 '14.- ',
 '15.- ',
 '16.- ',
 '17.- ',
 '18.- ',
 '19.- ',
 '20.- ',
 '21.- ',
 '22.- ',
 '23.- ',
 '24.- ',
 '25.- ',
 '26.- ',
 '27.- ',
 '28.- ',
 '29.- ',
 '30.- ',
 '31.- ',
 '32.- ',
 '33.- ',
 '34.- ',
 '35.- ',
 '36.- ',
 '37.- ',
 '38.- ',
 '39.- ',
 '40.- ',
 '41.- ',
 '42.- ',
 '43.- ',
 '44.- ',
 '45.- ',
 '46.- ',
 '47.- ',
 '48.- ',
 '49.- ',
 '50.- ',
 '51.- ',
 '52.- ',
 '53.- ']


def string_a_fecha(fecha_string):
    fecha_string.replace("'", "") # viene con una ' al comienzo a veces
    
    try:
        parsed_date = datetime.strptime(fecha_string, "%d/%m/%Y")
    except ValueError:            
        return None

    return parsed_date.date()

def string_a_fecha_hora(fechahora_string):
    fechahora_string.replace("'", "")
    try:
        parsed_date = datetime.strptime(fechahora_string, "%d-%m-%Y %H:%M:%S")
    
    except ValueError:
        return None
    
    return parsed_date.date()
            


def formateo_establecimiento(string_establecimiento):
        
    try:    
        if 'esta' in string_establecimiento.lower():
            return Establecimiento.objects.get(establecimiento='EST')
        elif 'craw' in string_establecimiento.lower():
            return Establecimiento.objects.get(establecimiento='JC')
        elif 'carr' in string_establecimiento.lower():
            return Establecimiento.objects.get(establecimiento='HC')
        elif 'baqu' in string_establecimiento.lower():
            return Establecimiento.objects.get(establecimiento='BAQ')
    except:
        print("Establecimiento no válido")
    
def formateo_fono(fono):
    print("fono___________________", fono)
    if pd.isna(fono) : #si no hay número (Not A Number)
        return "Sin Número"
 
    elif isinstance(fono, float):
        return int(fono)
    
def formateo_funcionario(funcionario):
    funcionario = funcionario[5:14].rstrip() #solo el rut, si el rut es menor que 10 millones, le quita el espacio.
    funcionario = Usuario.objects.get(rut=funcionario)
    return funcionario

    

  

def ingreso(archivo):
    informe_formularios_headers = pd.read_excel(archivo, nrows=0, header=16) #dataframe con solo los headers
    riesgos = []
    headers_fecha_prox_control = []
    for header in informe_formularios_headers:
        if ('0 A 5' in header) and ('RIESGO' in header):
            riesgos.append(header)
        elif ('6 A 9' in header) and ('RIESGO' in header):
            riesgos.append(header)
        elif ('10 A 19' in header) and ('RIESGO' in header):
            riesgos.append(header)
        elif ('0' in header) and ('5' in header) and ('FECHA' in header):
            headers_fecha_prox_control.append(header)
        elif ('6' in header) and ('9' in header) and ('FECHA' in header):
            headers_fecha_prox_control.append(header)
        elif ('10' in header) and ('19' in header) and ('FECHA' in header):
            headers_fecha_prox_control.append(header)
    
   
    
    
    print('riesgos::::::::::::::::::::', riesgos)
    columnas = ['ESTABLECIMIENTO',
                'RUT', 
                'DV', 
                'PACIENTE', 
                'FECHA DE NACIMIENTO', 
                'SEXO', 
                'TELEFONO 1', 
                'TELEFONO 2', 
                'FECHA FORMULARIO', 
                'FUNCIONARIOS FORMULARIO', 
                '53.- ESTADO',
                'FUNCIONARIOS FORMULARIO',
                'FECHA FORMULARIO'
                ]
    columnas.extend(riesgos)
    columnas.extend(headers_fecha_prox_control)

    informe_formularios_df = pd.read_excel(archivo, header=16, usecols=columnas)
    for index, fila in informe_formularios_df.iterrows():
        rut_sin_dv=fila['RUT'],
        dv =fila['DV'],
        nombre = fila['PACIENTE'],
        fecha_nac = string_a_fecha(fila['FECHA DE NACIMIENTO']), #string a formato datefield
        sexo = fila['SEXO'],
        fono_1 = formateo_fono(fila['TELEFONO 1']),
        fono_2 = formateo_fono(fila['TELEFONO 2']),
        establecimiento = formateo_establecimiento(fila['ESTABLECIMIENTO']), #segun choices
        usuario = formateo_funcionario(fila['FUNCIONARIOS FORMULARIO'])
        fecha_formulario = string_a_fecha(fila['FECHA FORMULARIO'])
        riesgo_0_a_5 = fila[riesgos[0]]
        riesgo_6_a_9 = fila[riesgos[1]]
        riesgo_10_a_19 = fila[riesgos[2]]
        
        if not pd.isna(riesgo_0_a_5):
            riesgo = riesgo_0_a_5
        elif not pd.isna(riesgo_6_a_9):
            riesgo = riesgo_6_a_9
        elif not pd.isna(riesgo_10_a_19):
            riesgo = riesgo_10_a_19
            
        if 'alto' in riesgo.lower():
            riesgo = 'ALTO'
        elif 'bajo' in riesgo.lower():
            riesgo = 'BAJO'
        """
                for riesgo in riesgos:
            print("riesgo:", riesgo)
            if not pd.isna(fila[riesgo]):
                print("fila-riesgo", fila[riesgo])
                if 'alto' in fila[riesgo].lower():
                    riesgo = 'ALTO'
                elif 'bajo' in fila[riesgo].lower():
                    riesgo = 'BAJO'
                else:
                    pass
            
        """    
        estado_control = fila['53.- ESTADO']
        if pd.isna(estado_control):
            estado_control = ''
        elif estado_control.startswith('Pri'):
            estado_control = 'PRI'
        elif estado_control.startswith('Ing'):
            estado_control = 'ING'
            
            
            
        for fecha in headers_fecha_prox_control:
            if pd.isna(fila[fecha]):
                pass
            else:
                
                datetime_prox_control = string_a_fecha_hora(fila[fecha])
                
            
        
            

        if not fila['RUT']:
            print(f"Paciente {fila['PACIENTE']} no tiene rut, no será agregado a la base de datos")
            pass
        
            
        elif not Paciente.objects.filter(rut_sin_dv=fila['RUT']): #si el paciente no existe, se agrega
            instancia_paciente = Paciente(rut_sin_dv=fila['RUT'],
                                      dv = dv,
                                      nombre = nombre,
                                      fecha_nac = fecha_nac, #string a formato datefield
                                      sexo = sexo,
                                      fono_1 = fono_1,
                                      fono_2 = fono_2,
                                      establecimiento = establecimiento, #segun choices
                                      )
            instancia_paciente.save()
            pass
            
            

        elif Paciente.objects.filter(rut_sin_dv=fila['RUT']):
            instancia_paciente = Paciente.objects.get(rut_sin_dv = fila['RUT'])#si ya está, hay que actualizar
            instancia_paciente.establecimiento = formateo_establecimiento(fila['ESTABLECIMIENTO'])
            if not pd.isna(fila['TELEFONO 1']):
                instancia_paciente.fono_1 = fila['TELEFONO 1']
            if not pd.isna(fila['TELEFONO 2']):
                instancia_paciente.fono_2 = fila['TELEFONO 2']
          
            instancia_paciente.save()
            pass
        print("usuario para formulario", usuario)
        
        """
        if Usuario.objects.filter(usuario=formateo_funcionario(fila['FUNCIONARIOS FORMULARIO'])):
            instancia_formulario = Usuario.objects.get(usuario=formateo_funcionario(fila['FUNCIONARIOS FORMULARIO']))
        """
        
        instancia_formulario = InformeFormularios(usuario=formateo_funcionario(fila['FUNCIONARIOS FORMULARIO']),
                                                  paciente=Paciente.objects.get(rut_sin_dv=fila['RUT']),
                                                  fecha_formulario = fecha_formulario,
                                                  riesgo = riesgo,
                                                  estado_control = estado_control,
                                                  datetime_prox_control = datetime_prox_control
                                                  )
        print("instancia formulario----------", instancia_formulario)
    
        instancia_formulario.save()
    """
    
    return False
    usuario = models.OneToOneField(Usuario, on_delete=models.DO_NOTHING, null = False)
    paciente = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING, null=False)
    fecha_formulario = models.DateField()
    riesgo_choices = [('ALTO', 'Riesgo Alto'),('BAJO', 'Riesgo Bajo')]
    riesgo = models.CharField(max_length=4, choices=riesgo_choices, null=True)
    estado_control_choices = [('ING', 'Ingreso'), ('PRI', 'Primer Control del Año')]
    estado_control = models.CharField(max_length=3, choices=estado_control_choices, null=True)
    datetime_prox_control = models.DateTimeField()
    """
    return True
"""

class Validar(): 
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.archivo_df = pd.read_excel(nombre_archivo, nrows=16) #guardar dataframe del excel, sólo hasta la línea 16 para hacer las validaciones
        self.si = '✅'
        self.no = '❌'
        #self.contexto = {}
    
    try:
        def xlsx(self):
    
            if self.nombre_archivo.endswith(".xlsx"):
                return self.si
            else:
                return self.no
        
        def comuna(self):
            comuna = 'Vallenar'
            if comuna in str(self.archivo_df.iat[2, 1]):
                return self.si
            else:
                return self.no
       
"""


#websockets enviar mail

#revisar utf encoding

#jasonwebtocken
#tockerizar forms logins y archivos web tocken del response

#aws lambda crear funciones como endpoint validacion de archivos en la nuve

#pip black Formatter autopip
