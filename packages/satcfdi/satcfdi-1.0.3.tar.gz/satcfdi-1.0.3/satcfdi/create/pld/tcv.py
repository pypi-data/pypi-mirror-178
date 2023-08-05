from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence
from ...cfdi import CFDI, XElement


class FideicomisoDestinatarioType(XElement):
    def __init__(
            self,
            denominacion_razon: str,
            rfc: str = None,
            identificador_fideicomiso: str = None,
    ): 
        """
        
        :param denominacion_razon: 
        :param rfc: 
        :param identificador_fideicomiso: 
        """
        
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'Rfc': rfc,
            'IdentificadorFideicomiso': identificador_fideicomiso,
        })
        

class PersonaMoralDestinatarioType(XElement):
    def __init__(
            self,
            denominacion_razon: str,
            fecha_constitucion: date = None,
            rfc: str = None,
    ): 
        """
        
        :param denominacion_razon: 
        :param fecha_constitucion: 
        :param rfc: 
        """
        
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
        })
        

class PersonaFisicaDestinatarioType(XElement):
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
    ): 
        """
        
        :param nombre: 
        :param apellido_paterno: 
        :param apellido_materno: 
        :param fecha_nacimiento: 
        :param rfc: 
        :param curp: 
        """
        
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
        })
        

class TipoPersonaDestinatarioType(XElement):
    def __init__(
            self,
            persona_fisica: PersonaFisicaDestinatarioType | dict = None,
            persona_moral: PersonaMoralDestinatarioType | dict = None,
            fideicomiso: FideicomisoDestinatarioType | dict = None,
    ): 
        """
        
        :param persona_fisica: 
        :param persona_moral: 
        :param fideicomiso: 
        """
        
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class DestinatarioType(XElement):
    def __init__(
            self,
            destinatario_persona_aviso: str,
            tipo_persona: TipoPersonaDestinatarioType | dict = None,
    ): 
        """
        
        :param destinatario_persona_aviso: 
        :param tipo_persona: 
        """
        
        super().__init__({
            'DestinatarioPersonaAviso': destinatario_persona_aviso,
            'TipoPersona': tipo_persona,
        })
        

class ExtranjeroEntregaType(XElement):
    def __init__(
            self,
            pais: str,
            estado_provincia: str,
            ciudad_poblacion: str,
            codigo_postal: str,
    ): 
        """
        
        :param pais: 
        :param estado_provincia: 
        :param ciudad_poblacion: 
        :param codigo_postal: 
        """
        
        super().__init__({
            'Pais': pais,
            'EstadoProvincia': estado_provincia,
            'CiudadPoblacion': ciudad_poblacion,
            'CodigoPostal': codigo_postal,
        })
        

class NacionalEntregaType(XElement):
    def __init__(
            self,
            codigo_postal: str,
    ): 
        """
        
        :param codigo_postal: 
        """
        
        super().__init__({
            'CodigoPostal': codigo_postal,
        })
        

class TipoEntregaType(XElement):
    def __init__(
            self,
            nacional: NacionalEntregaType | dict = None,
            extranjero: ExtranjeroEntregaType | dict = None,
    ): 
        """
        
        :param nacional: 
        :param extranjero: 
        """
        
        super().__init__({
            'Nacional': nacional,
            'Extranjero': extranjero,
        })
        

class EntregaType(XElement):
    def __init__(
            self,
            fecha_entrega: date,
            tipo_entrega: TipoEntregaType | dict,
    ): 
        """
        
        :param fecha_entrega: 
        :param tipo_entrega: 
        """
        
        super().__init__({
            'FechaEntrega': fecha_entrega,
            'TipoEntrega': tipo_entrega,
        })
        

class DatosNoSucursalType(XElement):
    def __init__(
            self,
            colonia: str,
            calle: str,
            numero_exterior: str,
            codigo_postal: str,
            numero_interior: str = None,
    ): 
        """
        
        :param colonia: 
        :param calle: 
        :param numero_exterior: 
        :param codigo_postal: 
        :param numero_interior: 
        """
        
        super().__init__({
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'NumeroInterior': numero_interior,
        })
        

class DatosSucursalType(XElement):
    def __init__(
            self,
            codigo_postal: str,
    ): 
        """
        
        :param codigo_postal: 
        """
        
        super().__init__({
            'CodigoPostal': codigo_postal,
        })
        

class TipoCustodiaType(XElement):
    def __init__(
            self,
            datos_sucursal: DatosSucursalType | dict = None,
            datos_no_sucursal: DatosNoSucursalType | dict = None,
    ): 
        """
        
        :param datos_sucursal: 
        :param datos_no_sucursal: 
        """
        
        super().__init__({
            'DatosSucursal': datos_sucursal,
            'DatosNoSucursal': datos_no_sucursal,
        })
        

class CustodiaType(XElement):
    def __init__(
            self,
            fecha_inicio: date,
            fecha_fin: date,
            tipo_custodia: TipoCustodiaType | dict,
    ): 
        """
        
        :param fecha_inicio: 
        :param fecha_fin: 
        :param tipo_custodia: 
        """
        
        super().__init__({
            'FechaInicio': fecha_inicio,
            'FechaFin': fecha_fin,
            'TipoCustodia': tipo_custodia,
        })
        

class RecepcionType(XElement):
    def __init__(
            self,
            tipo_servicio: str,
            fecha_recepcion: date,
            codigo_postal: str,
    ): 
        """
        
        :param tipo_servicio: 
        :param fecha_recepcion: 
        :param codigo_postal: 
        """
        
        super().__init__({
            'TipoServicio': tipo_servicio,
            'FechaRecepcion': fecha_recepcion,
            'CodigoPostal': codigo_postal,
        })
        

class DatosValoresType(XElement):
    def __init__(
            self,
            tipo_valor: str,
            valor_objeto: str,
            descripcion: str,
    ): 
        """
        
        :param tipo_valor: 
        :param valor_objeto: 
        :param descripcion: 
        """
        
        super().__init__({
            'TipoValor': tipo_valor,
            'ValorObjeto': valor_objeto,
            'Descripcion': descripcion,
        })
        

class DatosEfectivoInstrumentosType(XElement):
    def __init__(
            self,
            instrumento_monetario: str,
            moneda: str,
            monto_operacion: str,
    ): 
        """
        
        :param instrumento_monetario: 
        :param moneda: 
        :param monto_operacion: 
        """
        
        super().__init__({
            'InstrumentoMonetario': instrumento_monetario,
            'Moneda': moneda,
            'MontoOperacion': monto_operacion,
        })
        

class TipoBienType(XElement):
    def __init__(
            self,
            datos_efectivo_instrumentos: DatosEfectivoInstrumentosType | dict = None,
            datos_valores: DatosValoresType | dict = None,
    ): 
        """
        
        :param datos_efectivo_instrumentos: 
        :param datos_valores: 
        """
        
        super().__init__({
            'DatosEfectivoInstrumentos': datos_efectivo_instrumentos,
            'DatosValores': datos_valores,
        })
        

class DatosOperacionType(XElement):
    def __init__(
            self,
            fecha_operacion: date,
            tipo_operacion: str,
            tipo_bien: TipoBienType | dict | Sequence[TipoBienType | dict],
            recepcion: RecepcionType | dict = None,
            custodia: CustodiaType | dict = None,
            entrega: EntregaType | dict = None,
            destinatario: DestinatarioType | dict = None,
    ): 
        """
        
        :param fecha_operacion: 
        :param tipo_operacion: 
        :param tipo_bien: 
        :param recepcion: 
        :param custodia: 
        :param entrega: 
        :param destinatario: 
        """
        
        super().__init__({
            'FechaOperacion': fecha_operacion,
            'TipoOperacion': tipo_operacion,
            'TipoBien': tipo_bien,
            'Recepcion': recepcion,
            'Custodia': custodia,
            'Entrega': entrega,
            'Destinatario': destinatario,
        })
        

class DetalleOperacionesType(XElement):
    def __init__(
            self,
            datos_operacion: DatosOperacionType | dict | Sequence[DatosOperacionType | dict],
    ): 
        """
        
        :param datos_operacion: 
        """
        
        super().__init__({
            'DatosOperacion': datos_operacion,
        })
        

class FideicomisoSimpleType(XElement):
    def __init__(
            self,
            denominacion_razon: str,
            rfc: str = None,
            identificador_fideicomiso: str = None,
    ): 
        """
        
        :param denominacion_razon: 
        :param rfc: 
        :param identificador_fideicomiso: 
        """
        
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'Rfc': rfc,
            'IdentificadorFideicomiso': identificador_fideicomiso,
        })
        

class PersonaMoralSimpleType(XElement):
    def __init__(
            self,
            denominacion_razon: str,
            fecha_constitucion: date = None,
            rfc: str = None,
            pais_nacionalidad: str = None,
    ): 
        """
        
        :param denominacion_razon: 
        :param fecha_constitucion: 
        :param rfc: 
        :param pais_nacionalidad: 
        """
        
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
            'PaisNacionalidad': pais_nacionalidad,
        })
        

class PersonaFisicaSimpleType(XElement):
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
            pais_nacionalidad: str = None,
    ): 
        """
        
        :param nombre: 
        :param apellido_paterno: 
        :param apellido_materno: 
        :param fecha_nacimiento: 
        :param rfc: 
        :param curp: 
        :param pais_nacionalidad: 
        """
        
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
            'PaisNacionalidad': pais_nacionalidad,
        })
        

class TipoPersonaSimpleType(XElement):
    def __init__(
            self,
            persona_fisica: PersonaFisicaSimpleType | dict = None,
            persona_moral: PersonaMoralSimpleType | dict = None,
            fideicomiso: FideicomisoSimpleType | dict = None,
    ): 
        """
        
        :param persona_fisica: 
        :param persona_moral: 
        :param fideicomiso: 
        """
        
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class DuenoBeneficiarioType(XElement):
    def __init__(
            self,
            tipo_persona: TipoPersonaSimpleType | dict,
    ): 
        """
        
        :param tipo_persona: 
        """
        
        super().__init__({
            'TipoPersona': tipo_persona,
        })
        

class TelefonoType(XElement):
    def __init__(
            self,
            clave_pais: str = None,
            numero_telefono: str = None,
            correo_electronico: str = None,
    ): 
        """
        
        :param clave_pais: 
        :param numero_telefono: 
        :param correo_electronico: 
        """
        
        super().__init__({
            'ClavePais': clave_pais,
            'NumeroTelefono': numero_telefono,
            'CorreoElectronico': correo_electronico,
        })
        

class ExtranjeroType(XElement):
    def __init__(
            self,
            pais: str,
            estado_provincia: str,
            ciudad_poblacion: str,
            colonia: str,
            calle: str,
            numero_exterior: str,
            codigo_postal: str,
            numero_interior: str = None,
    ): 
        """
        
        :param pais: 
        :param estado_provincia: 
        :param ciudad_poblacion: 
        :param colonia: 
        :param calle: 
        :param numero_exterior: 
        :param codigo_postal: 
        :param numero_interior: 
        """
        
        super().__init__({
            'Pais': pais,
            'EstadoProvincia': estado_provincia,
            'CiudadPoblacion': ciudad_poblacion,
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'NumeroInterior': numero_interior,
        })
        

class NacionalType(XElement):
    def __init__(
            self,
            colonia: str,
            calle: str,
            numero_exterior: str,
            codigo_postal: str,
            numero_interior: str = None,
    ): 
        """
        
        :param colonia: 
        :param calle: 
        :param numero_exterior: 
        :param codigo_postal: 
        :param numero_interior: 
        """
        
        super().__init__({
            'Colonia': colonia,
            'Calle': calle,
            'NumeroExterior': numero_exterior,
            'CodigoPostal': codigo_postal,
            'NumeroInterior': numero_interior,
        })
        

class TipoDomicilioType(XElement):
    def __init__(
            self,
            nacional: NacionalType | dict = None,
            extranjero: ExtranjeroType | dict = None,
    ): 
        """
        
        :param nacional: 
        :param extranjero: 
        """
        
        super().__init__({
            'Nacional': nacional,
            'Extranjero': extranjero,
        })
        

class RepresentanteApoderadoType(XElement):
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
    ): 
        """
        
        :param nombre: 
        :param apellido_paterno: 
        :param apellido_materno: 
        :param fecha_nacimiento: 
        :param rfc: 
        :param curp: 
        """
        
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
        })
        

class FideicomisoType(XElement):
    def __init__(
            self,
            denominacion_razon: str,
            apoderado_delegado: RepresentanteApoderadoType | dict,
            rfc: str = None,
            identificador_fideicomiso: str = None,
    ): 
        """
        
        :param denominacion_razon: 
        :param apoderado_delegado: 
        :param rfc: 
        :param identificador_fideicomiso: 
        """
        
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'ApoderadoDelegado': apoderado_delegado,
            'Rfc': rfc,
            'IdentificadorFideicomiso': identificador_fideicomiso,
        })
        

class PersonaMoralType(XElement):
    def __init__(
            self,
            denominacion_razon: str,
            pais_nacionalidad: str,
            giro_mercantil: str,
            representante_apoderado: RepresentanteApoderadoType | dict,
            fecha_constitucion: date = None,
            rfc: str = None,
    ): 
        """
        
        :param denominacion_razon: 
        :param pais_nacionalidad: 
        :param giro_mercantil: 
        :param representante_apoderado: 
        :param fecha_constitucion: 
        :param rfc: 
        """
        
        super().__init__({
            'DenominacionRazon': denominacion_razon,
            'PaisNacionalidad': pais_nacionalidad,
            'GiroMercantil': giro_mercantil,
            'RepresentanteApoderado': representante_apoderado,
            'FechaConstitucion': fecha_constitucion,
            'Rfc': rfc,
        })
        

class PersonaFisicaType(XElement):
    def __init__(
            self,
            nombre: str,
            apellido_paterno: str,
            apellido_materno: str,
            pais_nacionalidad: str,
            actividad_economica: str,
            fecha_nacimiento: date = None,
            rfc: str = None,
            curp: str = None,
    ): 
        """
        
        :param nombre: 
        :param apellido_paterno: 
        :param apellido_materno: 
        :param pais_nacionalidad: 
        :param actividad_economica: 
        :param fecha_nacimiento: 
        :param rfc: 
        :param curp: 
        """
        
        super().__init__({
            'Nombre': nombre,
            'ApellidoPaterno': apellido_paterno,
            'ApellidoMaterno': apellido_materno,
            'PaisNacionalidad': pais_nacionalidad,
            'ActividadEconomica': actividad_economica,
            'FechaNacimiento': fecha_nacimiento,
            'Rfc': rfc,
            'Curp': curp,
        })
        

class TipoPersonaType(XElement):
    def __init__(
            self,
            persona_fisica: PersonaFisicaType | dict = None,
            persona_moral: PersonaMoralType | dict = None,
            fideicomiso: FideicomisoType | dict = None,
    ): 
        """
        
        :param persona_fisica: 
        :param persona_moral: 
        :param fideicomiso: 
        """
        
        super().__init__({
            'PersonaFisica': persona_fisica,
            'PersonaMoral': persona_moral,
            'Fideicomiso': fideicomiso,
        })
        

class PersonaAvisoType(XElement):
    def __init__(
            self,
            tipo_persona: TipoPersonaType | dict,
            tipo_domicilio: TipoDomicilioType | dict = None,
            telefono: TelefonoType | dict = None,
    ): 
        """
        
        :param tipo_persona: 
        :param tipo_domicilio: 
        :param telefono: 
        """
        
        super().__init__({
            'TipoPersona': tipo_persona,
            'TipoDomicilio': tipo_domicilio,
            'Telefono': telefono,
        })
        

class AlertaType(XElement):
    def __init__(
            self,
            tipo_alerta: str,
            descripcion_alerta: str = None,
    ): 
        """
        
        :param tipo_alerta: 
        :param descripcion_alerta: 
        """
        
        super().__init__({
            'TipoAlerta': tipo_alerta,
            'DescripcionAlerta': descripcion_alerta,
        })
        

class ModificatorioType(XElement):
    def __init__(
            self,
            folio_modificacion: str,
            descripcion_modificacion: str,
    ): 
        """
        
        :param folio_modificacion: 
        :param descripcion_modificacion: 
        """
        
        super().__init__({
            'FolioModificacion': folio_modificacion,
            'DescripcionModificacion': descripcion_modificacion,
        })
        

class AvisoType(XElement):
    def __init__(
            self,
            referencia_aviso: str,
            prioridad: str,
            alerta: AlertaType | dict,
            persona_aviso: PersonaAvisoType | dict | Sequence[PersonaAvisoType | dict],
            detalle_operaciones: DetalleOperacionesType | dict,
            modificatorio: ModificatorioType | dict = None,
            dueno_beneficiario: DuenoBeneficiarioType | dict | Sequence[DuenoBeneficiarioType | dict] = None,
    ): 
        """
        
        :param referencia_aviso: 
        :param prioridad: 
        :param alerta: 
        :param persona_aviso: 
        :param detalle_operaciones: 
        :param modificatorio: 
        :param dueno_beneficiario: 
        """
        
        super().__init__({
            'ReferenciaAviso': referencia_aviso,
            'Prioridad': prioridad,
            'Alerta': alerta,
            'PersonaAviso': persona_aviso,
            'DetalleOperaciones': detalle_operaciones,
            'Modificatorio': modificatorio,
            'DuenoBeneficiario': dueno_beneficiario,
        })
        

class SujetoObligadoType(XElement):
    def __init__(
            self,
            clave_sujeto_obligado: str,
            clave_actividad: str,
            clave_entidad_colegiada: str = None,
            exento: str = None,
    ): 
        """
        
        :param clave_sujeto_obligado: 
        :param clave_actividad: 
        :param clave_entidad_colegiada: 
        :param exento: 
        """
        
        super().__init__({
            'ClaveSujetoObligado': clave_sujeto_obligado,
            'ClaveActividad': clave_actividad,
            'ClaveEntidadColegiada': clave_entidad_colegiada,
            'Exento': exento,
        })
        

class InformeType(XElement):
    def __init__(
            self,
            mes_reportado: str,
            sujeto_obligado: SujetoObligadoType | dict,
            aviso: AvisoType | dict | Sequence[AvisoType | dict] = None,
    ): 
        """
        
        :param mes_reportado: 
        :param sujeto_obligado: 
        :param aviso: 
        """
        
        super().__init__({
            'MesReportado': mes_reportado,
            'SujetoObligado': sujeto_obligado,
            'Aviso': aviso,
        })
        

class ArchivoType(XElement):
    def __init__(
            self,
            informe: InformeType | dict | Sequence[InformeType | dict],
    ): 
        """
        
        :param informe: 
        """
        
        super().__init__({
            'Informe': informe,
        })
        

class Archivo(ArchivoType):
    tag = '{http://www.uif.shcp.gob.mx/recepcion/tcv}archivo'

