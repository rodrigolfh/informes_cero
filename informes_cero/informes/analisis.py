import pandas as pd
from datetime import date
import msoffcrypto
import io
from .models import Paciente, Usuario, InformeFormularios, Establecimiento
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist #para usar el doesnotexist como excepcion con try-except
from dateutil.relativedelta import relativedelta




# LISTO: CORROBORAR QUE EL ARCHIVO SEA XLSX (doble, antes de subir en el view y después de subir en la función 'xslx')
# LISTO: Corroborar comuna

# LISTO  QUE TENGA EL NOMBRE DE UN CESFAM DE LA LISTA (PEDIRLE A CRISTIAN OTRAS PLANILLAS)

# LISTO: FECHA HASTA - DESDE = UN AÑO, CORROBORA QUE SEA UN INFORME DE UN AÑO Y UN MES CORRIDO 

# LISTO: FORMULARIO: QUE TENGA '(CER0)'
# LISTO: TODOS LOS METACAMPOS = tRUE, SITUACIÓN= TODOS, ESTADO: AMBOS EDAD INICIAL=0, FINAL MAYR A 20, SEXO AMBOS
# LISTO: CORROBORAR QUE ESTÉ CADA COLUMNA


# cambiar símbolos.


archivo = './archivos/Informe_Formularios_RAYEN_4.xlsx'


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
    try:
        funcionario_objeto = Usuario.objects.get(rut=funcionario)
        return funcionario_objeto
    
    except ObjectDoesNotExist:
        nuevo_user = User(username=funcionario)
        nuevo_user.save()
        nuevo_usuario = Usuario(user=nuevo_user, rut=funcionario, nombre=funcionario)
        nuevo_usuario.save()
        funcionario_nuevo = nuevo_usuario
        return funcionario_nuevo

    

  

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
        rut_sin_dv=int(fila['RUT']),
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
        instancia_paciente = ''
        completo = True
        
        
        
        
        if not pd.isna(riesgo_0_a_5):
            riesgo = riesgo_0_a_5
        elif not pd.isna(riesgo_6_a_9):
            riesgo = riesgo_6_a_9
        elif not pd.isna(riesgo_10_a_19):
            riesgo = riesgo_10_a_19
        else:
            completo = False
            
        if 'alto' in riesgo.lower():
            riesgo = 'ALTO'
        elif 'bajo' in riesgo.lower():
            riesgo = 'BAJO'
            
        else:
            completo = False   
        
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
        else:
            completo = False
            
            
            
        for fecha in headers_fecha_prox_control:
            if pd.isna(fila[fecha]):
                completo = False
            else:
                
                fecha_prox_control = string_a_fecha_hora(fila[fecha])
                
            
        
            

        if not fila['RUT']:
            print(f"Paciente {fila['PACIENTE']} no tiene rut, no será agregado a la base de datos")
            pass
        
        ###########3 inventar un rut y agregarlo
        
            
        elif not Paciente.objects.filter(rut_sin_dv=fila['RUT']): #si el paciente no existe, se agrega
            instancia_paciente = Paciente(rut_sin_dv=fila['RUT'],
                                      dv = dv,
                                      nombre = nombre,
                                      fecha_nac = fecha_nac, #string a formato datefield
                                      sexo = sexo,
                                      fono_1 = fono_1,
                                      fono_2 = fono_2,
                                      establecimiento = establecimiento[0], #segun choices
                                      )
            instancia_paciente.save()
            pass
            
            

        elif Paciente.objects.filter(rut_sin_dv=fila['RUT']):
            instancia_paciente = Paciente.objects.get(rut_sin_dv = fila['RUT'])#si ya está, hay que actualizar
            instancia_paciente.establecimiento = establecimiento[0] #por algun motivo la fx devuelve una tupla con 1 elemento
            if not pd.isna(fono_1):
                instancia_paciente.fono_1 = fono_1
            if not pd.isna(fono_2):
                instancia_paciente.fono_2 = fono_1
          
            instancia_paciente.save()
            pass
        print("usuario para formulario", usuario)
     
     
      # si no hay un formulario asociado al paciente, en la misma fecha, SE ESCRIBE.       
        
        if not InformeFormularios.objects.filter(paciente=rut_sin_dv, fecha_formulario=fecha_formulario):
            
            
            
            instancia_formulario = InformeFormularios(usuario=usuario,
                                                  paciente=instancia_paciente,
                                                  fecha_formulario = fecha_formulario,
                                                  riesgo = riesgo,
                                                  estado_control = estado_control,
                                                  fecha_prox_control = fecha_prox_control
                                                  )
            print("instancia formulario----------", instancia_formulario)

            instancia_formulario.save()
    
    
    return True

### Funciones para actualizar asincrónicamente las fechas de salida del bajo control.

def actualizar_fecha_prox_control_instancia(instancia):
    if instancia.fecha_sale != "Faltan datos":
   
        instancia.prox_control_segun_riesgo = instancia.fecha_sale
       
    else:
        instancia.completo = False
        
        

def actualizar_fecha_sale(instancia):

    fecha_form = instancia.fecha_formulario
    fecha_nacimiento = instancia.paciente.fecha_nac
    
        # Calcular la diferencia entre las fechas
       
    try:
        
        edad_form = fecha_form - fecha_nacimiento
        
        edad_años = edad_form.days // 365
        print("edad_años", edad_años)

        if edad_años < 3:
            if instancia.riesgo == 'BAJO':
                fecha_sale = instancia.fecha_formulario + relativedelta(months=12)
      
            elif instancia.riesgo == 'ALTO':
                fecha_sale = instancia.fecha_formulario + relativedelta(months=6)
               
        elif edad_años >= 3:
            if instancia.riesgo == 'BAJO':
                fecha_sale = instancia.fecha_formulario + relativedelta(months=12)
                
            elif instancia.riesgo == 'ALTO':
                fecha_sale = instancia.fecha_formulario + relativedelta(months=4)
                
        instancia.fecha_sale = fecha_sale
        
        if fecha_sale >= datetime.now().date():
            instancia.vigente = True
        
        else:
            instancia.vigente = False
              
        
         
    except TypeError:
        instancia.fecha_sale = instancia.fecha_prox_control
       
    

def actualizar_tiempo_restante_real(instancia):
    hoy = datetime.now().date()
    try:
            
        tiempo_restante = instancia.fecha_sale - hoy

        
    
    except TypeError:
       
        instancia.fecha_sale = instancia.prox_control_segun_riesgo
        tiempo_restante = instancia.fecha_sale - hoy
        
    
    instancia.tiempo_restante_real = int(tiempo_restante.days)
        
def eliminar_mayores_de_9(instancia):
    try:
        if instancia.edad_años > 9:
            instancia.delete()
            print("instancia borrada")
        
    except TypeError:
        pass    



        
    
def actualizar_db():
    instancias = InformeFormularios.objects.all()
    for instancia in instancias:
        actualizar_fecha_prox_control_instancia(instancia)
        actualizar_fecha_sale(instancia)
        actualizar_tiempo_restante_real(instancia)
        
        instancia.save()
        eliminar_mayores_de_9(instancia)
        

      
        
       
    