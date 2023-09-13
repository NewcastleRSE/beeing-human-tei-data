<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="3.0" xpath-default-namespace="http://www.tei-c.org/ns/1.0">
    <!-- Copy anything as it is -->
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*" />
        </xsl:copy>
    </xsl:template>

    <xsl:template match="front//note[@type='authorial' and @subtype='gloss']">
        <xsl:copy>
            <xsl:apply-templates select="@*" />

            <xsl:variable name="count">
                <xsl:number level="any"
                    count="front//note[@type='authorial' and @subtype='gloss']"
                    from="front" />
            </xsl:variable>

            <xsl:attribute name="xml:id">
                <xsl:value-of
                    select="concat('front', 'glon', $count)" />
            </xsl:attribute>

            <xsl:apply-templates select="node()" />
        </xsl:copy>
    </xsl:template>

    <xsl:template match="body//note[@type='authorial' and @subtype='gloss']">
        <xsl:copy>
            <xsl:apply-templates select="@*" />

            <xsl:variable name="count">
                <xsl:number level="any"
                    count="div[@type='chapter']//note[@type='authorial' and @subtype='gloss']"
                    from="div[@type='chapter']" />
            </xsl:variable>

            <xsl:attribute name="xml:id">
                <xsl:value-of
                    select="concat('ch', ancestor::div[@type='chapter']/@n, 'glon', $count)" />
            </xsl:attribute>

            <xsl:apply-templates select="node()" />
        </xsl:copy>
    </xsl:template>

    <!-- Matches notes for subsections in ch10 -->
    <xsl:template match="div[@type='section']//note[@type='authorial' and @subtype='gloss']">
        <xsl:copy>
            <xsl:apply-templates select="@*" />

            <xsl:variable name="count">
                <xsl:number level="any"
                    count="div[@type='section']//note[@type='authorial' and @subtype='gloss']"
                    from="div[@type='section']" />
            </xsl:variable>

            <xsl:attribute name="xml:id">
                <xsl:value-of
                    select="concat('ch', ancestor::div[@type='chapter']/@n, 'p', ancestor::div[@type='section']/@n, 'glon', $count)" />
            </xsl:attribute>

            <xsl:apply-templates select="node()" />
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>