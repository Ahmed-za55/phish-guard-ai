chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    fetch('http://localhost:8000/api/v1/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: tab.url })
    })
    .then(res => res.json())
    .then(data => {
      if (data.is_phishing) {
        chrome.scripting.executeScript({
          target: { tabId: tabId },
          func: () => {
            alert('[PHISHGUARD AI] WARNING: Active phishing vector detected on this page! Quarantine engaged.');
          }
        });
      }
    })
    .catch(err => console.log('PhishGuard Bridge offline:', err));
  }
});