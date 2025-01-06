# PhenoML Cohort API Documentation

The PhenoML Cohort API allows you to create patient cohorts using natural language descriptions. The API translates these descriptions into FHIR search queries and optional SQL queries. The API is currently in experimental mode and not intended for production use. The Medplum bot and Python notebook are the recommended way to try out the API. 

## Authentication

### Getting Your API Credentials
1. Sign up for PhenoML API credentials at [our signup form](https://forms.gle/LgEEsDfNym7XfWqK6)
2. Once approved, you'll receive a `clientId` and `clientSecret`

### Generating a Bearer Token
First, generate a bearer token using your credentials:

```bash
curl -X POST https://experiment.pheno.ml/api/collections/users/auth-with-password \
  -H "Content-Type: application/json" \
  -d '{
    "identity": "YOUR_CLIENT_ID",
    "password": "YOUR_CLIENT_SECRET"
  }'
```

The response will include your bearer token with other fields omitted for brevity:
```json
{
  "token": "YOUR_BEARER_TOKEN",

}
```

Then use this token in your API requests:
```bash
Authorization: Bearer YOUR_BEARER_TOKEN
```

Note: Keep your credentials and tokens secure and never share them publicly. If you believe your credentials have been compromised, contact us at hello@phenoml.com for a replacement.

## Basic Usage

### Example Request
```bash
curl -X POST https://experiment.pheno.ml/construe/cohort \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "include_extract_results": false,
      "include_rationale": false,
      "exclude_deceased": true,
      "sql_syntax": "bigquery"
    },
    "text": "between 18 and 80 years old with nsclc"
  }'
```

## Configuration Options

### include_extract_results
- **Default**: `false`
- **Description**: When enabled, includes detailed information about medical codes extracted from the text using the PhenoML Construe API
- **Use case**: Enable this when you want extra visibility into which specific medical codes and descriptions (e.g., SNOMED codes) were matched from your natural language description
- **Response impact**: Adds `codeExtractResults` field to each query in the response. Increases latency.

### include_rationale
- **Default**: `false`
- **Description**: When enabled, includes AI-generated explanations for each query component and code extraction
- **Use case**: Enable this to understand how the API interpreted your natural language description and why specific queries were generated
- **Response impact**: Adds `rationale` field to each query in the response. Increases latency

### exclude_deceased
- **Default**: `true`
- **Description**: Controls whether deceased patients should be excluded from the cohort
- **Use case**: Set to `false` if you want the generated queries to include deceased patients
- **Response impact**: Affects the `deceased` parameter in Patient resource queries

### sql_syntax
- **Default**: `null` (no SQL generated)
- **Description**: Specifies the SQL dialect for query generation
- **Current options**: Only supports "bigquery"
- **Use case**: Enable this when you need a SQL query for your BigQuery FHIR dataset
- **Response impact**: Adds `sql` field to the response with a BigQuery-compatible SQL query

## Response Examples

### Full Response (All Configurations Enabled)
```json
{
  "queries": [
    {
      "resource": "Patient",
      "searchParams": "birthdate=lt2006-01-01&birthdate=gt1944-01-01&deceased=false&_elements=id",
      "exclude": false,
      "rationale": "The patient resource is used to filter patients based on age and deceased status. The birthdate is used to filter patients between 18 and 80 years old. The deceased field is used to filter for alive patients."
    },
    {
      "resource": "Condition",
      "codeExtractResults": [
        {
          "systemName": "SNOMED_CT_US_LITE",
          "codes": [
            {
              "code": "254637007",
              "description": "Non-small cell lung cancer (disorder)",
              "reason": "The text does not mention 'Non-small cell lung cancer (disorder)' explicitly, but it does mention 'nsclc' which is an acronym for it"
            },
            {
              "code": "1255725002",
              "description": "NSCLC (non-small cell lung cancer) adenocarcinoma type",
              "reason": "The text mentions 'nsclc' which is an acronym for 'non-small cell lung cancer', but not specifically the adenocarcinoma type"
            },
            {
              "code": "457721000124104",
              "description": "Metastatic non-small cell lung cancer (disorder)",
              "reason": "The text does not mention 'Metastatic non-small cell lung cancer (disorder)' explicitly, but it does mention 'nsclc' which is an acronym for non-small cell lung cancer"
            }
          ]
        }
      ],
      "searchParams": "code=254637007,1255725002,457721000124104&_elements=id",
      "exclude": false,
      "rationale": "The condition resource is used to filter patients based on the condition of nsclc. The code field is used to filter patients with nsclc."
    }
  ],
  "sql": "\nSELECT id \nFROM (SELECT DISTINCT id\nFROM {PROJECT_ID}.{DATASET}.{PATIENT_TABLE}\nWHERE birthDate < '1944-01-01' AND birthDate > '2006-01-01' AND deceased IS NULL)\nWHERE id IN (\n    SELECT DISTINCT subject.patientId AS id\nFROM {PROJECT_ID}.{DATASET}.{CONDITION_TABLE},\n  UNNEST(code.coding) as coding\nWHERE coding.code IN ('254637007','1255725002','457721000124104') AND coding.system IN ('http://snomed.info/sct')\n);",
  "cohortDescription": "between 18 and 80 years old with nsclc"
}
```

### Minimal Response (Basic Configurations)
```json
{
  "queries": [
    {
      "resource": "Patient",
      "searchParams": "birthdate=lt2006-01-01&birthdate=gt1944-01-01&deceased=false&_elements=id",
      "exclude": false
    },
    {
      "resource": "Condition",
      "searchParams": "code=254637007,1255725002,457721000124104&_elements=id",
      "exclude": false
    }
  ],
  "sql": "",
  "cohortDescription": "between 18 and 80 years old with nsclc"
}
```

## Response Fields

### queries
Array of FHIR search queries where each query contains:
- `resource`: FHIR resource type (e.g., "Patient", "Condition")
- `searchParams`: FHIR search parameters
- `exclude`: Boolean indicating if this is an exclusion criteria
- `rationale`: (optional) AI rationale for the query component
- `codeExtractResults`: (optional) Medical codes extracted from text. SNOMED_CT_US_LITE (subset of SNOMED codes mapped to ICD10) and RXNORM are currently supported. 

### sql
Generated SQL query when `sql_syntax` is specified. Variables in curly braces need to be replaced with your actual table names. The Jupyter notebook includes code to help with this. 
- `{PROJECT_ID}`: Your BigQuery project ID
- `{DATASET}`: Your FHIR dataset name
- `{PATIENT_TABLE}`: Your FHIR Patient table name
- `{CONDITION_TABLE}`: Your FHIR Condition table name

### cohortDescription
Echo of the input text description for reference. 