# ISO/ISO/TC211 Code Sets

This repository contains the point-of-truth source data of the [International Standards Organization](https://www.iso.org)'s [Technical Committee 211 (Geographic information/Geomatics)](https://committee.iso.org/home/tc211)'s code sets. Code sets are controlled lists of identified terms used in standards.

Code set content here is stored here in [RDF](https://www.w3.org/TR/rdf12-concepts/) data files in the [Turtle format](https://www.w3.org/TR/rdf12-turtle/) as [Semantic Web](https://en.wikipedia.org/wiki/Semantic_Web) vocabularies according to the [Vocabulary Publication Profile of SKOS](https://linked.data.gov.au/def/vocpub/spec), with SKOS being the [SKOS Simple Knowledge Organization System](https://www.w3.org/TR/skos-reference/) model. 

The code sets are published online at [IRI](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) persistent identifier locations resolved via the [Open Geospatial Consortium's "Rainbow" reference data publication system](https://defs.opengis.net) at:

* *<https://def.isotc211.org/codesets>*

## Governance

The code sets here will be maintained via procedures aligning with [ISO 19135:2026 Geographic information — Procedures for item registration](https://www.iso.org/standard/87753.html) with the ISO/TC211's [Advisory Group 6 Group for Ontology Maintenance (GOM)](https://committee.iso.org/sites/tc211/home/about/advisory-groups.html) acting as the _Control Body_ organising expert reviews of proposed content changes from _Content Authorities_ - standards editors and content maintainers.

Content Authorities will not be select by GOM but assigned via ISO/TC211 processes, yet to be determined throughout 2026.

### Who can propose changes?

Until the ISO/TC211 May 2027 plenary meeting, changes to code sets will only be accepted from Content Authorities as ISO/TC211 moved to the first comprehensive and authoritative publication of code sets. From May 2026, Content Authorities may allow changes to code sets to be proposed by others - trusted editors, general public etc.: to be determined by the Content Authorities.

### Changes procedure

Change procedures will follow [ISO 19135:2026 Geographic information — Procedures for item registration](https://www.iso.org/standard/87753.html) with automation built into GitHub Actions-based workflows. Due to this, the best form of change request that can be made is a Pull Requests on this repository made at <https://github.com/iso-TC211/codesets/pulls>.

Pull Requests will result in a review workflow, coordinated by the Control Body and assigned to Content Authorities.

If you cannot make a Pull Request, please raise an Issue indicating the change requested at <https://github.com/iso-TC211/codesets/issues>. Sensible issues will be converted into Pull Requests by GOM.

If you cannot raise an Issue, please contact GOM or the Content Authority of your target code set. GOM can be contacted via the details below.

### Change annotations

All changes to code sets - either the code sets as a whole or individual concepts within them - will be annotated on the code set or concept with the Submitter and approving Content Authority indicated as well as the date of the change. 

An example of a fictitious addition of 'chatbot' to the [19115 On Line Function Code](https://def.isotc211.org/codeset/OnLineFunctionCode) is:

```turtle
:chatbot
    a skos:Concept ;
    rdfs:isDefinedBy cs: ;
    skos:definition "Artificial Intelligence chat bot for asking questions about the resource"@en ;    
    skos:inScheme cs: ;
    skos:prefLabel "chatbot"@en ;
    skos:topConceptOf cs: ;
    ls:hasLifecycleStage [
        time:hasBeginning [ time:inXSDDate "2026-01-12"^^xsd:date ] ;
        time:hasEnd [ time:inXSDDate "2026-02-28"^^xsd:date ] ;
        schema:additionalType status:submitted ;
        prov:qualifiedAttribution [
            prov:agent <http://example.com/org/x> ;  # Organisation X
            prov:role role:submitter ;
        ] ;
        skos:scopeNote "Concept added"
    ] ,
    [
        time:hasBeginning [ time:inXSDDate "2026-02-28"^^xsd:date ] ;
        time:hasEnd [ time:inXSDDate "2026-03-04"^^xsd:date ] ;
        schema:additionalType status:accepted ;
        prov:qualifiedAttribution [
            prov:agent <http://example.com/org/iso19115-editors> ; 
            prov:role role:contentAuthority ;
        ] ;
    ] ,
    [
        time:hasBeginning [ time:inXSDDate "2026-03-04"^^xsd:date ] ;
        # no end time - current
        schema:additionalType status:stable ;
        prov:qualifiedAttribution [
            prov:agent <https://def.isotc211.org/org/ag6> ;  # GOM 
            prov:role role:contentAuthority ;
        ] ;
    ] ;
.
```

Here the addition was 'submitted' in January 2026 by Organisation X, 'accepted' in February by ISO 19115 Editors and techncially implemented in March by GOM.

> [!NOTE]
> The organisations and roles used in this example are indicative of real things but fictitious. Roles and identifiers for groups will be finalised by May 2026.

## Publication Status

### Code Set coverage

Not all the Code Sets within ISO/TC211's 19* series of standards are yet delivered here. Those that are, are published at <https://def.isotc211.org/codesets> with the remainder to be delivered by May 2026. Until that time, Content Authorities are being contacted to assist with delivery of all ISO/TC211 code sets.

## Content Structure

The RDF resources in this repository within the `resources/` folder that constitute the catalogue of code sets are organised according to a structured manifest allowing for automated validation and absorption by the OGC Rainbow system. The following table of resources is auto-generated by the [PrezManifest](https://github.com/Kurrawong/prezmanifest) tool from the `manifest.ttl` file:

| Resource                                                    | Role                                                                                                                | Description                                                                     |
|-------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Catalogue Definition:<br />[`catalogue.ttl`](catalogue.ttl) | [Catalogue Data](https://prez.dev/ManifestResourceRoles/CatalogueData)                                              | The definition of, and metadata for, the code sets container object - catalogue |
| Resource Data:<br />[`codesets/*.ttl`](codesets/*.ttl)      | [Resource Data](https://prez.dev/ManifestResourceRoles/ResourceData)                                                | Code sets as catalogued resources                                               |
| Labels Files:<br />[`background/*.ttl`](background/*.ttl)   | [Complete Catalogue and Resource Labels](https://prez.dev/ManifestResourceRoles/CompleteCatalogueAndResourceLabels) | Labels for resource data elements and reference data such as Agents             |

## License & Use

These vocabularies are available for reuse under the conditions of the [Creative Commons BY 4.0 License](https://creativecommons.org/licenses/by/4.0/), a copy of the deed of which is contained in this repository in the LICENSE file.

These vocabularies and the software in this repository is copyright as follows:

&copy; International Organization for Standardization, 2026

## Contact

These code sets are managed by the ISO/TC211's [Advisory Group 6 Group for Ontology Maintenance (GOM)](https://committee.iso.org/sites/tc211/home/about/advisory-groups.html). Please contact that group using the details at:

* <https://github.com/ISO-TC211/GOM#contact>

> [!NOTE]  
> Contact points for individual code sets are not yet available but are planned to become so when code set maintenance is completely implemented, expected in late 2025.
