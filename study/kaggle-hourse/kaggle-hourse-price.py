# 导入需要的模块
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 用来绘图的，封装了matplot
# 要注意的是一旦导入了seaborn，
# matplotlib的默认作图风格就会被覆盖成seaborn的格式
import seaborn as sns
from scipy import stats
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')
# 1.读取训练集
data_train = pd.read_csv("./train.csv")
# print(data_train)
# 2.查看数据集中 SalePrice 这一列中的统计情况
sale_price_col = data_train['SalePrice']
sale_price_aly = sale_price_col.describe()
print(sale_price_aly)  # 由分析结果可知，SalePrice 这一列没有无效或者其他非数值数据
# 3.通过图示化来进一步展示“SalePrice”
sns.distplot(sale_price_col)
plt.show()
# 4.峰度和偏度
# 偏度：偏度（Skewness）是描述某变量取值分布对称性的统计量。
# Skewness=0 分布形态与正态分布偏度相同
# Skewness>0 正偏差数值较大，为正偏或右偏。长尾巴拖在右边。
# Skewness<0 负偏差数值较大，为负偏或左偏。长尾巴拖在左边。
# 计算公式： S= (X^ - M_0)/δ Skewness 越大，分布形态偏移程度越大。
print("偏度(Skewness): %f" % data_train['SalePrice'].skew())
# 峰度：峰度（Kurtosis）是描述某变量所有取值分布形态陡缓程度的统计量。
# Kurtosis=0 与正态分布的陡缓程度相同。
# Kurtosis>0 比正态分布的高峰更加陡峭——尖顶峰
# Kurtosis<0 比正态分布的高峰来得平台——平顶峰计算公式：β = M_4 /σ^4 偏度：
print("峰度(Kurtosis): %f" % data_train['SalePrice'].kurt())
# 将上面的计算结果、理论和图形相对比可以看到，长尾巴确实拖在右边，而且高峰陡峭。

# 分析数据特征
# 为了让我们对数据的分析更具科学性，我们可以新建一个excel文件，具体需要记录的数据如下：
# Variable：变量名
# Data Type：各变量的数据类型，分为“数值型--0”和“类别型--1”
# Segment：变量的类型。分为：“building--0”、“space--1”、“location--2”。具体解释如下：
#   building：比如房屋材料、造型等与房屋物理特性相关的特征（e.g. 'OverallQual'）
#   space：即与房屋空间有关的特征，如面积(e.g. 'TotalBsmtSF')
#   location：如地段、道路情况等(e.g. 'Neighborhood')
# Expectation：表示我们认为该变量对于“SalePrice”的影响程度，划分为“High---3”，“Medium---2”，“Low---1”
# Conclusion：与“Expectation”类似，这个表示我们在观察完数据后得出的结论，其实也可和“Expectation”相同。
# Comments：其他关于该变量的一些看法

# 对整理后的数据进一步分析来选出主要影响售价的特征，提取特征，提取有代表性，差异较大的部分
# 入选特征
# Variable	Segment	Data Type	Comments
# LotArea	    1	      0	    地皮面积
# GrLivArea	    1	      0	    生活面积
# TotalBsmtSF	1	      0	    地下室总面积
# MiscVal	    0	      0	    其他资产
# GarageArea/GarageCars	1 0	    车库
# YearBuilt	    0	      1	    建造年份
# CentralAir	0	      1	    中央空调
# OverallQual	0	      1	    总体评价
# Neighborhood	2	      1	    地段

# 验证主要特征是否满足要求
# 类别特征
# 1.中央空调
center_area = 'CentralAir'
# axis=0代表往跨行（down)，而axis=1代表跨列（across)
data = pd.concat([data_train['SalePrice'],data_train[center_area]], axis=1)
# 注意CenterAir这一列，就由两个取值组成，一个是X，一个是Y
fig = sns.boxplot(x = center_area,y = 'SalePrice',data = data)
fig.axis(ymin = 0,ymax = 800000)
plt.show()      # 有中央空调，价格更高

# 2.OverallQual 总体质量
overall_qual = 'OverallQual'
data = pd.concat([data_train['SalePrice'], data_train[overall_qual]], axis=1)
fig = sns.boxplot(x=overall_qual, y='SalePrice', data=data)
fig.axis(ymin=0, ymax=800000)
plt.show()      # OverallQual 越大，房价越高

# 3.YearBuilt 建造年份
year_built = 'YearBuilt'
data = pd.concat([data_train['SalePrice'], data_train[year_built]], axis=1)
f, ax = plt.subplots(figsize=(26, 12))
fig = sns.boxplot(x=year_built, y="SalePrice", data=data)
fig.axis(ymin=0, ymax=800000)
plt.show()
# 年份与价格的散点图
data.plot.scatter(x = year_built, y = 'SalePrice',ylim = (0,800000))
plt.show()
# 用了箱线图绘制了房价与建造年份的关系，但是并不十分明显，
# 所以又用点图来显示，可以很明显的看到有线性增长的趋势。

# 4.Neighborhood 地段
neighborhood = 'Neighborhood'
data = pd.concat([data_train['SalePrice'], data_train[neighborhood]], axis=1)
f, ax = plt.subplots(figsize=(26, 12))
fig = sns.boxplot(x=neighborhood , y="SalePrice", data=data)
fig.axis(ymin=0, ymax=800000);
plt.show()