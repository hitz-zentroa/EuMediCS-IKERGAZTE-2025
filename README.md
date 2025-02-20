# IKERGAZTE 2025: Medikuntzaren Domeinuko Euskarazko Corpus Sintetikoa Sortzen: Itzultzaile Automatikoen Ekarpena
**Egileak:**

## Itzultzailetan erabilitako datuak

### Terminologia

* [**ICD-10**](https://icdcdn.who.int/icd10/index.html): Banakako esaldien bilduma, guztiak arlo medikoari dagozkionak.
* [**SNOMED**](https://www.sanidad.gob.es/va/areas/saludDigital/interoperabilidadSemantica/factoriaRecursos/snomedCT/home.htm): Esaldi osoak izan beharrean, gaixotasunak, prozedurak, egitura anatomikoak eta beste hainbat termino mediko biltzen dituen datu-multzoa.

### Domeinuko testuak

* **elhuyar_med**: Ingelesezko liburu eta dokumentu medikoak, euskarara itzuliak.
* **elhuyar_kimika**: elhuyar med-en antzekoa, baina jatorrizko dokumentuetatik ateratako iragazki gabeko esaldiak ez ditu barne hartzen. Medikuntzarekin zuzenean lotuta ez badago ere, biokimikaren terminologia espezifikoa biltzen du.

### Esaldi orokorrak

* **Datu-multzo orokorra**: Espainieratik eta ingelesetik euskarara itzulitako esaldiak biltzen dituen datu-multzo ez-espezializatua.

## Aurreprozesamendua

1. Corpus bilketa eta kateamendua
2. [Bifixer](https://github.com/bitextor/bifixer) erabilita corpus paraleloen garbiketa orokorra burutu eta corpus elebidunen kalitatea hobetzen da.
3. Esaldien filtraketa burutzen da LaBSE similarity aplikatuz, errepresentazio bektorialak erabiliz esaldi paralelo pareak identifikatuz → [``LAaBSE_similarity_batches.py``](LaBSE_similarity_batches.py)
4. Esaldi duplikatuak kentzen dira → [``remove_duplicates.perl``](remove_duplicates.perl)


## Entrenamendua

Ereduak entrenatzeko, [MarianMT](https://huggingface.co/docs/transformers/model_doc/marian) erabili da, Transformer arkitekturan oinarritua. Hurrengo komandoa erabili da:

```
  marian \
    --model en-eu/model/model.npz --type transformer \
    --train-sets train_clean.en train_clean.eu \
    --vocabs en-eu/model/vocab.eneu.spm en-eu/model/vocab.eneu.spm \
    --dim-vocabs 8000 8000 --mini-batch-fit -w $WORKSPACE --maxi-batch 1000 \
    --valid-freq 500 --save-freq 500 --disp-freq 100 --valid-mini-batch 64 \
    --valid-metrics cross-entropy perplexity ce-mean-words bleu-detok \
    --valid-sets Flores-dev.en Flores-dev.eu \
    --early-stopping 5 --max-length 200 --overwrite --keep-best \
    --log en-eu/model/train.log --valid-log en-eu/model/valid.log \
    --tempdir en-eu/model --transformer-heads 8 \
    --enc-depth 6 --dec-depth 6 --tied-embeddings-all \
    --transformer-dropout 0.1 --label-smoothing 0.1 \
    --learn-rate 0.0003 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
    --optimizer-params 0.9 0.98 1e-09 --clip-norm 5 \
    --sync-sgd --exponential-smoothing \
    --normalize=0.6 --beam-size=6 --quiet-translation \
    --devices 0 1
```

## Itzultzaileak

Entrenatutako hiru itzultzaileak *HuggingFace* webgunean eskegita daude haien atzipena errazteko. Sortutako modeloak PyTorch-era moldatu dira haien erabilpena errazteko.

* Eleaniztun eredua (ingelesetik zein gaztelaniatik euskerarako itzultzailea): [anegda/medical_enes-eu](https://huggingface.co/anegda/medical_enes-eu)
* Gaztelaniatik euskerarako itzultzailea: [anegda/medical_es-eu](https://huggingface.co/anegda/medical_es-eu)
* Ingelesetik euskerarako itzultzailea: [anegda/medical_en-eu](https://huggingface.co/anegda/medical_en-eu) 

## Itzulpenak

Itzulpenak ereduekin egin ahal izateko [``translate.py``](https://github.com/Maits27/IKERGAZTE/blob/main/translate.py) script-a baliatu da, eredu ezberdinak zuzenean *HuggingFace*-etik atxikituz. 

