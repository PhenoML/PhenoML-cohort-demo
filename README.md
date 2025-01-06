# PhenoML Cohort Demo

Create cohorts with natural language! Integrate into your Medplum FHIR server with a Bot to power natural language care management and patient identification workflows. Use with BigQuery to supercharge your health outcomes analyses. 

This repository demonstrates how to use PhenoML's experimental cohort API to create and analyze patient cohorts using natural language descriptions. This experimental feature is a workflow built on our PhenoML Construe API, one of our PhenoML [solutions](https://www.phenoml.com/solutions) which uses LLMs to extract medical codes from natural language input. 

:warning: This is an experimental feature, subject to change, and not intended for production use. 

## :sunglasses: What's Included

### 1. Medplum Bot (`cohort_bot.ts`)
A bot that creates FHIR Group resources from natural language cohort descriptions:
- Takes natural language input (e.g., "patients over 40 with hyperlipidemia")
- Uses PhenoML experimental cohort API to generate FHIR queries
- Creates a Group containing matching patients

### 2. BigQuery Analysis (`cohort_demo_nb.ipynb`)
A Jupyter notebook demonstrating cohort analysis:
- Creates cohorts using natural language
- Queries BigQuery's public Synthea FHIR dataset as an example with configuration for your own FHIR dataset
- Analyzes demographics, conditions, and medications

## :computer: Getting Started

### Prerequisites
- PhenoML API credentials. Sign up for your trial credentials [here](https://forms.gle/LgEEsDfNym7XfWqK6)
- This API includes usage of UMLS systems: RxNorm and SNOMED. Please review notices and terms below. 

### BigQuery
- Access to BigQuery. Using Vertex AI Workbench notebook instance is helpful but not required. 
- Python packages: google-cloud-bigquery, pandas, requests (these are already installed in the notebook instance if you're using Vertex AI Workbench)
- Familiarity with analyzing FHIR data in SQL and/or Python is helpful. Check out [Analyzing Synthea FHIR Dataset with BigQuery](https://cloud.google.com/architecture/analyzing-fhir-data-in-bigquery) for more information.

### Medplum
- Familiarity with Medplum's FHIR API and bots. Check out [Medplum Bot Docs](https://www.medplum.com/docs/bots) for more information.

### API Documentation
- If you'd like to try out the cohort API directly, take a look at the [API Documentation](COHORT_API.md)

## :rocket: What kinds of cohorts can I create?
The Patient, Condition, and MedicationRequest FHIR resources are currently supported so you can create cohorts based on inclusion and exclusion criteria with multiple resources. SNOMED codes are used for the Condition resource and RxNorm codes are used for the MedicationRequest resource. We use vector embeddings search for the codes, so there's no code hallucinations here! Latency increases the more complex of a cohort you describe; ~4-7 seconds for simple cohorts and up to 20 seconds for complex cohorts. 

Below are some examples:
- Over 18 years old with strep throat
- Between 30 and 40 years old with type 2 diabetes
- Over 55 with NSCLC
- Over 40 and male with hyperlipidemia and not prescribed statins
- Over 60 and female with osteoporosis and prescribed bisphosphonates

## :sparkles: Coming Soon!
- Support for Observation, Procedure, and other FHIR resources
- Use custom coding systems and value sets. Instead of using SNOMED or RxNorm, you can upload your own coding system and value sets to let the API use them for cohort creation. 
- More complex cohort queries such as: 
    - "Over 65 and haven't received their flu shot this year"
    - "Received corticosteroids prior to hip fracture"
- Support for conversational cohort and health outcomes analyses 

## :tv: Demo
Check out a video demo on our youtube channel: [PhenoML Cohort Demo](https://youtu.be/__6CvAIvwPw)

## :speech_balloon: Support, Feedback and Contact
We'd love to hear your feedback and suggestions! Please reach out to us at [hello@phenoml.com](mailto:hello@phenoml.com)

For hands on support and questions, join our [Discord](https://discord.gg/XNVNzk6EaA)

## :information_source: UMLS
This experimental API includes usage of the following UMLS systems: SNOMED and RXNORM. Your usage is subject to the following notices and terms.

Bodenreider O. The Unified Medical Language System (UMLS): integrating biomedical terminology. Nucleic Acids Res. 2004 Jan 1;32(Database issue):D267-70. doi: 10.1093/nar/gkh061. PubMed PMID: 14681409; PubMed Central PMCID: PMC308795. 

### SNOMED
This API includes usage of SNOMED Clinical Terms® (SNOMED CT®), used by permission of the International Health Terminology Standards Development Organisation (IHTSDO). All rights reserved. SNOMED CT®, was originally created by The College of American Pathologists. "SNOMED" and "SNOMED CT" are registered trademarks of the IHTSDO. Acccess to this API is currently only available to those in a territory  represented by a member of The International Health Terminology Standards Development Organization. Please review the SNOMED license [SNOMED CT® Affiliate License Agreement](https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/license_agreement_snomed.html)

### RXNORM
This experimental API uses publicly available data courtesy of the U.S. National Library of Medicine (NLM), National Institutes of Health, Department of Health and Human Services; Nelson SJ, Zeng K, Kilbourne J, Powell T, Moore R. Normalized names for clinical drugs: RxNorm at 6 years. J Am Med Inform Assoc. 2011 Jul-Aug;18(4)441-8. doi: 10.1136/amiajnl-2011-000116. Epub 2011 Apr 21. PubMed PMID: 21515544; PubMed Central PMCID: PMC3128404. Courtesy of the U.S. National Library of Medicine.
