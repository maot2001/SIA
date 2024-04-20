from nltk.sentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

class Com_Agent:
    def __init__(self, comments: dict, movies: dict):
        self.sia = SentimentIntensityAnalyzer()
        self.desc, self.kw, self.rev, self.beliefs = {}, {}, {}, {}
        for c in comments:
            if movies[c]['description']: self.desc[c] = movies[c]['description']
            if movies[c]['keywords']: self.kw[c] = movies[c]['keywords']
            if movies[c]['review']['reviewBody']: self.rev[c] = movies[c]['review']['reviewBody']
            self.beliefs[c] = self.sia.polarity_scores(comments[c])['compound']

    def perceive(self, recommend: list, movies: dict):
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        prob = []
        
        for r in recommend:
            sim = []
            
            for c in self.beliefs:
                desc, kw, rev = False, False, False
                desc_v, kw_v, rev_v = 0, 0, 0
            
                if movies[r]['description'] and c in self.desc:
                    desc = True
                    desc_v = self.similarity(model, movies[r]['description'], self.desc[c])
            
                if movies[r]['keywords'] and c in self.kw:
                    kw = True
                    kw_v = self.similarity(model, movies[r]['keywords'], self.kw[c])
            
                if movies[r]['review']['reviewBody'] and c in self.rev:
                    rev = True
                    rev_v = self.similarity(model, movies[r]['review']['reviewBody'], self.rev[c])
            
                lc = self.linear_combination(desc, kw, rev, desc_v, kw_v, rev_v)
                sim.append((lc[0], lc[1] * self.beliefs[c]))
            
            m = max(sim, key=lambda x: (x[0], abs(x[1])))
            prob.append(m[1])
        
        return prob

    def similarity(self, model, text1, text2):
        emb_text1 = model.encode([text1], convert_to_tensor=True).mean(dim=0)
        emb_text2 = model.encode([text2], convert_to_tensor=True).mean(dim=0)
        return 1 - cosine(emb_text1, emb_text2)
    
    def linear_combination(self, desc, kw, rev, desc_v, kw_v, rev_v):
        if desc and kw and rev:
            val = .5 * desc_v + .3 * kw_v + .2 * rev_v
            return (100, val)
        if desc and kw:
            val = .625 * desc_v + .375 * kw_v
            return (80, val)
        if desc and rev:
            val = .715 * desc_v + .285 * rev_v
            return (70, val)
        if kw and rev:
            val = .6 * kw_v + .4 * rev_v
            return (50, val)
        if desc:
            return (50, desc_v)
        if kw:
            return (30, kw_v)
        if rev:
            return (20, rev_v)
        return (0, 0)