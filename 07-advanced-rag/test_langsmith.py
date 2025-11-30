import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()
key = os.getenv('LANGSMITH_API_KEY')

if not key:
    print("ERROR: LANGSMITH_API_KEY not found in .env")
    exit(1)

print(f"Testing LangSmith API with key: {key[:20]}...")
client = Client(api_key=key)

print("\n1. Testing basic connection (get_project)...")
try:
    # Попробуем получить информацию о проекте по умолчанию
    info = client.get_project()
    print(f"   ✓ Success! Project info retrieved")
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}: {e}")

print("\n2. Testing list_projects...")
try:
    projects = list(client.list_projects(limit=1))
    print(f"   ✓ Success! Found {len(projects)} projects")
    if projects:
        print(f"   Project name: {projects[0].name}")
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}: {e}")

print("\n3. Testing list_datasets (read access)...")
try:
    datasets = list(client.list_datasets(limit=1))
    print(f"   ✓ Success! Found {len(datasets)} datasets")
    if datasets:
        print(f"   Dataset name: {datasets[0].name}")
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}: {e}")
    if "403" in str(e) or "Forbidden" in str(e):
        print("   ⚠ This indicates you don't have access to datasets feature")

print("\n4. Testing create_dataset (write access)...")
try:
    # Попробуем создать тестовый датасет
    test_dataset = client.create_dataset(
        dataset_name="test-dataset-check",
        description="Temporary test dataset to check access"
    )
    print(f"   ✓ Success! Dataset created: {test_dataset.id}")
    # Удалим тестовый датасет
    client.delete_dataset(dataset_id=test_dataset.id)
    print(f"   ✓ Test dataset deleted")
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}: {e}")
    if "403" in str(e) or "Forbidden" in str(e):
        print("   ⚠ This indicates you don't have permission to create datasets")
        print("   💡 You may need to:")
        print("      - Activate datasets feature in your LangSmith account")
        print("      - Check your subscription plan")
        print("      - Verify API key permissions in settings")

print("\n5. Checking API key format...")
if key.startswith("lsv2_pt_"):
    print("   Key type: Personal Token (pt)")
elif key.startswith("lsv2_sk_"):
    print("   Key type: Secret Key (sk)")
else:
    print(f"   Key type: Unknown (starts with: {key[:8]})")




