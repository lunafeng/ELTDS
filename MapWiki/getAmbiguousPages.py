#!/usr/bin/python
import wikipedia
from SPARQLWrapper import SPARQLWrapper, JSON

def queryDbpedia(title):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	query = ("""
		PREFIX  dbo:  <http://dbpedia.org/ontology/>
		PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

		SELECT DISTINCT  ?o
		WHERE
		  {   { <http://dbpedia.org/resource/%s>
				  dbo:wikiPageDisambiguates  ?o
		      }
		    UNION
		      { <http://dbpedia.org/resource/%s>
				  dbo:wikiPageRedirects  ?r .
			?r        dbo:wikiPageDisambiguates  ?o
		      }
		    UNION
		      { <http://dbpedia.org/resource/%s_(disambiguation)>
				  dbo:wikiPageDisambiguates  ?o
		      }
		    UNION
		      { <http://dbpedia.org/resource/%s_(disambiguation)>
				  dbo:wikiPageRedirects  ?r .
			?r        dbo:wikiPageDisambiguates  ?o
		      }
		  }
	""")
	sparql.setQuery(query % (title, title, title, title))
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	results = results["results"]["bindings"]
	documents = []
	for result in results:
		url = result["o"]["value"]
		if url not in documents and "_(disambiguation)" not in url:
			title = url.split("http://dbpedia.org/resource/")[1]
			documents.append(str(title))
	return documents

def main(title):
		documents = []
		try:
			result = wikipedia.summary(title.title())
		except wikipedia.exceptions.DisambiguationError as e:
			r = title.title().replace(" ","_")
			documents.append(r)
			result = e.options
			for r in result:
				if "disambiguation" not in r and "All articles starting with" not in r and "All pages beginning with" not in r and "List of" not in r and "Category:" not in r:
					r = r.replace(" ", "_")
					try:
						documents.append(str(r))
					except:
						pass
		except:
			pass
		try:
			result = wikipedia.summary(title.title() + " (disambiguation)")
		except wikipedia.exceptions.DisambiguationError as e:
			result = e.options
			r = title.title().replace(" ","_")
			documents.append(r)
			for r in result:
				if "disambiguation" not in r and "All articles starting with" not in r and "All pages beginning with" not in r and "List of" not in r and "Category:" not in r:
					r = r.replace(" ", "_")
					try:
						documents.append(str(r))
					except:
						pass
		except:
			pass
		title = title.replace(" ","_")
		documentsAll = list(set(documents))
		if len(documentsAll) == 0:
			documentsAll = list(set(queryDbpedia(title.title()) + documents))
		return documentsAll


