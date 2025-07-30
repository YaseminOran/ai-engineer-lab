# MLflow Experiments Directory

Bu klasör, MLflow deneylerinin metadata bilgilerini içerir.

## Deney Yapısı

```
mlflow/experiments/
├── README.md                    # Bu dosya
├── iris_initial/               # İlk deney
│   ├── meta.yaml              # Deney metadata
│   └── runs/                  # Çalıştırma kayıtları
├── iris_manual_training/       # Manuel eğitim deneyi
│   ├── meta.yaml              # Deney metadata
│   └── runs/                  # Çalıştırma kayıtları
└── iris_retraining/           # Yeniden eğitim deneyi
    ├── meta.yaml              # Deney metadata
    └── runs/                  # Çalıştırma kayıtları
```

## Deney Detayları

### iris_initial
- **Deney ID**: 1
- **Oluşturma Tarihi**: 2024-01-15
- **Durum**: Active
- **Çalıştırma Sayısı**: 3
- **Amaç**: İlk model eğitimi ve karşılaştırma

### iris_manual_training
- **Deney ID**: 2
- **Oluşturma Tarihi**: 2024-01-15
- **Durum**: Active
- **Çalıştırma Sayısı**: 3
- **Amaç**: Manuel model eğitimi

### iris_retraining
- **Deney ID**: 3
- **Oluşturma Tarihi**: 2024-01-15
- **Durum**: Active
- **Çalıştırma Sayısı**: 1
- **Amaç**: Model yeniden eğitimi

## Çalıştırma Kayıtları

### iris_initial Runs
1. **Run 1**: Logistic Regression
   - Accuracy: 0.93
   - Duration: 2.1s
   - Status: Finished

2. **Run 2**: Random Forest
   - Accuracy: 0.90
   - Duration: 3.5s
   - Status: Finished

3. **Run 3**: SVM
   - Accuracy: 0.97
   - Duration: 1.8s
   - Status: Finished

### iris_manual_training Runs
1. **Run 1**: Logistic Regression
   - Accuracy: 0.93
   - Duration: 2.0s
   - Status: Finished

2. **Run 2**: Random Forest
   - Accuracy: 0.90
   - Duration: 3.2s
   - Status: Finished

3. **Run 3**: SVM
   - Accuracy: 0.97
   - Duration: 1.9s
   - Status: Finished

### iris_retraining Runs
1. **Run 1**: Random Forest (Optimized)
   - Accuracy: 0.98
   - Duration: 4.1s
   - Status: Finished

## Metadata Formatı

### meta.yaml
```yaml
artifact_location: ./mlflow/artifacts
experiment_id: "1"
lifecycle_stage: active
name: iris_initial
```

### Run Metadata
```yaml
run_id: "abc123def456"
experiment_id: "1"
status: FINISHED
start_time: 1642234567
end_time: 1642234570
```

## Kullanım

### MLflow UI
```bash
# MLflow UI başlatma
mlflow ui --port 5001

# Belirli bir deneyi görüntüleme
mlflow ui --port 5001 --experiment-name iris_manual_training
```

### Programatik Erişim
```python
import mlflow

# Deney listesi
experiments = mlflow.list_experiments()
print(experiments)

# Belirli bir deneyi getirme
experiment = mlflow.get_experiment_by_name("iris_manual_training")
print(experiment)

# Deney çalıştırmalarını arama
runs = mlflow.search_runs(experiment.experiment_id)
print(runs)
```

### Deney Karşılaştırma
```python
# İki deneyi karşılaştırma
exp1 = mlflow.get_experiment_by_name("iris_initial")
exp2 = mlflow.get_experiment_by_name("iris_manual_training")

runs1 = mlflow.search_runs(exp1.experiment_id)
runs2 = mlflow.search_runs(exp2.experiment_id)

# En iyi sonuçları karşılaştırma
best_run1 = runs1.loc[runs1['metrics.accuracy'].idxmax()]
best_run2 = runs2.loc[runs2['metrics.accuracy'].idxmax()]

print(f"İlk deney en iyi: {best_run1['metrics.accuracy']}")
print(f"İkinci deney en iyi: {best_run2['metrics.accuracy']}")
```

## Notlar

- Deney metadata'ları MLflow tarafından otomatik oluşturulur
- Her deney benzersiz bir ID'ye sahiptir
- Çalıştırma kayıtları deney içinde saklanır
- Deneyler MLflow UI üzerinden yönetilebilir
- Eski deneyler arşivlenebilir veya silinebilir 