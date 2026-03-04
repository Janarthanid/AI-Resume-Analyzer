from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity(jd, resume):
    jd_embed = model.encode(jd)
    resume_embed = model.encode(resume)
    score = util.cos_sim(jd_embed, resume_embed)
    return float(score)
