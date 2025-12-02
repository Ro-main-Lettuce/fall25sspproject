from datasets import load_dataset
import pandas as pd
import subprocess
import os

# Security keywords for Task-5
SECURITY_KEYWORDS = [
    'race', 'racy', 'buffer', 'overflow', 'stack', 'integer', 'signedness',
    'underflow', 'improper', 'unauthenticated', 'gain access', 'permission',
    'cross site', 'css', 'xss', 'denial service', 'dos', 'crash', 'deadlock',
    'injection', 'request forgery', 'csrf', 'xsrf', 'forged', 'security',
    'vulnerability', 'vulnerable', 'exploit', 'attack', 'bypass', 'backdoor',
    'threat', 'expose', 'breach', 'violate', 'fatal', 'blacklist', 'overrun',
    'insecure'
]

def clean_diff_text(text):
    if text is None:
        return ""
    text = str(text)
    return text.replace('\n', '\\n').replace('"', '""')

def check_security_keywords(title, body):
    title = str(title or "").lower()
    body = str(body or "").lower()
    combined = f"{title} {body}"
    return int(any(keyword in combined for keyword in SECURITY_KEYWORDS))

def load_table(dataset_name, table_name):
    print(f"Loading {table_name}...")
    ds = load_dataset(dataset_name, table_name)
    return pd.DataFrame(ds['train'])

def task_1():
    df = load_table("hao-li/AIDev", "all_pull_request")
    task1_df = df[['title', 'id', 'agent', 'body', 'repo_id', 'repo_url']]
    task1_df.columns = ['TITLE', 'ID', 'AGENTNAME', 'BODYSTRING', 'REPOID', 'REPOURL']
    task1_df.to_csv('task1.csv', index=False, encoding='utf-8')
    print("✅ Task-1 completed")
    return task1_df

def task_2():
    df = load_table("hao-li/AIDev", "all_repository")
    task2_df = df[['id', 'language', 'stars', 'url']]
    task2_df.columns = ['REPOID', 'LANG', 'STARS', 'REPOURL']
    task2_df.to_csv('task2.csv', index=False, encoding='utf-8')
    print("✅ Task-2 completed")
    return task2_df

def task_3():
    df = load_table("hao-li/AIDev", "pr_task_type")
    task3_df = df[['id', 'title', 'reason', 'type', 'confidence']]
    task3_df.columns = ['PRID', 'PRTITLE', 'PRREASON', 'PRTYPE', 'CONFIDENCE']
    task3_df.to_csv('task3.csv', index=False, encoding='utf-8')
    print("✅ Task-3 completed")
    return task3_df

def task_4():
    df = load_table("hao-li/AIDev", "pr_commit_details")
    task4_df = df[['pr_id', 'sha', 'message', 'filename', 'status', 'additions',
                   'deletions', 'changes', 'patch']]
    task4_df.columns = ['PRID', 'PRSHA', 'PRCOMMITMESSAGE', 'PRFILE', 'PRSTATUS',
                        'PRADDS', 'PRDELSS', 'PRCHANGECOUNT', 'PRDIFF']
    task4_df['PRDIFF'] = task4_df['PRDIFF'].fillna('').apply(clean_diff_text)
    task4_df.to_csv('task4.csv', index=False, encoding='utf-8')
    print("✅ Task-4 completed")
    return task4_df

def task_5(task1_df, task3_df):
    merged_df = pd.merge(task1_df, task3_df, left_on='ID', right_on='PRID', how='left')
    merged_df['SECURITY'] = merged_df.apply(
        lambda row: check_security_keywords(row['TITLE'], row['BODYSTRING']), axis=1
    )
    task5_df = merged_df[['ID', 'AGENTNAME', 'PRTYPE', 'CONFIDENCE', 'SECURITY']]
    task5_df.columns = ['ID', 'AGENT', 'TYPE', 'CONFIDENCE', 'SECURITY']
    task5_df.to_csv('task5.csv', index=False, encoding='utf-8')
    print("✅ Task-5 completed")
    return task5_df

def main():
    print("Starting full project processing...\n")
    df1 = task_1()
    task_2()
    df3 = task_3()
    task_4()
    df5 = task_5(df1, df3)
    print("\n🎉 All tasks 1-7 completed successfully.")

if __name__ == "__main__":
    main()

