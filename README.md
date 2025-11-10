# TGQ-SSR



**Text to Graph Query Using Semantic Subgraph Retrieval – Experimental Codebase**

------



## 1. Project Overview



**TGQ-SSR** is a research codebase aimed at converting natural-language queries into graph queries via Semantic Subgraph Retrieval (SSR). The core idea is to: parse a text query → retrieve a semantically relevant subgraph from a graph database → generate a corresponding graph query (e.g., GQL/SPARQL). This pipeline is suitable for tasks such as knowledge-graph question answering, graph database retrieval, and semantic graph-query generation.


![Overview](.\assests\Overview.png)
=======
------



## 2. Key Features



- **Text-query parsing**: Map natural-language inputs to candidate graph paths/structures
- **Subgraph retrieval**: From a large graph database, identify and fetch the relevant subgraph matching the query semantics
- **Graph query generation**: From the retrieved subgraph, build an executable graph query
- **Domain-transfer experiments**: Support multiple domains (e.g., social networks, finance, healthcare) to evaluate transferability of the SSR pipeline

------



## 3. Repository Structure

```shell
.
├── 0DataImport/        # Scripts for data import / preprocessing
├── 1TestBaseModel/     # Testing base models
├── 2Finetune/          # Fine-tuning model workflows
├── 3Reason/            # Subgraph retrieval & query generation modules
├── 4Evaluation/        # Experiment evaluation, metrics computation
├── DataBase/           # Database module (AgensGraph setup)
├── Domain-transfer in medical dataset construction/    # Healthcare domain transfer scripts
├── Domain-transfer for financial dataset construction/ # Finance domain transfer scripts
└── README.md           # This README
```

------



## 4. Database Configuration (AgensGraph)

### Step 1 – Install & compile AgensGraph

This project uses AgensGraph (link: https://github.com/liruxru/agensgraph/ or the official repository) as the required database platform. You must compile/install AgensGraph in a C environment before proceeding.

**Installation steps (example on Ubuntu):**

```sh
git clone https://github.com/skaiworldwide-oss/agensgraph.git
cd agensgraph
sudo apt-get update
sudo apt-get install build-essential libreadline-dev zlib1g-dev flex bison libxml2-dev libxslt-dev libssl-dev
./configure --prefix=/usr/local/agensgraph
make install
echo "export PATH=/usr/local/agensgraph/bin:$PATH" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/agensgraph/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc
```

Refer to the official installation guide: `AgensGraph INSTALL.md`

### Step 2 – Install pgvector

This project uses `pgvector` (v0.7.0) to provide vector retrieval capabilities for AgensGraph (which is based on PostgreSQL).

```sh
git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

### Step 3 – Configure AgensGraph for Vector Support (Important)

As per the design in the thesis (Chapter 5), you need to configure AgensGraph to load and use the `pgvector` extension. This may also require **modifying the AgensGraph source code** to support vectors in extended columns (Agens-ext) or within properties (Agens-in).

1. Load `pgvector` in AgensGraph's `postgresql.conf` file.

2. Log in to the database and create the extension:

   SQL

   ```cypher
   CREATE EXTENSION pgvector;
   ```

3. (According to the thesis solution) Modify the AgensGraph storage model to support columns of type `vector(d)`.

### Step 4 – Configure Neo4j (Baseline)

For performance comparison, you can also optionally install `Neo4j` (v5.26.0). Neo4j versions 5.13+ support vector storage and indexing within properties.

### Step 5 – Database Initialization

1. Initialize your database cluster (AgensGraph).
2. Create a graph database (e.g., `CREATE GRAPH tgq_graph;`).
3. Load data using the scripts in `0DataImport/`.

------



## 5. Quick Start

### Environment Setup

1. Python version: e.g., 3.10

2. Use `virtualenv` or `conda` for isolation

3. Install dependencies:

   ```shell
   pip install -r requirements.txt
   ```

### Data Import & Vectorization

1. Ensure AgensGraph is running and accessible.

2. Enter the `0DataImport/` folder and run:

   ```shell
   cd 0DataImport/
   python import_data.py --dataset social # (social, financial, or medical)
   ```

3. Run the graph vectorization script (using BCEmbedding):

   ```sh
   python vectorize_graph.py --config config/database_config.yaml
   ```

### Model Fine-Tuning

This project uses LLaMA-Factory for model fine-tuning (LoRA). Supported models include (see thesis section 4.3.1.1 ):

- Qwen2.5 (0.5B, 1.5B, 7B, 32B)
- GLM-4 (9B-Chat)
- Gemma2 (9B-IT)
- LLama3.1 (8B-Instruct)

Run fine-tuning:

```shell
cd 2Finetune/
# (Start fine-tuning using LLaMA-Factory's command line or Web UI)
# Example (specific command depends on how you use LLaMA-Factory)
CUDA_VISIBLE_DEVICES=0,1 llama-factory-cli train --config config/finetune_qwen_lora.yaml
```



### Subgraph Retrieval & Query Generation

```shell
cd 3Reason/
python retrieve_and_generate.py --model_path /path/to/finetuned_model \
                                --query "Tell me the details about Titanic?"
```



### Evaluation

Evaluate the quality of the generated queries using the metrics defined in the thesis (section 4.3.1.4).

```shell
cd 4Evaluation/
python evaluate.py --predictions output/graph_queries.json \
                   --ground_truth data/gt_queries.json \
                   --metrics SyA SeP SeR
```

- **SyA**: Syntactic Accuracy 
- **SeP**: Semantic Precision 
- **SeR**: Semantic Recall 

------



## 6. Datasets

This project uses datasets from the following three domains for training and evaluation :

- **Social domain**: LDBC Social Network Benchmark (SNB).
- **Financial domain**: LDBC Financial Benchmark.
- **Healthcare domain**: OpenKG's Knowledge Graph of Common Family Diseases.

------



## 7. Configuration Parameters



Edit the `config/` directory to set key parameters:

| **Module**     | **Parameter**                                | **Description**                               |
| -------------- | -------------------------------------------- | --------------------------------------------- |
| **Database**   | `db_host`, `db_port`, `username`, `password` | Connection details for AgensGraph             |
| **Model**      | `learning_rate`, `batch_size`, `epochs`      | Fine-tuning settings                          |
| **Retrieval**  | `beam_width`, `max_depth`                    | Subgraph retrieval search parameters          |
| **Evaluation** | `metric_list`                                | List of evaluation metrics (e.g., F1, Recall) |

------



## 8. Output Description



- `output/subgraph.json` – The retrieved subgraph (nodes, edges, weights)
- `output/graph_queries.json` – Generated graph query statements
- `logs/` – Training logs and loss/accuracy curves
- `eval_results/` – Evaluation summaries (precision, recall, F1, etc.)

------



## 9. Contributing



We welcome contributions! Follow these steps:

1. Fork the repository and create a feature branch: `feature/your_feature`
2. Make your changes and test thoroughly
3. Update documentation or tests if needed
4. Submit a Pull Request, describing your change, its purpose, and included tests
5. Maintain consistent code style and documentation clarity

------



## 10. License



This project is licensed under the MIT License (or your preferred license). See the `LICENSE` file for full terms.

------



## 11. Contact



- **Author**: [bravo]
- **Email**: 2024439153@tju.edu.cn
- **Repository**: [https://github.com/anxiaozu/TGQ-SSR](https://www.google.com/search?q=https://github.com/anxiaozu/TGQ-SSR&authuser=1)
