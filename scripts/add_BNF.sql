/* 
   add_BNF.sql is a MySQL script intended to add Bibliotheque nationale de France
   as another "Other Sites" option. 

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2011 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url) VALUES (26,'Bibliotheque nationale de France','http://catalogue.bnf.fr/servlet/RechercheEquation?rq.schisme=B&rq.clef.0=pertinence&rq.autre=oui&rq.termes.0=%s&Equation=MOT&TexteTypeDoc=DESNFPIBTMCJOV&rq.sens.0=croissant&categorieRecherche=RechercheMotsNotices&rq.relation.0=&rq.valeurs.1=LM&rq.operateur.0=&rq.valeurs.0=ABCDEGHIJKLMNOPQRSTUVWXYZ1&rq.filtre.1=FiltreConditionCommunication&rq.filtre.0=FiltreSousCatalogue&rq.page=1&TexteCollection=HGARSTUVWXYZ1DIECBMJNQLOKP&rq.critere.0=NoticeB&rq.recherche=Combinee&categorieRecherche=RechercheMotsNotices&rq.page=1&rq.recherche=Combinee&rq.schisme=B&rq.professionnelle=0&rq.operateur.0=&rq.critere.0=NoticeB&rq.relation.0=&rq.filtre.0=FiltreSousCatalogue&rq.valeurs.0=ABCDEGHIJKLMNOPQRSTUVWXYZ1&rq.filtre.1=FiltreConditionCommunication&rq.valeurs.1=LM&rq.clef.0=pertinence&rq.sens.0=croissant&host=catalogue');

