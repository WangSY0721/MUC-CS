import jieba

s='王蒋小明在加州理工大学上学'
words=jieba.lcut(s,cut_all=False)		#将中文文本拆分为词语保存到列表words中.
print(words)
