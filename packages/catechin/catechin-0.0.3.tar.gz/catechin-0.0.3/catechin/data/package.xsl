<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:strip-space elements="*"/>

  <!-- identity transform -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="/package">
    <xsl:copy>
      <xsl:apply-templates select="node()[not(contains(name(), '_depend'))]
                                   | buildtool_depend[1]
                                   | buildtool_export_depend[1]
                                   | build_depend[1]
                                   | run_depend[1]
                                   | exec_depend[1]
                                   | test_depend[1]
                                   | doc_depend[1]
                                   | conflict[1]
                                   | replace[1]" />
    </xsl:copy>
  </xsl:template>

  <xsl:template match="*[contains(name(), '_depend')]">
    <xsl:for-each select="../*[name()=name(current())]" >
      <xsl:sort/>
      <xsl:copy-of select="." />
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>
