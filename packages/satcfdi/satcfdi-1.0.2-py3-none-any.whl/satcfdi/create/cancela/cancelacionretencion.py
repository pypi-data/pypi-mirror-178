from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence

from ..w3.signature import signature_c14n_sha1
from ... import Signer
from ...cfdi import CFDI, XElement


class Folio(XElement):
    """
    http://www.sat.gob.mx/esquemas/retencionpago/1
    Folio fiscal (UUID) a ser cancelado.
    """
    def __init__(
            self,
            uuid: str,
            motivo: str,
            folio_sustitucion: str = None,
    ): 
        """
        Folio fiscal (UUID) a ser cancelado.
        
        :param uuid: UUID generado en la operación de timbrado del comprobante solicitado.
        :param motivo: Clave del motivo de cancelación del comprobante.
        :param folio_sustitucion: Atributo condicional que representa al UUID que sustituye al folio fiscal cancelado. Es requerido cuando la clave del motivo de cancelación es 01.
        """
        
        super().__init__({
            'UUID': uuid,
            'Motivo': motivo,
            'FolioSustitucion': folio_sustitucion,
        })
        

class Cancelacion(XElement):
    """
    Elemento raíz para realizar una solicitud de cancelación de CFDI.
    """
    tag = '{http://www.sat.gob.mx/esquemas/retencionpago/1}Cancelacion'

    def __init__(
            self,
            emisor: Signer,
            folios: Folio | Sequence[Folio | dict],
            fecha: datetime = None
    ):
        """
        Elemento raíz para realizar una solicitud de cancelación de CFDI.

        :param emisor: Atributo requerido para expresar el RFC del emisor del (os) CFDI a cancelar.
        :param fecha: Atributo requerido para expresar la fecha de la operación.
        :param folios: Colección de folios fiscales (UUID) a ser cancelados.
        """
        super().__init__({
            'RfcEmisor': emisor.rfc,
            'Fecha': fecha or datetime.now(),
            'Folios': folios,
        })
        self["_nsmap"] = {
            None: "http://www.sat.gob.mx/esquemas/retencionpago/1",
            "xsd": "http://www.w3.org/2001/XMLSchema",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }

        sig = signature_c14n_sha1(
            signer=emisor,
            element=self.to_xml(),
            nsmap={
                None: 'http://www.w3.org/2000/09/xmldsig#',
                "xsd": "http://www.w3.org/2001/XMLSchema",
                "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            }
        )
        self['Signature'] = sig

