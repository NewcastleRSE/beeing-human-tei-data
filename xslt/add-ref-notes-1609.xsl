<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="3.0" xpath-default-namespace="http://www.tei-c.org/ns/1.0">
    
    <!-- Identity transform -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="note[@subtype='bibliographic' and not(.//bibl) and not(.//ref)]">
        <xsl:copy>
            <xsl:apply-templates select="@*" />
            <ref>
                <xsl:attribute name="target">#</xsl:attribute>
                <xsl:apply-templates select="node()" />
            </ref>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>