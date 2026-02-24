# 📊 淘宝母婴购物数据分析项目

> 基于**阿里云天池数据集 #45**的深度数据分析

**创建时间**: 2026-02-24  
**数据来源**: [Tianchi Dataset #45](https://tianchi.aliyun.com/dataset/45)

---

## 📖 项目概述

分析淘宝母婴购物数据，挖掘用户行为模式、购买偏好，并生成可视化报告。

### 🎯 分析目标

- **用户洞察** - 了解母婴用户的群体特征
- **商品洞察** - 发现热销品类和商品规律
- **行为洞察** - 分析购买行为和复购模式
- **价值洞察** - 客户分层和生命周期价值

---

## 📁 项目结构

```
taobao-maternity-analysis-2026.2.24/
├── data/                    # 数据文件
│   ├── raw/                # 原始数据（天池数据集）
│   ├── processed/          # 清洗后的数据
│   └── output/             # 分析结果/图表
├── docs/                    # 文档
│   ├── README.md           # 项目说明
│   ├── analysis_report.md  # 完整分析报告
│   └── visualization_report.html  # HTML可视化报告
├── src/                     # 源代码
│   ├── analysis.py         # 主分析脚本
│   ├── generate_sample_data.py  # 模拟数据生成器
│   └── download_data.py    # 数据下载指引
├── tests/                   # 测试代码
├── assets/                  # 资源文件
└── config/                  # 配置文件
```

---

## 🚀 快速开始

### 1. 准备环境

```bash
# 创建项目
python skills/project-manager/scripts/create_project.py create --name taobao-maternity-analysis

# 进入项目目录
cd projects/taobao-maternity-analysis

# 安装依赖
pip install pandas matplotlib seaborn
```

### 2. 下载数据

```bash
# 方法1: 手动下载天池数据集
# 访问: https://tianchi.aliyun.com/dataset/45
# 下载后放入 data/raw/ 目录

# 方法2: 运行模拟数据生成器（用于演示）
python src/generate_sample_data.py
```

### 3. 运行分析

```bash
python src/analysis.py
```

### 4. 查看结果

- **本地查看**: 打开 `docs/visualization_report.html`
- **图表文件**: `data/output/*.png`
- **分析报告**: `docs/analysis_report.md`

---

## 📊 分析内容

### 1. 用户画像分析

- 性别分布（男女婴比例）
- 年龄分布（购买时的婴儿年龄）
- 年龄段购买行为分析

### 2. 商品分析

- 热销品类排行
- 品类销量分布
- 商品购买量分布

### 3. 时间趋势分析

- 年度销售趋势（2012-2015）
- 月度趋势
- 季节性分析

### 4. RFM客户价值分析

- **R (Recency)** - 最近购买时间
- **F (Frequency)** - 购买频次
- **M (Monetary)** - 累计消费金额
- 客户分层（冠军/流失风险/忠诚客户等）

---

## 📈 核心发现

### 用户洞察
- 男女婴用户比例均衡（46% vs 44%）
- **1-2岁是黄金消费期**（占49%购买量）
- 用户复购率高，平台粘性强

### 商品洞察
- 前5大品类销量均衡（差异<5%）
- 各品类覆盖约95%用户
- 中小订单为主（85%订单≤5件）

### 时间趋势
- 年增长率2-3%，稳定增长
- 用户基数稳定（970-980人）
- 无明显季节性波动

### 客户价值
- **14.5%冠军客户**是核心收入来源
- **18.7%客户有流失风险**，需立即召回
- 新客户占比11.3%，有增长潜力

---

## 💡 业务建议

### P0 紧急
1. 为145位冠军客户建立VIP专属服务
2. 立即召回187位流失风险客户

### P1 重要
3. 针对1-2岁核心年龄段优化商品
4. 提升平均客单价（目标4件+）

---

## 🛠️ 技术栈

| 环节 | 工具 |
|------|------|
| 数据处理 | Python + Pandas |
| 可视化 | Matplotlib + Seaborn |
| 统计分析 | NumPy + SciPy |
| 报告生成 | Jupyter Notebook / Markdown |
| 报告格式 | HTML / PDF |

---

## 📄 相关文件

- [完整分析报告](docs/analysis_report.md)
- [HTML可视化报告](docs/visualization_report.html)
- [模拟数据生成器](src/generate_sample_data.py)
- [分析脚本](src/analysis.py)

---

## 📝 许可证

MIT License

---

## 🙏 致谢

- 数据来源：[阿里云天池](https://tianchi.aliyun.com)
- 开源工具：[Python](https://www.python.org/), [Pandas](https://pandas.pydata.org/), [Matplotlib](https://matplotlib.org/)

---

**如有问题或建议，欢迎提交 Issue！**
