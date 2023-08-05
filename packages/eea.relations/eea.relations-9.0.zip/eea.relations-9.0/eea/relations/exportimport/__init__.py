""" GenericSetup export/import XML adapters
"""
import os
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody

def importRelationsTool(context):
    """Import settings."""
    logger = context.getLogger('eea.relations')

    body = context.readDataFile('possible_relations.xml')
    if body is None:
        logger.info("Nothing to import")
        return

    site = context.getSite()
    tool = getToolByName(site, 'portal_relations', None)
    if not tool:
        logger.info('portal_relations tool missing')
        return

    importer = queryMultiAdapter((tool, context), IBody)
    if importer is None:
        logger.warning("Import adapter missing.")
        return

    # set filename on importer so that syntax errors can be reported properly
    subdir = getattr(context, '_profile_path', '')
    importer.filename = os.path.join(subdir, 'possible_relations.xml')

    importer.body = body
    logger.info("Imported.")

def exportRelationsTool(context):
    """Export settings."""
    logger = context.getLogger('eea.relations')
    site = context.getSite()
    tool = getToolByName(site, 'portal_relations')

    if tool is None:
        logger.info("Nothing to export")
        return

    exporter = queryMultiAdapter((tool, context), IBody)
    if exporter is None:
        logger.warning("Export adapter missing.")
        return

    context.writeDataFile('possible_relations.xml',
                          exporter.body, exporter.mime_type)
    logger.info("Exported.")
