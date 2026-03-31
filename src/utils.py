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