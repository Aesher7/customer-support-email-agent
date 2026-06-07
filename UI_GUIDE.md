# Customer Support Email Agent - UI Guide

## Overview

A modern, responsive web interface for testing and monitoring the customer support email agent system.

## Accessing the UI

Start the server and open your browser:

```bash
uvicorn src.main:app --reload
```

Then navigate to: **http://localhost:8000/**

## Features

### 1. Test Page

**Purpose:** Test the email agent with mock emails

**Features:**
- **Email Composer** - Write test emails with realistic content
- **Sample Templates** - Pre-loaded test scenarios:
  - Sample 1: Damaged item return (complaint)
  - Sample 2: Shipping inquiry
  - Sample 3: Technical support
- **Real-time Processing** - See agent responses immediately
- **Results Display:**
  - Intent detected (complaint, inquiry, etc.)
  - Confidence score
  - Processing status
  - Generated response
  - Retrieved knowledge base documents

**How to Use:**
1. Click the **Test** tab
2. Fill in the email form or load a sample
3. Click **"Send Test Email"**
4. View processing results
5. Click **"View in Inbox"** to see more details

### 2. Inbox Page

**Purpose:** View all processed emails and their details

**Layout:**
- **Left Panel** - Email list
  - Shows 50 most recent emails
  - Click any email to view details
  - Displays:
    - Subject
    - Sender
    - Date
    - Intent category with color coding

- **Right Panel** - Email details
  - Original message
  - Processing results (intent, confidence, status)
  - Generated response
  - Review status (if flagged)
  - All metadata

**How to Use:**
1. Click the **Inbox** tab
2. Emails load automatically
3. Click any email to see full details
4. Click "Back" to return to list

### 3. Stats Page

**Purpose:** Monitor system performance and metrics

**Metrics Displayed:**
- **Total Emails** - Total emails processed
- **Sent Emails** - Emails successfully sent to customers
- **Pending Review** - Emails awaiting human review
- **Intent Distribution** - Breakdown of email types (complaints, inquiries, etc.)

**How to Use:**
1. Click the **Stats** tab
2. View metrics in real-time
3. Monitor intent distribution

## Email Processing Flow (Visible in UI)

```
1. Submit Test Email
        ↓
2. Agent Processing (Loading spinner)
        ↓
3. Results Display:
   ├─ Intent Classification
   ├─ Confidence Score
   ├─ Generated Response
   ├─ Knowledge Base Documents Retrieved
   └─ Status (Sent/Pending Review)
        ↓
4. View in Inbox
```

## Intent Color Coding

- **Complaint** - Red (#dc2626)
- **Inquiry** - Blue (#2563eb)
- **Request** - Gray (#6b7280)
- **Feedback** - Amber (#f59e0b)
- **Urgent** - Dark Red (#b91c1c)

## Sample Emails

### Sample 1: Damaged Item (Complaint)
```
From: customer@example.com
Subject: Can I return my damaged order?
Body: I received my order yesterday but the item arrived damaged...
```
**Expected:** Intent = "complaint", Status = "pending_review"

### Sample 2: Shipping (Inquiry)
```
From: john.doe@example.com
Subject: How long does shipping take?
Body: Hi, I placed an order yesterday and I'm wondering...
```
**Expected:** Intent = "inquiry", Status = "sent"

### Sample 3: Technical (Support)
```
From: tech.user@example.com
Subject: Technical issue with the app
Body: I'm having trouble logging into the app...
```
**Expected:** Intent = "inquiry", Status = "sent"

## API Integration

The UI communicates with these endpoints:

```
POST   /api/email              - Process a test email
GET    /api/admin/emails       - Get all emails
GET    /api/admin/emails/{id}  - Get email details
GET    /api/admin/stats        - Get system statistics
GET    /api/admin/review-queue - Get emails pending review
GET    /health                 - Health check
```

## Responsive Design

The UI is fully responsive and works on:
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (< 768px)

## Dark Mode (Coming Soon)

The UI uses light theme by default. Dark mode support can be added by modifying `style.css` variables.

## Performance Notes

- Emails load in groups (50 per page by default)
- Processing typically takes 2-5 seconds
- UI updates in real-time without page refresh

## Keyboard Shortcuts

- **Tab** - Navigate form fields
- **Enter** - Submit email form
- **Click** - View email details

## Troubleshooting

### UI not loading
- Ensure `static/` folder exists with all files
- Check console for CORS errors
- Verify server is running: `http://localhost:8000/docs`

### Emails not appearing in Inbox
- Send a test email first
- Check database is initialized: `python scripts/initialize_faiss.py`
- Verify OpenAI API key in `.env`

### Slow processing
- Check OpenAI API status
- Verify FAISS index is initialized
- Check network connection

## Customization

### Change Sample Emails
Edit `static/script.js` - `SAMPLE_EMAILS` array

### Modify Styling
Edit `static/style.css` - CSS variables at top

### Add New Endpoints
Add routes in `src/api/admin.py`

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## File Structure

```
static/
├── index.html       - Main UI page
├── style.css        - All styling
├── script.js        - All interactivity
└── assets/          - (Future: images, fonts)
```

## Tips & Tricks

1. **Test Different Intents** - Use sample emails to see how different intents are handled
2. **Monitor Review Queue** - Check which emails are flagged for human review
3. **Track Confidence** - Higher confidence scores (>0.8) indicate more reliable classifications
4. **Analyze Knowledge Base** - See which documents are retrieved for each query
5. **Monitor Stats** - Watch intent distribution to understand customer patterns

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Email search/filter
- [ ] Export reports as PDF
- [ ] Real email integration
- [ ] Response editing before sending
- [ ] Batch email processing
- [ ] Analytics dashboard
- [ ] Email templates
