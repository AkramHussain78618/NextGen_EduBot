
# Student Chatbot AI

An attractive AI student chatbot built using Flask + Wikipedia API.

## Features
- Attractive UI
- Wikipedia-based answers
- Fast response
- Easy GitHub upload
- Easy deployment on Render
- No database required

## Run Locally

### Step 1
Install Python

### Step 2
Install requirements

```bash
pip install -r requirements.txt
```

### Step 3
Run project

```bash
python app.py
```

### Step 4
Open browser

```bash
http://127.0.0.1:5000
```

## Deploy on Render

1. Upload project to GitHub
2. Create Render Web Service
3. Add:
   - Build Command:
   ```bash
   pip install -r requirements.txt
   ```

   - Start Command:
   ```bash
   gunicorn app:app
   ```

4. Deploy

