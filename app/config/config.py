# Standard library imports
import os

# ****************** [START] Google Cloud project settings ****************** #
project =  os.getenv('GCP_PROJECT')
location = os.environ.get('GCP_REGION', 'us-central1')
# ******************* [END] Google Cloud project settings ******************* #


# ************************* [START] BigQuery config ************************* #
bigquery_dataset = os.getenv('BIGQUERY_DATASET')
# ************************** [END] BigQuery config ************************** #


# *********************** [START] LLM parameter config ********************** #
# Vertex AI model to use for the LLM
model_name='gemini-pro@latest'

# maximum number of model responses generated per prompt
candidate_count = 1

# determines the maximum amount of text output from one prompt.
# a token is approximately four characters.
max_output_tokens = 2048

# temperature controls the degree of randomness in token selection.
# lower temperatures are good for prompts that expect a true or
# correct response, while higher temperatures can lead to more
# diverse or unexpected results. With a temperature of 0 the highest
# probability token is always selected. for most use cases, try
# starting with a temperature of 0.2.
temperature = 0

# top-p changes how the model selects tokens for output. Tokens are
# selected from most probable to least until the sum of their
# probabilities equals the top-p value. For example, if tokens A, B, and C
# have a probability of .3, .2, and .1 and the top-p value is .5, then the
# model will select either A or B as the next token (using temperature).
# the default top-p value is .8.
top_p = .8

# top-k changes how the model selects tokens for output.
# a top-k of 1 means the selected token is the most probable among
# all tokens in the model’s vocabulary (also called greedy decoding),
# while a top-k of 3 means that the next token is selected from among
# the 3 most probable tokens (using temperature).
top_k = 40

# how verbose the llm and langchain agent is when thinking
# through a prompt. you're going to want this set to True
# for development so you can debug its thought process
verbose = True
# *********************** [END] LLM parameter config ************************ #


# ********************** [START] Configuration Checks *********************** #
if not project:
    raise Exception('GCP_PROJECT environment variable not set')

if not bigquery_dataset:
    raise Exception('BIGQUERY_DATASET environment variable not set')
# *********************** [END] Configuration Checks ************************ #
