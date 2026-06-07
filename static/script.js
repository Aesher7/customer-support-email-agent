// Sample emails for testing
const SAMPLE_EMAILS = [
    {
        subject: "Can I return my damaged order?",
        body: "I received my order yesterday but the item arrived damaged. The packaging was ripped open and the product is broken. I would like to return it and get a refund or replacement. Please let me know what I need to do.",
        sender: "customer@example.com"
    },
    {
        subject: "How long does shipping take?",
        body: "Hi, I placed an order yesterday and I'm wondering how long it will take to arrive. I need it by Friday. Also, can you tell me about your shipping options?",
        sender: "john.doe@example.com"
    },
    {
        subject: "Technical issue with the app",
        body: "I'm having trouble logging into the app. I enter my password but it says it's incorrect, but I'm sure it's right. I tried resetting my password but didn't receive an email. Can someone help me access my account?",
        sender: "tech.user@example.com"
    }
];

let currentEmailId = null;

// Page Navigation
function showTestPage() {
    switchPage('testPage');
    updateActiveNav(0);
}

function showInboxPage() {
    switchPage('inboxPage');
    updateActiveNav(1);
    loadInbox();
}

function showStatsPage() {
    switchPage('statsPage');
    updateActiveNav(2);
    loadStats();
}

function switchPage(pageId) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

function updateActiveNav(index) {
    const links = document.querySelectorAll('.nav-links a');
    links.forEach((link, i) => {
        if (i === index) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Load Sample Email
function loadSampleEmail(index) {
    const email = SAMPLE_EMAILS[index - 1];
    document.getElementById('sender').value = email.sender;
    document.getElementById('subject').value = email.subject;
    document.getElementById('body').value = email.body;
}

// Handle Email Form Submission
async function handleSubmit(event) {
    event.preventDefault();

    const sender = document.getElementById('sender').value;
    const recipient = document.getElementById('recipient').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value;

    const submitBtn = document.getElementById('submitBtn');
    const resultsSection = document.getElementById('resultsSection');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsContent = document.getElementById('resultsContent');
    const errorContent = document.getElementById('errorContent');

    // Show loading
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing...';
    resultsSection.style.display = 'block';
    loadingIndicator.style.display = 'flex';
    resultsContent.style.display = 'none';
    errorContent.style.display = 'none';

    try {
        const response = await fetch('/api/email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sender,
                recipient,
                subject,
                body
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Error processing email');
        }

        // Store email ID for later
        currentEmailId = data.email_id;

        // Display results
        loadingIndicator.style.display = 'none';
        resultsContent.style.display = 'block';

        document.getElementById('resultIntent').textContent = data.intent.toUpperCase();
        document.getElementById('resultConfidence').textContent = (data.confidence * 100).toFixed(1) + '%';
        document.getElementById('resultStatus').textContent = data.requires_human_review ? '🔄 Pending Review' : '✅ Sent';
        document.getElementById('resultReview').textContent = data.requires_human_review ? 'Yes' : 'No';
        document.getElementById('resultId').textContent = data.email_id;
        document.getElementById('resultResponse').textContent = data.response_body;

    } catch (error) {
        console.error('Error:', error);
        loadingIndicator.style.display = 'none';
        errorContent.style.display = 'block';
        document.getElementById('errorText').textContent = `Error: ${error.message}`;
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Test Email';
    }
}

// Load Inbox
async function loadInbox() {
    const inboxList = document.getElementById('inboxList');

    try {
        const response = await fetch('/api/admin/emails');
        const data = await response.json();

        if (data.emails.length === 0) {
            inboxList.innerHTML = '<div class="loading"><p>No emails yet. Send a test email first!</p></div>';
            return;
        }

        let html = '';
        data.emails.forEach(email => {
            const date = new Date(email.created_at).toLocaleDateString();
            const intentClass = `intent-${email.intent}`;
            html += `
                <div class="email-item" onclick="viewEmailDetail('${email.id}')">
                    <h5>${email.subject}</h5>
                    <div class="email-meta">
                        <span class="email-from">${email.sender}</span>
                        <span class="email-date">${date}</span>
                    </div>
                    <span class="intent-badge ${intentClass}">${email.intent.toUpperCase()}</span>
                </div>
            `;
        });

        inboxList.innerHTML = html;

    } catch (error) {
        console.error('Error loading inbox:', error);
        inboxList.innerHTML = '<div class="error-message"><p>Error loading emails</p></div>';
    }
}

// View Email Detail
async function viewEmailDetail(emailId = null) {
    if (!emailId && !currentEmailId) return;

    const id = emailId || currentEmailId;
    const detailPanel = document.getElementById('emailDetailPanel');
    const detailContent = document.getElementById('emailDetailContent');

    try {
        const response = await fetch(`/api/admin/emails/${id}`);
        const email = await response.json();

        if (email.error) {
            detailContent.innerHTML = '<div class="error-message"><p>' + email.error + '</p></div>';
            detailPanel.style.display = 'block';
            return;
        }

        const html = `
            <div class="email-header">
                <h3>${email.subject}</h3>
                <div class="detail-row">
                    <span class="detail-label">From:</span>
                    <span class="detail-value">${email.sender}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">To:</span>
                    <span class="detail-value">${email.recipient}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Date:</span>
                    <span class="detail-value">${new Date(email.created_at).toLocaleString()}</span>
                </div>
            </div>

            <div style="margin-bottom: 2rem;">
                <h4>Original Message</h4>
                <div style="background: var(--light-color); padding: 1rem; border-radius: 0.375rem; white-space: pre-wrap;">
                    ${email.body}
                </div>
            </div>

            <div style="margin-bottom: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 0.5rem; color: white;">
                <h4 style="color: white;">Processing Results</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                    <div>
                        <p style="opacity: 0.9; margin-bottom: 0.25rem;">Intent</p>
                        <p style="font-size: 1.5rem; font-weight: bold;">${email.intent.toUpperCase()}</p>
                    </div>
                    <div>
                        <p style="opacity: 0.9; margin-bottom: 0.25rem;">Confidence</p>
                        <p style="font-size: 1.5rem; font-weight: bold;">${(email.confidence * 100).toFixed(1)}%</p>
                    </div>
                    <div>
                        <p style="opacity: 0.9; margin-bottom: 0.25rem;">Status</p>
                        <p style="font-size: 1.5rem; font-weight: bold;">${email.status.toUpperCase()}</p>
                    </div>
                    <div>
                        <p style="opacity: 0.9; margin-bottom: 0.25rem;">Requires Review</p>
                        <p style="font-size: 1.5rem; font-weight: bold;">${email.in_review ? 'YES' : 'NO'}</p>
                    </div>
                </div>
            </div>

            <div style="margin-bottom: 2rem;">
                <h4>Generated Response</h4>
                <div style="background: var(--light-color); padding: 1rem; border-radius: 0.375rem; border-left: 4px solid var(--secondary-color); white-space: pre-wrap; line-height: 1.8;">
                    ${email.response || 'No response generated'}
                </div>
            </div>

            ${email.in_review ? `
                <div style="background: #fef08a; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid var(--warning-color);">
                    <h4 style="color: #92400e; margin-bottom: 1rem;">⚠️ Pending Human Review</h4>
                    <p style="color: #b45309;">This email has been flagged for human review.</p>
                    ${email.review_notes ? `<p style="margin-top: 0.5rem; color: #78350f;"><strong>Review Notes:</strong> ${email.review_notes}</p>` : ''}
                </div>
            ` : ''}
        `;

        detailContent.innerHTML = html;
        detailPanel.style.display = 'block';

    } catch (error) {
        console.error('Error loading email detail:', error);
        detailContent.innerHTML = '<div class="error-message"><p>Error loading email details</p></div>';
        detailPanel.style.display = 'block';
    }
}

function closeEmailDetail() {
    document.getElementById('emailDetailPanel').style.display = 'none';
}

// Load Stats
async function loadStats() {
    const statsContent = document.getElementById('statsContent');

    try {
        const response = await fetch('/api/admin/stats');
        const stats = await response.json();

        // Create intent distribution chart
        let intentHtml = '<h5>Intent Distribution</h5><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1rem;">';
        for (const [intent, count] of Object.entries(stats.intent_distribution)) {
            intentHtml += `
                <div style="background: var(--light-color); padding: 1rem; border-radius: 0.375rem; text-align: center;">
                    <div style="font-weight: 600; color: var(--primary-color);">${count}</div>
                    <div style="font-size: 0.875rem; color: #6b7280;">${intent}</div>
                </div>
            `;
        }
        intentHtml += '</div>';

        const html = `
            <div class="stat-card">
                <h4>Total Emails</h4>
                <div class="stat-value">${stats.total_emails}</div>
            </div>

            <div class="stat-card">
                <h4>Sent Emails</h4>
                <div class="stat-value">${stats.sent_emails}</div>
            </div>

            <div class="stat-card">
                <h4>Pending Review</h4>
                <div class="stat-value">${stats.pending_review}</div>
            </div>

            <div style="grid-column: 1 / -1; background: white; padding: 2rem; border-radius: 0.5rem; box-shadow: var(--shadow-lg);">
                ${intentHtml}
            </div>
        `;

        statsContent.innerHTML = html;

    } catch (error) {
        console.error('Error loading stats:', error);
        statsContent.innerHTML = '<div class="error-message"><p>Error loading statistics</p></div>';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load initial stats
    loadStats();
});
