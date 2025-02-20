from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import csv
import argparse

def cos_sim(u,v):
    return 1 - cosine(u,v)

parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

model = SentenceTransformer('sentence-transformers/LaBSE')
parser.add_argument("input", help="input file to be process")
parser.add_argument("output", help="output file to write ")

args = parser.parse_args()


with open(args.input, "r", encoding="utf8") as input_file:
    tsv_reader = csv.reader(input_file, delimiter="\t", quoting=csv.QUOTE_NONE)
    l1 = []
    l2 = []
    h = []
    q = []
    for row in tsv_reader:
        l1.append(row[0])
        l2.append(row[1])
        h.append(row[2])
        q.append(row[3])

encodeL1 = model.encode(l1, batch_size=4, show_progress_bar=True)
encodeL2 = model.encode(l2,batch_size=4, show_progress_bar=True)
outputs = [cos_sim(x[0], x[1]) for x in zip(encodeL1, encodeL2)]
with open(args.output, "w", encoding="utf8") as output_file:
    for output in zip(l1, l2, h, q, outputs):
        print(output[0] +"\t" + output[1] + "\t" + output[2] + "\t" + str(output[3]) + "\t" + str(output[4]), file=output_file)