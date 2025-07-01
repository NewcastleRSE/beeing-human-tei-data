<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="3.0" xpath-default-namespace="http://www.tei-c.org/ns/1.0">
    
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*" />
        </xsl:copy>
    </xsl:template>
      
    <xsl:template match="//note">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:attribute name="type">authorial</xsl:attribute>
            <xsl:attribute name="subtype">summary</xsl:attribute>
            <xsl:apply-templates select="node()"/>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>