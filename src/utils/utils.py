from matplotlib.pyplot import  bar, grid, title, xlabel, xticks, ylabel, show, ylim,figure

def plotBarNulls(df, tit):
    null_counts = df.isnull().sum()
    figure(figsize=(12, 6))
    bar(null_counts.index,null_counts.values,color='skyblue')
    ylim(0, df.shape[0])
    grid(axis='y', linestyle='--', alpha=0.7)
    title(tit,fontsize=16, fontweight='bold')
    xlabel("columns",fontsize=12)
    xticks(rotation=45)
    ylabel('frequency',fontsize=12)
    show()

def fToC(x):
    return (x-32)*5/9

def cToF(x):
    return x*(9/5)+32

def categorize_complaint(text):
        if text==None:
            return None
        text = text.lower()
        if any(x in text for x in ['pain', 'abd', 'back', 'leg', 'arm', 'hip', 'foot', 'neck']):
            return 1
        elif any(x in text for x in ['chest', 'palpitations', 'tachycardia', 'nstemi', 'hypertension']):
            return 2
        elif any(x in text for x in ['shortness of breath', 'dyspnea', 'respiratory', 'pe']):
            return 3
        elif any(x in text for x in ['stroke', 'cva', 'facial droop', 'weakness', 'altered mental status']):
            return 4
        elif any(x in text for x in ['fever', 'infection', 'sepsis', 'neutropenia']):
            return 5
        elif any(x in text for x in ['psych', 'psychiatric', 'depression', 'suicide', 'si']):
            return 6
        elif any(x in text for x in ['trauma', 'fall', 'head bleed', 'fracture', 'mvc']):
            return 7
        elif any(x in text for x in ['vomiting', 'nausea', 'diarrhea', 'abdominal distention']):
            return 8
        else:
            return 9