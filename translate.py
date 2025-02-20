from transformers import MarianMTModel, MarianTokenizer
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

src_text_multilingual = ["The patient had brain damage", "El paciente tiene daño cerebral"]
#src_text_es = ["El paciente tiene daño cerebral"]
#src_text_en = ["The patient had brain damage"]

model_name_multilingual = "HiTZ/medical_enes-eu"
#model_name_es = "HiTZ/medical_es-eu"
#model_name_en = "HiTZ/medical_en-eu"

tokenizer = MarianTokenizer.from_pretrained(model_name_multilingual)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name_multilingual)
translated = model.generate(**tokenizer(src_text_multilingual, return_tensors="pt", padding=True))
print([tokenizer.decode(t, skip_special_tokens=True) for t in translated])
