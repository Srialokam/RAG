from src.chat import ask
from dotenv import load_dotenv
import json

load_dotenv()

# 20 questions with known correct keywords from the PDF
test_cases = [
    {"question": "What is dbt?", "keywords": ["transformation", "ELT", "SQL", "analytics"]},
    {"question": "What is the difference between dbt Core and dbt Cloud?", "keywords": ["free", "open source", "paid", "CLI", "managed"]},
    {"question": "What is the medallion architecture?", "keywords": ["bronze", "silver", "gold"]},
    {"question": "What is a dbt snapshot?", "keywords": ["SCD", "history", "dbt_valid_from", "dbt_valid_to"]},
    {"question": "What does the ref() function do?", "keywords": ["dependency", "reference", "model"]},
    {"question": "What is the source() function?", "keywords": ["source", "raw", "database"]},
    {"question": "What is dbt Canvas?", "keywords": ["drag", "visual", "no-code", "cloud"]},
    {"question": "What is Jinja in dbt?", "keywords": ["template", "dynamic", "SQL"]},
    {"question": "What is a dbt macro?", "keywords": ["reusable", "function", "DRY"]},
    {"question": "What does dbt build command do in dbt?", "keywords": ["seed", "run", "test", "snapshot", "DAG", "order"]},
    {"question": "What is generate_schema_name used for?", "keywords": ["schema", "prod", "prefix"]},
    {"question": "What does dbt docs generate do?", "keywords": ["catalog", "manifest", "documentation"]},
    {"question": "What is a DAG in dbt?", "keywords": ["directed", "dependency", "lineage"]},
    {"question": "When should you use seeds in dbt?", "keywords": ["CSV", "static", "mapping", "codes"]},
    {"question": "What does dbt_valid_to null mean?", "keywords": ["current", "active", "record"]},
    {"question": "What is the loop.last pattern?", "keywords": ["comma", "column", "Jinja"]},
    {"question": "What is the Bronze layer?", "keywords": ["raw", "source", "ingestion"]},
    {"question": "What is the Silver layer?", "keywords": ["cleansed", "joined", "transformed"]},
    {"question": "What is the Gold layer?", "keywords": ["aggregation", "KPI", "business"]},
    {"question": "What is dbt test used for?", "keywords": ["quality", "assertion", "data", "tests"]}
]

def evaluate():
    print("Running evaluation on 20 questions...\n")
    
    passed = 0
    failed = 0
    results = []

    for i, test in enumerate(test_cases):
        question = test["question"]
        keywords = test["keywords"]
        
        result = ask(question)
        answer = result["answer"].lower()
        sources = result["sources"]
        
        # Check if at least half the keywords appear in the answer
        matched = [kw for kw in keywords if kw.lower() in answer]
        success = len(matched) >= len(keywords) / 2
        
        status = "✅ PASS" if success else "❌ FAIL"
        if success:
            passed += 1
        else:
            failed += 1

        results.append({
            "question": question,
            "answer": result["answer"],
            "sources": sources,
            "matched_keywords": matched,
            "passed": success
        })

        print(f"[{i+1}/20] {status} | {question}")
        print(f"        Keywords matched: {matched}\n")

    # Summary
    score = (passed / len(test_cases)) * 100
    print("\n--- Evaluation Summary ---")
    print(f"Passed:  {passed}/20")
    print(f"Failed:  {failed}/20")
    print(f"Score:   {score:.1f}%")

    if score >= 80:
        print("Rating:  🟢 Great — your RAG is performing well")
    elif score >= 60:
        print("Rating:  🟡 Good — some answers need improvement")
    else:
        print("Rating:  🔴 Needs work — consider adjusting chunk size")

    # Save results to file
    with open("evaluation_results.json", "w") as f:
        json.dump({
            "score": score,
            "passed": passed,
            "failed": failed,
            "results": results
        }, f, indent=2)
    
    print("\nFull results saved to evaluation_results.json")

if __name__ == "__main__":
    evaluate()