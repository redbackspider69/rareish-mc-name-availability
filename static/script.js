function updateStatus() {
  fetch('/status')
    .then(res => res.json())
    .then(data => {
      const status = document.getElementById('status');
      if (data.current) {
        status.textContent = "Currently checking: " + data.current;
      } else {
        status.textContent = "Status: Idle";
      }
    });
}

function updateUsernames() {
  fetch('/usernames')
    .then(res => res.json())
    .then(data => {
      document.getElementById('results').innerText = data.available_usernames.join(', ');
      document.getElementById('lost').innerText = data.lost_usernames.join(', ');
      document.getElementById('other').innerText = data.other_usernames.join(', ');
      document.getElementById('error').innerText = data.error_usernames.join(', ');
      document.getElementById('taken').innerText = data.taken_usernames.join(', ');
    });
}

function startChecking() {
  fetch('/start', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      alert("Start status: " + data.status);
    });
}

function stopChecking() {
  fetch('/stop', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      alert("Stop status: " + data.status);
    });
}

function resetChecker() {
  fetch('/reset', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      alert("Reset status: " + data.status);
      document.getElementById('results').innerText = '';
      document.getElementById('lost').innerText = '';
      document.getElementById('other').innerText = '';
      document.getElementById('error').innerText = '';
      document.getElementById('taken').innerText = '';
      document.getElementById('status').innerText = "Status: Idle";
    });
}

setInterval(() => {
  updateStatus();
  updateUsernames();
}, 2000);

window.onload = () => {
  updateStatus();
  updateUsernames();
};