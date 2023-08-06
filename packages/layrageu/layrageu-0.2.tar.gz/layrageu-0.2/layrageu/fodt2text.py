#!/usr/bin/python3
# -*- coding:Utf-8 -*-

"""
Layrageu : XSL stylesheet as a module file.
"""

# Variables globales ====================================================#

__author__ = "Etienne Nadji <etnadji@eml.cc>"

FODT_TO_TEXT_XML = """<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink">

<xsl:output omit-xml-declaration="yes" method="text" encoding="UTF-8" />

<xsl:strip-space elements="*" />

<xsl:variable name="emph-style">Emphasis</xsl:variable>
<xsl:variable name="bold-style">Strong_20_Emphasis</xsl:variable>

<xsl:template match="/"><xsl:apply-templates select="/office:document/office:body/office:text" /></xsl:template>

<xsl:template match="text:a"><xsl:apply-templates /></xsl:template>
<xsl:template match="text:line-break">{lb}</xsl:template>

<xsl:template match="text:p"><xsl:apply-templates /><xsl:text>
</xsl:text></xsl:template>

<xsl:template match="text:span">
  <xsl:variable name="format">
    <xsl:choose>
      <xsl:when test="@text:style-name = $bold-style">bold</xsl:when>
      <xsl:when test="@text:style-name = $emph-style">emph</xsl:when>
      <xsl:otherwise>unknown</xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <xsl:choose>
    <xsl:when test="$format = 'bold'">**</xsl:when>
    <xsl:when test="$format = 'emph'">*</xsl:when>
    <xsl:otherwise></xsl:otherwise>
  </xsl:choose>
  <xsl:apply-templates />
  <xsl:choose>
    <xsl:when test="$format = 'bold'">**</xsl:when>
    <xsl:when test="$format = 'emph'">*</xsl:when>
    <xsl:otherwise></xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>"""

# vim:set shiftwidth=4 softtabstop=4:
