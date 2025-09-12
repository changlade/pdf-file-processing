# 🛡️ macOS Security Warning - User Guide

## 🚨 **Getting a Security Warning?**

If you see this message when trying to open the PDF Document Explorer:

> **"Apple could not verify "PDF Document Explorer" is free of malware that may harm your Mac or compromise your privacy."**

**Don't worry!** This is a standard macOS security warning for apps that aren't distributed through the App Store. The app is completely safe.

## ✅ **How to Open the App (Method 1 - Recommended)**

### Step 1: Right-Click Instead of Double-Click
- **Right-click** (or Control+click) on `PDF Document Explorer.app`
- Select **"Open"** from the menu

### Step 2: Confirm in Security Dialog
- A dialog will appear asking if you want to open the app
- Click **"Open"** to confirm
- The app will launch normally

### Step 3: Future Usage
- After doing this once, you can double-click the app normally
- macOS remembers your choice and won't show the warning again

## 🔧 **Alternative Method (System Preferences)**

If the right-click method doesn't work:

### Step 1: Try to Open the App
- Double-click the app (this will show the security warning)
- Click **"Cancel"** in the warning dialog

### Step 2: Go to System Preferences
- Open **System Preferences** (Apple menu → System Preferences)
- Click **"Security & Privacy"**
- Click the **"General"** tab

### Step 3: Allow the App
- You'll see a message about "PDF Document Explorer" being blocked
- Click **"Open Anyway"** next to this message
- Enter your password if prompted
- Click **"Open"** in the confirmation dialog

## 🎯 **For Very Old Macs (macOS 10.9-10.12)**

If you're using a very old Mac, the interface might look slightly different:

### macOS 10.9-10.11:
- Go to **System Preferences → Security & Privacy**
- Under **"Allow apps downloaded from:"**
- Select **"Anywhere"** (you may need to click the lock icon first)
- Try opening the app again

### macOS 10.12:
- Follow the same steps as newer versions
- The "Open Anyway" button should appear in Security & Privacy

## ❓ **Why Does This Happen?**

- macOS has a security feature called **Gatekeeper**
- It only trusts apps that are:
  - Downloaded from the App Store, OR
  - Signed with an Apple Developer certificate
- Since this is a custom app, it shows a warning first
- This is normal and doesn't mean the app is dangerous

## 🛡️ **Is the App Safe?**

**Yes, absolutely!** The PDF Document Explorer:
- ✅ Only processes PDF files locally on your Mac
- ✅ Runs a simple web server for the interface
- ✅ Doesn't connect to the internet (except for the PDF.js library)
- ✅ Doesn't access any personal files outside its folder
- ✅ Doesn't install anything on your system
- ✅ Is completely self-contained

## 📞 **Need Help?**

If you're still having trouble:
1. Make sure you downloaded the `.app` file completely
2. Check that the file isn't corrupted (download again if needed)
3. Try restarting your Mac and opening the app again
4. Contact the person who sent you the app for assistance

## 🎉 **Once It's Working**

After successfully opening the app:
- Your browser will open automatically
- You'll see the PDF Document Explorer interface
- You can browse and search through PDF documents
- No further security warnings will appear

The app works completely offline and is designed to be safe and user-friendly on older Mac systems!
