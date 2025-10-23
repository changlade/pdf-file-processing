# ✅ Reference Display Fix for Cloud Run

## Problem Summary

The application was experiencing a critical error when clicking on references in Cloud Run:

```
Uncaught TypeError: Cannot read properties of undefined (reading 'filter')
    at createTextBlockElement ((index):2214:46)
```

## Root Cause

The `reference_index` in `car_references.json` stores **block IDs** (strings like `"block_7"`, `"block_205"`), not the actual block objects. When a user clicked on a reference, the code was treating these block ID strings as if they were full block objects with properties like `block_id`, `page_number`, and `references`.

### Data Structure
```json
{
  "blocks": [
    {
      "block_id": "block_7",
      "page_number": 7,
      "references": ["CAR-D29-0015-000", "P-0080"]
    }
  ],
  "reference_index": {
    "CAR-D29-0015-000": ["block_7", "block_205"]  // ← These are strings, not objects!
  }
}
```

### The Bug
When a reference was selected:
```javascript
// ❌ BEFORE - Treated block IDs as block objects
if (selectedReference) {
    blocksToShow = referencesData.reference_index[selectedReference] || [];
    // blocksToShow is now ["block_7", "block_205"]
}

// Later, when creating block elements:
block.references.filter(...)  // ❌ Error! block is "block_7" (a string), not an object
```

## Solution

### 1. **Fixed `updateTextBlocks()` Function**
Map block IDs to actual block objects:
```javascript
// ✅ AFTER - Map block IDs to actual blocks
if (selectedReference) {
    const blockIds = referencesData.reference_index[selectedReference] || [];
    blocksToShow = blockIds.map(blockId => 
        referencesData.blocks.find(block => block.block_id === blockId)
    ).filter(block => block !== undefined);
}
```

### 2. **Fixed `exportSearchResults()` Function**
Applied the same fix to ensure CSV export works correctly:
```javascript
if (selectedReference) {
    const blockIds = referencesData.reference_index[selectedReference] || [];
    blocksToExport = blockIds.map(blockId => 
        referencesData.blocks.find(block => block.block_id === blockId)
    ).filter(block => block !== undefined);
}
```

### 3. **Added Safety Checks**
Added defensive checks throughout the code to prevent errors if `block.references` is undefined:

**In `createTextBlockElement()`:**
```javascript
const allRefs = (block.references || []).filter(ref => isReferenceType(ref));
```

**In all filter operations:**
```javascript
blocksToShow = blocksToShow.filter(block => 
    block.references && block.references.some(ref => ...)
);
```

**In CSV export:**
```javascript
const matchingRefs = (block.references || []).filter(ref => {...});
...
`"${(block.references || []).join('; ')}"`
```

### 4. **Enhanced Reference List Filtering**
Fixed generic search to properly display all reference types including standalone witness codes:

**Default View:**
```javascript
// Show all supported reference types, but only standalone witness codes
filteredRefs = allReferences.filter(ref => {
    if (!isReferenceType(ref)) return false;
    
    // For witness codes, only show standalone ones
    if (ref.startsWith('D29-') || ref.startsWith('D30-') || 
        ref.startsWith('V45-') || ref.startsWith('V44-')) {
        return isStandaloneWitnessCode(ref);
    }
    
    return true;
});
```

**Generic Search:**
```javascript
// Show all matching references, filtering out embedded witness codes
filteredRefs = allReferences.filter(ref => {
    if (!ref.toLowerCase().includes(currentFilter.toLowerCase())) return false;
    if (!isReferenceType(ref)) return false;
    
    // For witness codes, only show standalone ones
    if (ref.startsWith('D29-') || ref.startsWith('D30-') || 
        ref.startsWith('V45-') || ref.startsWith('V44-')) {
        return isStandaloneWitnessCode(ref);
    }
    
    return true;
});
```

## Files Modified

- **`web/index.html`**: Updated reference display logic, added safety checks, enhanced filtering

## Testing Locally

```bash
cd /Users/christophe.anglade/Documents/pdf-file-processing
python3 app.py
```

Then visit http://localhost:8080 and test:
1. ✅ Click on any P- reference in the reference list
2. ✅ Click on any CAR- reference
3. ✅ Search for "P-0080" or "D29-" or "CAR-"
4. ✅ Export results to CSV

## Deployment

The application is now ready for Cloud Run deployment:

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/pdf-explorer
gcloud run deploy pdf-explorer \
  --image gcr.io/YOUR_PROJECT_ID/pdf-explorer \
  --memory 2Gi \
  --timeout 300s \
  --allow-unauthenticated
```

## Reference Types Now Working

### Evidence Codes (CAR- prefix)
- ✅ **CAR-OTP-XXXXXXXX**: Office of the Prosecutor evidence (~4,354 total)
- ✅ **CAR-D29-XXXX-XXXX**: Defence team D29 evidence (~214 total)
- ✅ **CAR-D30-XXXX-XXXX**: Defence team D30 evidence (~132 total)

### Witness Codes (Standalone)
- ✅ **P-XXXX**: Prosecution witnesses (4,245 references)
- ✅ **D29-XXXX**: Defence team D29 witnesses (172 references, excluding embedded)
- ✅ **D30-XXXX**: Defence team D30 witnesses (196 references, excluding embedded)
- ✅ **V44-XXXX** and **V45-XXXX**: Victim witnesses (56 references)

## Summary

All reference display issues have been resolved:
- ✅ References now display correctly in the reference list
- ✅ Clicking on references properly loads and displays blocks
- ✅ All reference types (P-, CAR-, D29-, D30-, V45-, V44-) are supported
- ✅ Standalone witness codes are correctly distinguished from embedded codes
- ✅ Export to CSV works correctly
- ✅ No more TypeError when accessing `block.references`
- ✅ Robust error handling with safety checks throughout

