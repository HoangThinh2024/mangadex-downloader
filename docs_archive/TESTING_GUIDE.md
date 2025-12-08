# MangaDex Downloader Webapp - v2.0 Testing Guide

## 🚀 Quick Start
```
Server running on: http://localhost:8000
```

---

## ✅ All 7 Features - Testing Checklist

### **1. Search by Manga Title**
- ✅ **Fixed** - Required field removed
- **Test:** 
  - Search tab → Enter "One Piece" → Click Search
  - Expected: Shows results with cover, title, status, ID
  - Pagination: Shows "Previous/Next" buttons when total > 12

### **2. Pagination (Page Navigation)**
- ✅ **Fixed** - All pages now display buttons
- **Test:**
  - Search tab → Enter "of" (returns 13,331 results!)
  - Expected: Page 1, 2, 3... buttons appear
  - Click page 2 → Results change with new offset
  - Try "Next" button → Shows page 2 results

### **3. Display Manga URL/ID**
- ✅ **Fixed** - Shows in search results & details
- **Test:**
  - Search results show "ID: abc12345..." below title
  - Click "View" → Details tab shows full ID at top
  - Copy ID → Can paste to download section

### **4. Directory Selection for Downloads**
- ✅ **Already implemented in v2.0**
- **Test:**
  - Download tab → "Select Download Directory" input
  - Browse or type path
  - Download button uses this directory

### **5. Search by Author**
- ✅ **Fixed** - No longer requires title
- **Test:**
  - Search tab → Leave title empty
  - Enter author "Oda" → Click Search
  - Expected: Returns 2 manga by Oda family authors
  - Try "Araki Hirohiko" → Shows JoJo's series

### **6. Search by Artist**
- ✅ **Fixed** - Works without title
- **Test:**
  - Search tab → Leave title & author empty
  - Enter artist name → Click Search
  - Expected: Returns manga with that artist

### **7. All MangaDex Languages (39 total)**
- ✅ **Fixed** - Full list in dropdown
- **Test:**
  - Search tab → Open "Original Language" dropdown
  - Scroll through: English, Japanese, Chinese, Korean, Spanish, French, German, Italian, Portuguese, Russian, Arabic, Hindi, Thai, Vietnamese, Polish, Ukrainian, Indonesian, Turkish, Bengali, Bulgarian, Catalan, Czech, Welsh, Danish, Dutch, Estonian, Farsi, Finnish, Greek, Hebrew, Hungarian, Japanese (Romanized), Javanese, Kazakh, Khmer, Lao, Lithuanian, Macedonian, Mongolian, Malay
  - Select "Japanese" → Search "Naruto" → Returns original Japanese language manga

---

## 🧪 Test Scenarios

### Scenario A: Find One Piece Author's Manga
1. Search tab
2. Author field: "Oda"
3. Title & Artist: (leave empty)
4. Click Search
5. **Expected:** Shows Oda Minamo's manga (2 results)

### Scenario B: Pagination with Many Results
1. Search tab
2. Title field: "of"
3. Limit: 12 (default)
4. Click Search
5. **Expected:** 
   - "13,331 results total" displayed
   - Page buttons: 1, 2, 3, 4... > (showing first 5 pages)
6. Click page 2
7. **Expected:** New 12 results loaded with offset=12

### Scenario C: View Manga Details
1. Search tab → Search "One Piece"
2. Click "View" on first result
3. Details tab opens automatically
4. **Expected:**
   - Manga ID (UUID format)
   - Title: "ONE PIECE"
   - Status: "ongoing"
   - Authors: Oda Eiichirou
   - Cover image
   - Download chapters button

### Scenario D: Search All Fields Combined
1. Search tab
2. Title: "Demon"
3. Author: (empty)
4. Artist: (empty)
5. Status: "ongoing"
6. Language: "ja" (Japanese)
7. Rating: "safe"
8. Click Search
9. **Expected:** Manga matching all filters

### Scenario E: All Fields Optional
1. Search tab
2. Title: (empty)
3. Author: "Akira"
4. Artist: (empty)
5. Click Search
6. **Expected:** Returns manga by authors named "Akira"
7. Should NOT show error "Title required"

---

## 🔍 Debugging

If you encounter issues:

### No results returned?
- Check API server logs (terminal)
- Verify search parameters sent to API
- Try common titles: "One Piece", "Naruto", "Bleach"

### Pagination buttons not showing?
- Search results must have > 12 total
- Use "of", "the", "and" for large result sets
- Check browser console for JS errors (F12)

### Manga details blank?
- URL should be `/api/manga/{uuid}`
- Check that manga ID is valid UUID format
- Server should return 200 OK status

### Search by author returns 0 results?
- Author search first finds author IDs
- Then queries manga by those IDs
- Not all authors have published manga
- Try "Oda" (55 authors found, 2 have manga)

---

## 📊 API Endpoints (for reference)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/search/manga` | GET | Search with title/author/artist/filters |
| `/api/manga/{id}` | GET | Get manga details |
| `/api/manga/{id}/chapters` | GET | Get chapters list |
| `/api/languages` | GET | Get all 39 language codes |
| `/api/authors` | GET | Search authors |
| `/api/artists` | GET | Search artists |

**Test endpoints in browser:**
```
http://localhost:8000/api/search/manga?title=One%20Piece&limit=5
http://localhost:8000/api/search/manga?authors=Oda&limit=5
http://localhost:8000/api/languages
```

---

## ✨ What's New in v2.0

| Feature | Before | After |
|---------|--------|-------|
| Search | Title only, required | Title/Author/Artist, all optional |
| Pagination | None (only 12 results) | Full pagination with page buttons |
| ID Display | None | Shows in search & details |
| Directory | Not implemented | Full path selection |
| Languages | 4 hardcoded | All 39 MangaDex languages |
| Author Search | Not available | Search by author/artist name |

---

## 🎯 Success Criteria

✅ All 7 features working  
✅ No required fields on search  
✅ Pagination shows pages 2+  
✅ Author/artist search functional  
✅ Details endpoint returns data  
✅ 39 languages in dropdown  
✅ No console errors  

---

**Questions? Check browser console (F12) for detailed error messages.**
