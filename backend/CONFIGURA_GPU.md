# 🎮 Configurazione GPU per AI

## ✅ Configurazione Automatica

Il sistema rileva automaticamente la GPU e la usa se disponibile!

### Per PyTorch (AI Locale Integrata)

**✅ Già configurato!** Il codice rileva automaticamente:
- CUDA (NVIDIA GPU)
- CPU (fallback se GPU non disponibile)

**Verifica GPU:**
```python
import torch
print(f"CUDA disponibile: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
```

---

## 🚀 Configurazione Ollama per GPU

### Windows (NVIDIA)

1. **Verifica CUDA installato:**
   ```powershell
   nvidia-smi
   ```

2. **Ollama usa automaticamente la GPU se disponibile!**
   - Ollama rileva automaticamente CUDA
   - Non serve configurazione aggiuntiva

3. **Verifica che Ollama usi GPU:**
   ```powershell
   ollama run llama3.2 "test"
   # Controlla Task Manager -> GPU per vedere utilizzo
   ```

### Forzare uso GPU (se necessario)

Se Ollama non usa la GPU automaticamente:

1. **Installa CUDA Toolkit:**
   - Download: https://developer.nvidia.com/cuda-downloads
   - Installa CUDA 11.8 o superiore

2. **Verifica variabili d'ambiente:**
   ```powershell
   $env:CUDA_VISIBLE_DEVICES = "0"
   ```

3. **Riavvia Ollama:**
   ```powershell
   # Chiudi Ollama
   Get-Process ollama | Stop-Process
   
   # Riavvia
   ollama serve
   ```

---

## 🔍 Verifica Utilizzo GPU

### Task Manager Windows

1. Apri Task Manager (CTRL+SHIFT+ESC)
2. Vai su tab "Performance"
3. Seleziona "GPU"
4. Quando generi spiegazioni AI, vedrai utilizzo GPU

### PowerShell

```powershell
# Monitora GPU NVIDIA
nvidia-smi -l 1

# Oppure usa GPU-Z o MSI Afterburner
```

---

## ⚡ Vantaggi GPU

### Con GPU:
- ✅ **10-50x più veloce** per inferenza AI
- ✅ Generazione spiegazioni: ~1-2 secondi (invece di 10-30s)
- ✅ CPU libera per altre operazioni
- ✅ Migliore esperienza utente

### Senza GPU (CPU):
- ⚠️ Più lento ma funziona comunque
- ⚠️ Generazione: ~5-15 secondi
- ✅ Nessuna configurazione necessaria

---

## 🛠️ Troubleshooting

### Ollama non usa GPU?

1. **Verifica CUDA:**
   ```powershell
   nvidia-smi
   ```

2. **Verifica modelli Ollama:**
   ```powershell
   ollama list
   # Alcuni modelli potrebbero non supportare GPU
   ```

3. **Prova modello più piccolo:**
   ```powershell
   ollama pull gemma3:1b
   # Modelli più piccoli funzionano meglio su GPU
   ```

### PyTorch non rileva GPU?

1. **Installa PyTorch con CUDA:**
   ```powershell
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Verifica installazione:**
   ```python
   import torch
   print(torch.cuda.is_available())
   ```

---

## 📊 Performance Attese

### Con GPU NVIDIA:
- **Ollama**: 1-3 secondi per spiegazione
- **PyTorch T5/GPT-2**: 2-5 secondi per spiegazione
- **Utilizzo GPU**: 30-70% durante generazione

### Senza GPU (CPU):
- **Ollama**: 5-15 secondi per spiegazione
- **PyTorch T5/GPT-2**: 10-30 secondi per spiegazione
- **Utilizzo CPU**: 50-100% durante generazione

---

## ✅ Checklist

- [ ] GPU NVIDIA installata
- [ ] Driver NVIDIA aggiornati
- [ ] CUDA Toolkit installato (opzionale, Ollama lo gestisce)
- [ ] Ollama rileva GPU automaticamente
- [ ] PyTorch con CUDA (se usi AI Locale)
- [ ] Test generazione spiegazione con GPU attiva

---

## 🎯 Risultato

Se tutto è configurato correttamente:
- ✅ Ollama userà GPU automaticamente
- ✅ PyTorch userà GPU se disponibile
- ✅ Generazione spiegazioni 10-50x più veloce
- ✅ Esperienza utente molto migliore!

