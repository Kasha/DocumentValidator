html_doc_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "document_id": {
      "type": "object",
      "properties": {
        "value": {
          "type": "string"
        },
        "location": {
          "type": "integer"
        }
      },
      "required": [
        "value",
        "location"
      ]
    },
    "title": {
      "type": "object",
      "properties": {
        "value": {
          "type": "string"
        },
        "location": {
          "type": "integer"
        }
      },
      "required": [
        "value",
        "location"
      ]
    },
    "header": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "row": {
              "type": "object",
              "properties": {
                "row": {
                  "type": "integer"
                },
                "location": {
                  "type": "integer"
                }
              },
              "required": [
                "row",
                "location"
              ]
            },
            "columns": {
              "type": "array",
              "items": [
                {
                  "type": "object",
                  "properties": {
                    "col": {
                      "type": "integer"
                    },
                    "location": {
                      "type": "integer"
                    },
                    "value": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "col",
                    "location",
                    "value"
                  ]
                },
              ]
            }
          },
          "required": [
            "row",
            "columns"
          ]
        }
      ]
    },
    "body": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "row": {
              "type": "object",
              "properties": {
                "row": {
                  "type": "integer"
                },
                "location": {
                  "type": "integer"
                }
              },
              "required": [
                "row",
                "location"
              ]
            },
            "columns": {
              "type": "array",
              "items": [
                {
                  "type": "object",
                  "properties": {
                    "col": {
                      "type": "integer"
                    },
                    "location": {
                      "type": "integer"
                    },
                    "value": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "col",
                    "location",
                    "value"
                  ]
                }
              ]
            }
          },
          "required": [
            "row",
            "columns"
          ]
        }
      ]
    },
    "footer": {
      "type": "object",
      "properties": {
        "value": {
          "type": "string"
        },
        "creation_date": {
          "type": "string"
        },
        "creation_country": {
          "type": "string"
        }
      },
      "required": [
        "value",
        "creation_date",
        "creation_country"
      ]
    }
  },
  "required": [
    "document_id",
    "title",
    "header",
    "body",
    "footer"
  ]
}