###### -*- coding: utf-8 -*-


__author__  = 'UNIS - ENS de Lyon <vutheany.loch@ens-lyon.fr>'
__docformat__ = 'plaintext'

from Products.CMFCore.permissions import setDefaultRoles
from Products.Archetypes.public import DisplayList

############################################
### Default Things for XML FILE
LOM_ROOT_HEADER = \
"""
<lom:lom xmlns:lomfr="http://www.lom-fr.fr/xsd/LOMFR" xmlns:lom="http://ltsc.ieee.org/xsd/LOM"
    xmlns:lomfrens="http://pratic.ens-lyon.fr/xsd/LOMFRENS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd http://pratic.ens-lyon.fr/xsd/lomfrensv1.0/lomfrens.xsd">
"""

LOM_ROOT_FIN = \
"""
</lom:lom>
"""

LANGUES =  DisplayList((
    ('fre', 'French'),
    ('eng', 'English'),
	('ger', 'Deutch'),
	('spa', 'Spanish'),
	('ita', 'Italian'),
	('ara', 'Arabic'),
    ))
#DOCUMENTS_TYPES_9 ne s'utilise pas
DOCUMENTS_TYPES_9=DisplayList((
            ('collection','collection'), 
            ('ensemble de données', 'ensemble de données'),
            ('événement', 'événement'),
            ('image', 'image'),
            ('image fixe','image fixe'),
            ('image en mouvement','image en mouvement'),
            ('logiciel', 'logiciel'),
            ('objet physique', 'objet physique'),
            ('ressource interactive','ressource interactive'),
            ('service','service'),
            ('son', 'son'),
            ('texte', 'texte'),
            ))
DOCUMENTS_TYPES=DisplayList((
            ('géolocalisation-ensemble de données', 'Géolocalisation'),
            ('None-événement', 'Evénement'),
            ('image-image fixe', 'Image'),
            ('vidéo-image en mouvement','Vidéo'),
            ('son-son', 'son'),
            ('texte-texte', 'texte'),
            ('téléchargement-None', 'Téléchargement'),
            ('lienVersUnAutreSite-None', 'Lien vers un autre site'),
            ('imageDeLaSemaine-None', 'Image de la semaine'),
            ))           
DOCUMENTS_PEDAS=DisplayList((
            ('article-lom:lecture','Article'), 
            ('conférence-lom:lecture', 'Conférence'),
            ('exercice-lom:exercise', 'Exercice'),
            ('expérience-lom:experiment', 'Expérience'),
            ('simulation-lom:simulation','Simulation'),
            ('None-lomfr:scénario pédagogique','Scénario pédagogique'),
            ('None-lomfr:tutoriel', 'tutoriel'),
            ('dossier-None', 'Dossier'),
            ('question-None','Question du mois'),
            ('imageDeLaSemaine-None','Image de la semaine'),
            ('entretien-None', 'Entretien'),
            ))
            
FORMATS_RESSOURCE =  DisplayList((
    ('text/html', 'text/html'),
    ('text/xml', 'text/xml'),
    ('application/vdn-rn-realmedia', 'application/vdn-rn-realmedia'),
    ('application/pdf', 'application/pdf'),
    ('application/x-shockwave-flash', 'application/x-shockwave-flash'),
    ('image/jpeg', 'image/jpeg'),
    ))

PUBLIC_CIBLE =  DisplayList((
    ('learner', 'learner'),
    ('teacher', 'teacher'),
    ('author', 'author'),
    ('manager', 'manager'),
    ))
NIVEAUX =  DisplayList((
    ('enseignement primaire-school', 'Enseignement primaire'),
    ('enseignement secondaire-school', 'Enseignement secondaire'),
    ('licence-higher education', 'Licence'),
    ('master-higher education', 'Master'),
    ('doctorat-higher education', 'Doctorat'),
    ('formation continue-training', 'Formation continue'),
    ))

PROJECTNAME = 'enslyon.FicheIndexation'

ADD_PERMISSIONS = {
    'ficheIndexation': 'enslyon.FicheIndexation: Add ficheIndexation',
}
