# Standard library imports
import os

# Third party imports
import vertexai

def initialize():
    """
    Initialize the VertexAIUtils class.
    """

    project =  os.getenv('GCP_PROJECT')
    location = os.environ.get('GCP_REGION', 'us-central1')

    vertexai.init(project=project, location=location)
