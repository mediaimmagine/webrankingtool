# Quick Google Analytics API Setup (5 Minutes)

Since you already have Google Analytics data, let's get API access quickly!

## 🚀 Fast Track Setup:

### Step 1: Get Your GA4 Property ID (1 minute)

1. Go to: https://analytics.google.com
2. Click: **Admin** (gear icon, bottom left)
3. Under "Property" column, click: **Property Settings**
4. Copy the **Property ID** (looks like: `123456789` or `12345678`)

📝 **Save this number!**

### Step 2: Create Service Account (5 minutes)

1. Go to: https://console.cloud.google.com
2. Create/select project: "Trieste Analytics"
3. **Enable API:**
   - APIs & Services → Library
   - Search: "Google Analytics Data API"
   - Click "Enable"
4. **Create Service Account:**
   - IAM & Admin → Service Accounts
   - Click "+ CREATE SERVICE ACCOUNT"
   - Name: `analytics-reader`
   - Click "CREATE AND CONTINUE"
   - Skip role selection → "CONTINUE" → "DONE"
5. **Create Key:**
   - Click the service account you just created
   - Keys → Add Key → Create new key
   - Type: JSON
   - Click "CREATE"
   - File downloads: Save it as `google_analytics_credentials.json`

### Step 3: Grant Access (1 minute)

1. In the service account page, **copy the email** (looks like: `analytics-reader@project-name.iam.gserviceaccount.com`)
2. Go to: https://analytics.google.com
3. Admin → Property Access Management
4. Click "+"
5. Paste the service account email
6. Role: **Viewer**
7. Uncheck "Notify user"
8. Click "Add"

### Step 4: Save Configuration

Save these in a file called `google_analytics_config.json`:

```json
{
  "property_id": "YOUR_PROPERTY_ID_HERE",
  "credentials_file": "google_analytics_credentials.json"
}
```

## ✅ Done!

Then tell me and I'll test the connection!

