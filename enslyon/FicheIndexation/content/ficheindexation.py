# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from ZPublisher.HTTPRequest import HTTPRequest
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from ComputedAttribute import ComputedAttribute

from Products.GenericSetup.interfaces import IDAVAware

from zope.formlib import form
from plone.fieldsets.fieldsets import FormFieldsets
from zope.schema import List
from zope.i18nmessageid import MessageFactory
from Products.Archetypes import atapi
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import TextField
from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import LinesWidget
from Products.Archetypes.atapi import KeywordWidget
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import BooleanWidget
from Products.Archetypes.atapi import SelectionWidget, MultiSelectionWidget
from Products.Archetypes.atapi import RFC822Marshaller
from Products.Archetypes.atapi import AnnotationStorage

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.ATExtensions.ateapi import FormattableNamesField
from Products.ATExtensions.ateapi import FormattableNamesWidget

from Products.Archetypes.utils import contentDispositionHeader

from enslyon.FicheIndexation.interfaces import IficheIndexation
from enslyon.FicheIndexation.config import PROJECTNAME
from enslyon.FicheIndexation.config import LANGUES, DOCUMENTS_TYPES, FORMATS_RESSOURCE, DOCUMENTS_PEDAS, PUBLIC_CIBLE, NIVEAUX

#from Products.ATContentTypes import ATCTMessageFactory as _
from Products.CMFPlone import PloneMessageFactory as _
_ = MessageFactory('enslyon.FicheIndexation')


from Products.Archetypes.public import *
from Products.Archetypes.utils import contentDispositionHeader
from DateTime import DateTime
import xml

ficheIndexationSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

   #langues pour @langauge
    StringField('lomLangue',
              vocabulary = LANGUES,
              default = _(u'fre'),
              widget = atapi.SelectionWidget(label = _(u'Langues')),
             ),
    #With Lom: or not
#    BooleanField('withLom',
#              languageIndependent = True,
#              default = True,
#              widget = atapi.BooleanWidget(label = _(u"'lom:' dans les balises ?")),
#                        description=_(u"Pour avoir ou pas 'lom:' dans toutes les balises."),
#             ),
             
     #Pour la partie <lom:general>
        #Pour la partie <lom:identifier>
#    StringField('genIdenCatalog',
#                required=False,
#                searchable=True,
#                default = _(u'URI'),
#                write_permission = ModifyPortalContent,
#                widget = StringWidget(
#                        description = _(u"help_genIdenCatalog",
#                                        default=u"Exemple : URI, ENS-Lyon DGESCO Physique, etc. "),
#                        label = _(u'label_genIdenCatalog', default=u'Catalogue')
#                        )),              
    StringField('genIdenEntry',
                required=True,
                searchable=True,
                write_permission = ModifyPortalContent,
                widget = StringWidget(
                        maxlength=500,
                        size=100,
                        description = _(u'help_genIdenEntry',
                                        default=u"Resource URL. Example :"
                                        "http://acces.inrp.fr/acces/terre/paleo/variations/paleoclimats/accueil.htm."),
                        label = _(u'label_genIdenEntry', default=u'Resource address')
                        )),
                        
        #Pour la partie <lom:title>
#    StringField('genTitle',
#                required=True,
#                searchable=True,
#                write_permission = ModifyPortalContent,
#                widget = StringWidget(
#                        description = _(u'help_genTitle',
#                                        default=u'Le titre de la ressource. Note: Celui-ci est different de celui en #haut qui est le nom de cette fiche et qui pourra #etre plus court que le vrai titre de la ressource.'),
#                        label = _(u'label_genIdenEntry', default=u'Titre de la ressource')
#                        )),
         #Pour la partie <lom:description>
    TextField('genDescription',
         required=False,
         searchable=True,
         storage = AnnotationStorage(migrate=True),
         widget=TextAreaWidget(
             rows = 3,
             label = _(u'label_genDescription', default=u'Description'),
             description=_(u"help_genDescription", default=u"Resource summary."),
         ),
     ),
    
        #Pour la partie <lom:keyword>
    LinesField('genKeywords',
               languageIndependent=True,
               searchable=True,
               write_permission=ModifyPortalContent,
               widget=LinesWidget(
                      description = _(u'help_genKeywords',
                                        default=u"Type a key word line bye line."),
                      label=_(u'label_genKeywords', default=u'Key word(s)')
                      )),
                      
      #Pour la partie<lomfr:documentType>
    LinesField('genDocumentType',
               languageIndependent=True,
               required=True,
               searchable=True,
               default ='texte-texte',
               write_permission=ModifyPortalContent,
               vocabulary=DOCUMENTS_TYPES,
               widget=MultiSelectionWidget(
                      description = _(u'help_genDocumentType',
                                        default=u"Tick one or more Document/Media type(s)."),
                      label=_(u'label_genDocumentType', default=u'Document/Media types'),
                      format='checkbox',
                      )),
          #Pour la partie<lomfr:documentType>
    LinesField('documentTypePeda',
               languageIndependent=True,
               required=True,
               searchable=True,
               default ='article-lom:lecture',
               write_permission=ModifyPortalContent,
               vocabulary=DOCUMENTS_PEDAS,
               widget=MultiSelectionWidget(
                      description = _(u'help_DocumentTypePeda',
                                        default=u"Tick one or more Teaching type(s)."),
                      label=_(u'label_DocumentTypePeda', default=u'Teaching type(s).'),
                      format='checkbox',
                      )),
                      
                      
      #Pour les formats de la ressources lom:technical
#    LinesField('techFormat',
#               languageIndependent=True,
#               required=False,
#               searchable=False,
#               write_permission=ModifyPortalContent,
#               vocabulary=FORMATS_RESSOURCE,
#               widget=MultiSelectionWidget(
#                      description = _(u'help_techFormat',
#                                        default=u"Selectionner un ou des format(s) de la ressource."),
#                      label=_(u'label_techFormat', default=u'Type(s) de document'),
#                      format='select',
#                      )),
    
    #Pour la partie <lom:lifeCycle>
    DateTimeField('ResourcePublishedDate',
        searchable = 1,
        required = 0,
        default_method = 'getToday',
        widget = CalendarWidget(
            label=_(u'label_ResourcePublishedDate', default=u'Date de publication de ressource.'), 
			format="%Y-%m-%d",
			show_hm=0,
			description = _(u'help_ResourcePublishedDate', default=u"Indiquer ici la date de publication de la ressource"),
        ),
    ),
    FormattableNamesField('authors',
        searchable = 1,
        required = 1,
        minimalSize = 1,
        subfields=('firstnames','lastname', 'organisme'),
        subfield_sizes={'firstnames':50, 'lastname':50, 'organisme':50},
        subfield_labels={'username':'Auteurs'},
        subfield_maxlength={'organisme': 500,},
        is_duplicates_criterion=True,
        widget=FormattableNamesWidget(label="Authors",
            label_msgid="label_authors",
            macro_edit = "authors_widget",
            helper_js = ('authors_widget.js',),	
            description="Type the informations about author(s) line by line follwing the structure below for the organisations : Organisation1;Organisation2;Organisation3",
            description_msgid="help_authors",
        ) ,
    ),

    FormattableNamesField('contributeurs',
        searchable = 1,
        required = 1,
        minimalSize = 1,
        subfields=('firstnames','lastname', 'organisme'),
        subfield_sizes={'firstnames':50, 'lastname':50, 'organisme':50},
        subfield_labels={'username':'Auteurs'},
        subfield_maxlength={'organisme': 500,},
        is_duplicates_criterion=True,
        widget=FormattableNamesWidget(label="Contributors",
            label_msgid="label_contributeurs",
            macro_edit = "authors_widget",
            helper_js = ('authors_widget.js',),	
            description="Type the informations about contributor(s) line by line follwing the structure below for the organisations : Organisation1;Organisation2;Organisation3",
            description_msgid="help_contributors",
        ) ,
    ),
#    LinesField('cycleEditeur',
#               languageIndependent=True,
#               required=True,
#               searchable=False,
#               default='ENS Lyon|Université de Lyon;ENS Lyon|2012-10-15',
#               write_permission=ModifyPortalContent,
#               widget=LinesWidget(
#                      description = _(u'help_cycleEditeur',
#                                        default=u"Type the informations about publisher(s) line by line follwing the structure #below : Name|Organisation(s) separated by ';'|AAAA-MM-JJ."),
#                      label=_(u'label_cycleEditeur', default=u'Publisher'),
#                      rows=1,
#                      )), 
     
                      
#    LinesField('metaValidateur',
#               languageIndependent=True,
#               required=False,
#               searchable=False,
#               write_permission=ModifyPortalContent,
#               widget=LinesWidget(
#                      description = _(u'help_metaValidateur',
#                                        default=u"Saisir les informations concernant le validateur en respectant la structure : Prénom Nom|Organisme(s) séparé par #';'|AAAA-MM-JJ. Exemple : Axel Pfalzgraf|Université de Lyon; ENS Lyon; UNIS|2010-11-02."),
#                      label=_(u'label_metaValidateur', default=u'Validateur - lom:lom > lom:metaMetadata > lom:contribute > lom:role > lom:value = validator'),
#                      rows=1,
#                      )),                       
#    LinesField('public',
#               languageIndependent=True,
#               required=True,
#               searchable=False,
#               write_permission=ModifyPortalContent,
#               vocabulary=PUBLIC_CIBLE,
#               default =('learner', 'teacher'),
#               widget=MultiSelectionWidget(
#                      description = _(u'help_public',
#                                        default=u"Sélectionner le public cible."),
#                      label=_(u'label_public', default=u'Public cible - lom:lom > lom:educational > lom:intendedEndUserRole'),
#                      format='select',
#                      )),
#   LinesField('niveaux',
#               languageIndependent=True,
#               required=True,
#               searchable=False,
#               write_permission=ModifyPortalContent,
#               vocabulary=NIVEAUX,
#               widget=MultiSelectionWidget(
#                      description = _(u'help_niveaux',
#                                        default=u"Sélectionner le(s) niveau(x)."),
#                      label=_(u'label_niveaux', default=u'Niveaux'),
#                      format='select',
#                      )),
    #Pour la partie <lomfrens:ensData>
    
    #Pour la partie <lom:classification>
    TextField('classifications',
         required=False,
         searchable=True,
         default_output_type = 'text/xml',
         storage = AnnotationStorage(migrate=True),
         widget=TextAreaWidget(
             rows = 5,
             label = _(u'label_classifications', default=u'Lom:classification'),
             description=_(u"help_classifications", default=u"Paste here Classification TAG from genClass : http://unis.ens-lyon.fr/activites/indexation/taxonomies/select_taxons"),
         ),
     ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ficheIndexationSchema['title'].storage = atapi.AnnotationStorage()
#ficheIndexationSchema['description'].storage = atapi.AnnotationStorage()
del ficheIndexationSchema['description']
schemata.finalizeATCTSchema(ficheIndexationSchema, moveDiscussion=False)


class ficheIndexation(base.ATCTContent, HistoryAwareMixin):
    """Fiche Indexation Content Type"""
    implements(IficheIndexation, IDAVAware)

    meta_type = "ficheIndexation"
    schema = ficheIndexationSchema
    portal_type    = 'ficheIndexation'
    archetype_name = 'Fiche Indexation'
    _atct_newTypeFor = {'portal_type' : 'CMF ficheIndexation', 'meta_type' : 'ficheIndexation'}
    assocMimetypes = ('application/xhtml+xml', 'message/rfc822', 'text/xml' 'text/*',)
    assocFileExt   = ('txt', 'xml','stx', 'rst', 'rest', 'py',)
    title = atapi.ATFieldProperty('title')
    #description = atapi.ATFieldProperty('description')
	
    def getToday(self):
        now = DateTime()
        today = now.strftime("%Y-%m-%d")
        return today
	
    def toLocalizedTime(self, time, long_format=None, time_only = None):
        """Convert time to localized time
        """
        util = getToolByName(self, 'translation_service')
        return util.ulocalized_time(time, long_format, time_only, self,
                                    domain='plonelocales')
    def contentXML(self):
        langue=self['lomLangue']
        #langue='fre'
        #Gestion des types de documents (médias)
        if self['ResourcePublishedDate']:
            datePubRessource=self['ResourcePublishedDate'].strftime("%Y-%m-%d")
        else:
            datePubRessource=self.getToday()
        typesMedias = self['genDocumentType']
        droitAuteur=self.aq_parent.Rights()
        publisher=self.aq_parent.Description()
        orgEdit="ORG:"+publisher.split("ORG:")[-1]
        typesMediasENS=[]
        typesMediasLomfr=[]
        for typeMedia in typesMedias:
            typeMediaENS=typeMedia.split('-')[0]
            typeMediaLomfr=typeMedia.split('-')[1]
            typesMediasENS.append(typeMediaENS)
            
            if typeMediaLomfr!='None':
                typesMediasLomfr.append(typeMediaLomfr)
        
        #Gestion des types pédagogiques
        typesPeda=self['documentTypePeda']
        typesPedaENS=[]
        typesPedaLomfr=[]
        typesPedaLom=[]
        lecture=0
        for typePeda in typesPeda:
            typePedaENS=typePeda.split('-')[0]
            typePedaAutre=typePeda.split('-')[1]
            
            if typePedaENS !='None':
                typesPedaENS.append(typePedaENS)
            if typePedaAutre.find('lomfr:')!=-1:
                typePedaLomfr=str(typePedaAutre).replace('lomfr:', '')
                typesPedaLomfr.append(typePedaLomfr)
            else:
                if typePedaAutre.find('lom:')!=-1:
                    typePedaLom=str(typePedaAutre).replace('lom:', '')
                    if typePedaLom=='lecture' and lecture==0:
                        typesPedaLom.append(typePedaLom)
                        lecture=lecture + 1
                    else:
                        typesPedaLom.append(typePedaLom)
        
        typesEnsData=typesMediasENS+typesPedaENS
        if 'article' in typesEnsData and 'texte' in typesEnsData:
            typesEnsData.remove('texte')
        
        #Gestion des niveaux
        #niveauxList=self['niveaux']
        niveauxList=('higher education-higher education')
        niveauxLom=['higher education']
        niveauxLomfr=['formation continue']
        
        creatorId=getToolByName(self, 'portal_membership').getMemberById(self.Creator())
        if creatorId is None:
            creatorName=creatorId			
        else:
            creatorName=creatorId.getProperty("fullname")
        prenomCreator=str(creatorName).split(" ")[-1]
        nomCreator=str(creatorName).replace(" "+prenomCreator, "")
        
        DateTimeDeCreation=self.CreationDate()
        #pubDate = str(self.toLocalizedTime(self.Date())).replace('/', '-')
        pubDate = str(str(self.Date()).split('T')[0]).replace('/', '-')
        #DateDeCreation=str(self.toLocalizedTime(DateTimeDeCreation)).replace('/', '-')
        DateDeCreation=str(str(DateTimeDeCreation).split('T')[0]).replace('/', '-')
        
        xml_content="""<?xml version="1.0" encoding="utf-8"?>  
<lom:lom xmlns:lomfr="http://www.lom-fr.fr/xsd/LOMFR" xmlns:lom="http://ltsc.ieee.org/xsd/LOM"
        xmlns:lomfrens="http://pratic.ens-lyon.fr/xsd/LOMFRENS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd http://pratic.ens-lyon.fr/xsd/lomfrensv1.0/lomfrens.xsd">
    <lom:general>
        <lom:identifier>
            <lom:catalog>%s</lom:catalog>
            <lom:entry>%s</lom:entry>
        </lom:identifier>
        <lom:title>
            <lom:string language="%s">%s</lom:string>
        </lom:title>
        <lom:language>%s</lom:language>
        <lom:description>
            <lom:string language="%s">%s</lom:string>
        </lom:description>""" % ('URI', self['genIdenEntry'], langue, self['title'], langue, langue, self['genDescription'])
        keywords = self['genKeywords']
        if len(keywords) > 0:
            for word in keywords:
                xml_content += """
        <lom:keyword>
            <lom:string language="%s">%s</lom:string>
        </lom:keyword>""" % (langue, word)
        xml_content += """
        <lom:structure>
            <lom:source>LOMv1.0</lom:source>
            <lom:value>atomic</lom:value>
        </lom:structure>
        <lom:aggregationLevel>
            <lom:source>LOMv1.0</lom:source>
            <lom:value>1</lom:value>
        </lom:aggregationLevel>"""
        
        #documentTypes=self['genDocumentType']
        for type in typesMediasLomfr:
            xml_content += """
        <lomfr:documentType>
            <lomfr:source>LOMFRv1.0</lomfr:source>
            <lomfr:value>%s</lomfr:value>
        </lomfr:documentType>""" % type
        
        xml_content += """
    </lom:general>
    <lom:lifeCycle>
        <lom:version>
            <lom:string language="fre">1</lom:string>
        </lom:version>
        <lom:status>
            <lom:source>LOMv1.0</lom:source>
            <lom:value>final</lom:value>
        </lom:status>"""
        
        auteurs=self['authors']
        for auteur in auteurs:
            nom=auteur['lastname']
            prenom=auteur['firstname']
            fullname=auteur
            org=auteur['organisme']
            xml_content += """
        <lom:contribute>
            <lom:role>
                <lom:source>LOMv1.0</lom:source>
                <lom:value>author</lom:value>
            </lom:role>
            <lom:entity>BEGIN:VCARD
                VERSION:3.0 
                N:%s;%s;;; 
                FN:%s
                ORG:%s;
                END:VCARD
            </lom:entity>
            <lom:date>
                <lom:dateTime>%s</lom:dateTime>
            </lom:date>
        </lom:contribute> """ % (nom, prenom, fullname, org, datePubRessource)
        
        #editeurs=self['cycleEditeur']
        #for editeur in editeurs:
        #    editeurInfo=editeur.split("|")
        #    if editeurInfo[1]=='':
        #       orgEdit=';'
        #    elif editeurInfo[1].find(';')==-1:
        #       orgEdit=editeurInfo[1]+';'
        #    else:
        #       orgEdit=editeurInfo[1]
        #    NomPrenom=editeurInfo[0].split(" ")
            xml_content += """
        <lom:contribute>
            <lom:role>
                <lom:source>LOMv1.0</lom:source>
                <lom:value>publisher</lom:value>
            </lom:role>
            <lom:entity>BEGIN:VCARD 
                VERSION:3.0 
                N:;;;; 
                %s
                END:VCARD
            </lom:entity>
            <lom:date>
                <lom:dateTime>%s</lom:dateTime>
            </lom:date>
        </lom:contribute> """ % (publisher.strip(), datePubRessource)
        contributeurs=self['contributeurs']
        for c in contributeurs:
            nomC=c['lastname']
            prenomC=c['firstname']
            fullnameC=c
            orgC=c['organisme']
            xml_content += """
        <lom:contribute>
            <lom:role>
                <lom:source>LOMFRv1.0</lom:source>
                <lom:value>contributeur</lom:value>
            </lom:role>
            <lom:entity>BEGIN:VCARD 
                VERSION:3.0 
                N:%s;%s;;; 
                FN:%s
                ORG:%s;
                END:VCARD
            </lom:entity>
            <lom:date>
                <lom:dateTime>%s</lom:dateTime>
            </lom:date>
        </lom:contribute> """ % (nomC, prenomC, fullnameC, orgC, datePubRessource)
        xml_content += """
    </lom:lifeCycle>
    <lom:metaMetadata>
        <lom:contribute>
            <lom:role>
                <lom:source>LOMv1.0</lom:source>
                <lom:value>creator</lom:value>
            </lom:role>
            <lom:entity>BEGIN:VCARD 
                 VERSION:3.0
                 N:%s;%s;;; 
                 FN:%s %s
                 %s
                 END:VCARD
            </lom:entity>
            <lom:date>
                <lom:dateTime>%s</lom:dateTime>
            </lom:date>
        </lom:contribute>""" % (nomCreator, prenomCreator, prenomCreator, nomCreator, orgEdit, DateDeCreation)
        #validateurs=self['metaValidateur']
        #if len(validateurs)>0:
        #    for validateur in validateurs:
        #        validateurInfo=validateur.split("|")
        #        NomPrenom=validateurInfo[0].split(" ")
        xml_content += """
        <lom:contribute>
            <lom:role>
                <lom:source>LOMv1.0</lom:source>
                <lom:value>validator</lom:value>
            </lom:role>
            <lom:entity>BEGIN:VCARD 
                 VERSION:3.0
                 N:Pfalzgraf;Axel;;;
                 FN:Axel Pfalzgraf
                 %s
                 END:VCARD
            </lom:entity>
            <lom:date>
                <lom:dateTime>%s</lom:dateTime>
            </lom:date>
        </lom:contribute>""" % (orgEdit, pubDate)
#        % (NomPrenom[1], NomPrenom[0], validateurInfo[0], validateurInfo[1], validateurInfo[2],)
        xml_content += """
        <lom:metadataSchema>LOMv1.0</lom:metadataSchema>
        <lom:metadataSchema>LOMFRv1.0</lom:metadataSchema>
        <lom:metadataSchema>SupLOMFRv1.0</lom:metadataSchema>
        <lom:language>%s</lom:language>
    </lom:metaMetadata>
    <lom:technical>""" % 'fre'
        
        #formats=self['techFormat']
        formats=('text/html',)
        if len(formats)>0:
            for format in formats:
                xml_content +="""
            <lom:format>%s</lom:format> """ % format
        xml_content +="""
            <lom:location>%s</lom:location>
    </lom:technical>
    <lom:educational> """ % self['genIdenEntry']
        for learningResourceType in typesPedaLom:
            xml_content +="""
        <lom:learningResourceType>
            <lom:source>LOMv1.0</lom:source>
            <lom:value>%s</lom:value>
        </lom:learningResourceType> """ % learningResourceType
        
        publicCible=['teacher']
        for typePublic in publicCible:
            xml_content +="""
        <lom:intendedEndUserRole>
            <lom:source>LOMv1.0</lom:source>
            <lom:value>%s</lom:value>
        </lom:intendedEndUserRole> """ % typePublic
        
        for levelLom in niveauxLom:
            xml_content +="""
        <lom:context>
            <lom:source>LOMv1.0</lom:source>
            <lom:value>%s</lom:value>
        </lom:context> """ % levelLom
        
        for levelLomfr in niveauxLomfr:
            xml_content +="""
        <lom:context>
            <lom:source>LOMFRv1.0</lom:source>
            <lom:value>%s</lom:value>
        </lom:context> """ % levelLomfr    
        xml_content +="""
        <lom:language>%s</lom:language>
    </lom:educational>
    <lom:rights>
        <lom:cost>
            <lom:source>LOMv1.0</lom:source>
            <lom:value>no</lom:value>
        </lom:cost>
        <lom:copyrightAndOtherRestrictions>
            <lom:source>LOMv1.0</lom:source>
            <lom:value>yes</lom:value>
        </lom:copyrightAndOtherRestrictions>
        <lom:description>
            <lom:string language="%s">%s</lom:string>
        </lom:description>
    </lom:rights>""" % (langue, langue, droitAuteur)
        if len(typesEnsData) > 0 :
            xml_content+="""
    <lomfrens:ensData> """
            for typeEnsData in typesEnsData:
                xml_content+="""
        <lomfrens:ensDocumentType>
            <lomfrens:source>LOMFRENSv1.0</lomfrens:source>
            <lomfrens:value>%s</lomfrens:value>
        </lomfrens:ensDocumentType> """ % typeEnsData
        xml_content += """
    </lomfrens:ensData>
    %s
</lom:lom> """ % (self['classifications'])

        #if self['withLom']==False:
        #    return xml_content.replace('lom:', '')
        #else:
        #    return xml_content
         
        return xml_content
    
    def download(self, REQUEST=None, RESPONSE=None):
        """Download the saved data as xml
        """

        filename = self.id
        if filename.find('.') < 0:
            filename = 'LOM-%s.xml' % filename
            
        header_value = contentDispositionHeader('attachment', self.getCharset(), filename=filename)
        RESPONSE.setHeader("Content-Disposition", header_value)
        RESPONSE.setHeader("Content-Type", 'application/xml;charset=%s' % self.getCharset())
        xml_content=self.contentXML()
            
        return '%s' % xml_content

atapi.registerType(ficheIndexation, PROJECTNAME)
