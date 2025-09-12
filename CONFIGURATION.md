# Configuration Guide

## 🔐 Setting Up Your Databricks Token

The PDF Document Explorer requires a Databricks API token for semantic search functionality. Follow these steps to configure it securely:

### 1. Get Your Databricks Token

1. Log into your Databricks workspace
2. Go to **User Settings** → **Access Tokens**
3. Click **Generate New Token**
4. Copy the generated token (it starts with `dapi...`)

### 2. Configure the Token

**Option A: Environment Variable (Recommended)**
```bash
export DATABRICKS_TOKEN="your-actual-token-here"
```

**Option B: Configuration File**
1. Copy `config.example.env` to `config.env`
2. Edit `config.env` and replace `your-databricks-token-here` with your actual token
3. Load the configuration before running:
   ```bash
   source config.env
   ```

### 3. Verify Configuration

The applications will automatically detect the token from:
1. `DATABRICKS_TOKEN` environment variable
2. If not found, falls back to placeholder (semantic search won't work)

### 🔒 Security Notes

- **Never commit real tokens to git**
- The placeholder `your-databricks-token-here` is safe to commit
- Add `config.env` to `.gitignore` if you use Option B
- For production deployments, use environment variables

### 🚀 Running with Configuration

**Development:**
```bash
export DATABRICKS_TOKEN="dapi1234567890abcdef"
./builds/build_mac_v2.sh
```

**Production:**
```bash
# Set in your deployment environment
DATABRICKS_TOKEN="dapi1234567890abcdef" ./pdf_explorer_mac_v2.py
```

### 🔧 Troubleshooting

**Issue:** Semantic search returns "Failed to authenticate"
**Solution:** Verify your token is set correctly:
```bash
echo $DATABRICKS_TOKEN
```

**Issue:** Token not being detected
**Solution:** Ensure you've exported the environment variable in the same shell session where you run the application.

### 📝 Default Configuration

- **Databricks URL**: `https://dbc-0619d7f5-0bda.cloud.databricks.com/serving-endpoints/icc-intelligence/invocations`
- **Token Source**: Environment variable `DATABRICKS_TOKEN`
- **Fallback**: `your-databricks-token-here` (non-functional placeholder)
