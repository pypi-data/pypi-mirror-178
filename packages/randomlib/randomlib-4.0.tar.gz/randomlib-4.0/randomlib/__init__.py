import logging
import transformers
import huggingface_hub.utils #as hf_hub_utils
import pandas as pd
logging.disable(logging.INFO) # disable INFO 
logging.disable(logging.DEBUG) # disable INFO 
logging.disable(logging.WARNING) # disable INFO 
# hf_hub_utils.disable_progress_bars()
transformers.utils.logging.disable_progress_bar
pd.options.display.max_colwidth = None

