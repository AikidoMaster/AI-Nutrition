#!/usr/bin/env python
# coding: utf-8

# In[80]:


import pandas as pd


# In[ ]:


##Ingestion


# In[ ]:


df = pd.read_csv('data/data.csv')


# In[82]:


import pandas as pd

# Step 1: Read the original CSV file
df = pd.read_csv('data/data.csv')

# Step 2: Convert column names to lowercase and replace spaces/special characters
df.columns = (
    df.columns.str.lower()
    .str.replace(' ', '_')
    .str.replace('(', '')
    .str.replace(')', '')
    .str.replace('$', '')
)

# Step 4: Replace NaN values with empty strings and convert the entire DataFrame to strings
df = df.fillna('').astype(str)

# Step 5: Add an "ID" column with sequential values starting from 1
df['id'] = range(1, len(df) + 1)

# Step 6: Reorder the columns to make "ID" the first column
cols = ['id'] + [col for col in df.columns if col != 'id']
df = df[cols]

# Step 7: Save the modified DataFrame back to a new CSV file
df.to_csv('data/data.csv', index=False)

print("CSV file saved successfully with 'ID' as the first column!")


# In[79]:


df.columns


# In[63]:


get_ipython().system('curl -O https://raw.githubusercontent.com/alexeygrigorev/minsearch/main/minsearch.py')


# In[64]:


documents = df.to_dict(orient='records')


# In[65]:


documents


# In[66]:


import minsearch


# In[67]:


index = minsearch.Index(
    text_fields=['recipe_name', 'ingredients', 'nutritional_information',
       'dietary_tags', 'meal_type', 'cuisine_type', 'instructions'],
    keyword_fields=['id']
)


# In[68]:


# Convert all elements to strings
documents = df.to_dict(orient='records')


# In[69]:


# Now fit the index
index.fit(documents)


# In[123]:


# RAG flow


# In[70]:


query="give me the ingredients for Vegetarian Chili" 


# In[71]:


import openai  


# In[72]:


#import os

#api_key = os.getenv('OPENAI_API_KEY')


# In[73]:


# API Configuration
import openai

openai.api_key = "Your_Key"


# In[74]:


def search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[75]:


prompt_template = """
You're a Nutrition insrtuctor. Answer the QUESTION based on the CONTEXT from our exercises database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

entry_template = """
recipe_name:{recipe_name}         
ingredients:{ingredients}
nutritional_information:{nutritional_information}
dietary_tags:{dietary_tags}         
meal_type:{meal_type}        
cuisine_type:{cuisine_type}          
instructions:{instructions}  
""".strip()

def build_prompt(query, search_results):
    context = ""
    
    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

 


# In[76]:


search_results=search(query)
prompt = build_prompt(query, search_results)


# In[77]:


print(prompt)


# In[56]:


def llm(prompt, model='gpt-4o-mini'):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


# In[57]:


def rag(query, model='gpt-4o-mini'):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    print(prompt)
    answer = llm(prompt, model=model)
    return answer


# In[83]:


question = 'How many calories does the Vegetarian Chili contain?'
answer = rag(question)
print(answer)


# In[84]:


df_question = pd.read_csv('data/ground-truth-retrieval.csv')


# In[85]:


df_question.head()


# In[86]:


ground_truth = df_question.to_dict(orient='records')


# In[87]:


ground_truth[0]


# In[88]:


def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)

def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)


# In[89]:


def minsearch_search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[90]:


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['id']
        results = search_function(q)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }


# In[91]:


from tqdm.auto import tqdm


# In[92]:


evaluate(ground_truth, lambda q: minsearch_search(q['question']))


# In[93]:


df_validation = df_question[:100]
df_test = df_question[100:]


# Tuning and Finding the best parameters

# In[95]:


import random

def simple_optimize(param_ranges, objective_function, n_iterations=10):
    best_params = None
    best_score = float('-inf')  # Assuming we're minimizing. Use float('-inf') if maximizing.

    for _ in range(n_iterations):
        # Generate random parameters
        current_params = {}
        for param, (min_val, max_val) in param_ranges.items():
            if isinstance(min_val, int) and isinstance(max_val, int):
                current_params[param] = random.randint(min_val, max_val)
            else:
                current_params[param] = random.uniform(min_val, max_val)
        
        # Evaluate the objective function
        current_score = objective_function(current_params)
        
        # Update best if current is better
        if current_score > best_score:  # Change to > if maximizing
            best_score = current_score
            best_params = current_params
    
    return best_params, best_score


# In[96]:


gt_val = df_validation.to_dict(orient='records')


# In[97]:


def minsearch_search(query, boost=None):
    if boost is None:
        boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[98]:


param_ranges = {
    'recipe_name': (0.0, 3.0),
    'ingredients': (0.0, 3.0),
    'nutritional_information': (0.0, 3.0),
    'dietary_tags': (0.0, 3.0),
    'meal_type': (0.0, 3.0),
    'cuisine_type': (0.0, 3.0),
    'instructions': (0.0, 3.0),
}

def objective(boost_params):
    def search_function(q):
        return minsearch_search(q['question'], boost_params)

    results = evaluate(gt_val, search_function)
    return results['mrr']


# In[99]:


simple_optimize(param_ranges, objective, n_iterations=20)


# In[102]:


def minsearch_improved(query):
    boost = {
        'recipe_name': 2.46,
        'ingredients': 0.01,
        'nutritional_information': 1.35,
        'dietary_tags': 0.72,
        'meal_type': 1.16,
        'cuisine_type': 1.26,
        'instructions': 2.61    

    }

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results

evaluate(ground_truth, lambda q: minsearch_improved(q['question']))


# RAG evaluation

# In[103]:


prompt2_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


# In[104]:


len(ground_truth)


# In[107]:


record = ground_truth[0]
question = record['question']
answer_llm = rag(question)


# In[108]:


print(answer_llm)


# In[109]:


prompt = prompt2_template.format(question=question, answer_llm=answer_llm)
print(prompt)


# In[110]:


import json


# In[111]:


df_sample = df_question.sample(n=200, random_state=1)


# In[112]:


sample = df_sample.to_dict(orient='records')


# In[113]:


evaluations = []

for record in tqdm(sample):
    question = record['question']
    answer_llm = rag(question) 

    prompt = prompt2_template.format(
        question=question,
        answer_llm=answer_llm
    )

    evaluation = llm(prompt)
    evaluation = json.loads(evaluation)

    evaluations.append((record, answer_llm, evaluation))


# In[116]:


df_eval = pd.DataFrame(evaluations, columns=['record', 'answer', 'evaluation'])

df_eval['id'] = df_eval.record.apply(lambda d: d['id'])
df_eval['question'] = df_eval.record.apply(lambda d: d['question'])


# In[117]:


df_eval['relevance'] = df_eval.evaluation.apply(lambda d: d['Relevance'])
df_eval['explanation'] = df_eval.evaluation.apply(lambda d: d['Explanation'])


# In[118]:


del df_eval['record']
del df_eval['evaluation']


# In[119]:


df_eval.relevance.value_counts(normalize=True)


# In[120]:


df_eval.to_csv('data/rag-eval-gpt-4o-mini.csv', index=False)


# In[122]:


df_eval[df_eval.relevance == 'PARTLY_RELEVANT']


# In[ ]:




