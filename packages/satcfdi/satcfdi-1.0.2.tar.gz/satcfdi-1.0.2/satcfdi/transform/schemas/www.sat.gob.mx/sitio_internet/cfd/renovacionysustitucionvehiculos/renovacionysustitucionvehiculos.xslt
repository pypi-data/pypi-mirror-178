<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:decreto="http://www.sat.gob.mx/renovacionysustitucionvehiculos" version="2.0"><xsl:template match="decreto:renovacionysustitucionvehiculos"><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Version"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@TipoDeDecreto"/></xsl:call-template><xsl:apply-templates select="./decreto:DecretoRenovVehicular"/><xsl:apply-templates select="./decreto:DecretoSustitVehicular"/></xsl:template><xsl:template match="decreto:DecretoRenovVehicular"><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@VehEnaj"/></xsl:call-template><xsl:for-each select="./decreto:VehiculosUsadosEnajenadoPermAlFab"><xsl:apply-templates select="."/></xsl:for-each><xsl:apply-templates select="./decreto:VehiculoNuvoSemEnajenadoFabAlPerm"/></xsl:template><xsl:template match="decreto:DecretoSustitVehicular"><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@VehEnaj"/></xsl:call-template><xsl:apply-templates select="./decreto:VehiculoUsadoEnajenadoPermAlFab"/><xsl:apply-templates select="./decreto:VehiculoNuvoSemEnajenadoFabAlPerm"/></xsl:template><xsl:template match="decreto:VehiculosUsadosEnajenadoPermAlFab"><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@PrecioVehUsado"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@TipoVeh"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Marca"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@TipooClase"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Año"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@Modelo"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@NIV"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@NumSerie"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@NumPlacas"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@NumMotor"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@NumFolTarjCir"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@NumPedIm"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@Aduana"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@FechaRegulVeh"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Foliofiscal"/></xsl:call-template></xsl:template><xsl:template match="decreto:VehiculoNuvoSemEnajenadoFabAlPerm"><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Año"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@Modelo"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@NumPlacas"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@RFC"/></xsl:call-template></xsl:template><xsl:template match="decreto:VehiculoUsadoEnajenadoPermAlFab"><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@PrecioVehUsado"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@TipoVeh"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Marca"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@TipooClase"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Año"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@Modelo"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@NIV"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@NumSerie"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@NumPlacas"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@NumMotor"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@NumFolTarjCir"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@NumFolAvisoint"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@NumPedIm"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Aduana"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@FechaRegulVeh"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Foliofiscal"/></xsl:call-template></xsl:template></xsl:stylesheet>