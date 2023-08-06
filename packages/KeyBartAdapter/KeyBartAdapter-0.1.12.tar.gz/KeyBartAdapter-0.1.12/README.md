# KeyBartAdapter
A neural model that extends KeyBart with adapter layers.

## Usage
```commandline
pip instal KeyBartAdapter
```

```python
from models import KeyBartAdapter
model = KeyBartAdapter(256)
```

### Huggingface
Trained checkpoints on huggingface: [link](https://huggingface.co/Adapting/KeyBartAdapter)


### Inference
```python
from transformers import AutoTokenizer
from transformers import Text2TextGenerationPipeline

tokenizer = AutoTokenizer.from_pretrained("bloomberg/KeyBART")
pipe = Text2TextGenerationPipeline(model=model,tokenizer=tokenizer)
abstract = '''Non-referential face image quality assessment methods have gained popularity as a pre-filtering step on face recognition systems. In most of them, the quality score is usually designed with face matching in mind. However, a small amount of work has been done on measuring their impact and usefulness on Presentation Attack Detection (PAD). In this paper, we study the effect of quality assessment methods on filtering bona fide and attack samples, their impact on PAD systems, and how the performance of such systems is improved when training on a filtered (by quality) dataset. On a Vision Transformer PAD algorithm, a reduction of 20% of the training dataset by removing lower quality samples allowed us to improve the BPCER by 3% in a cross-dataset test.'''
pipe(abstract)

```
