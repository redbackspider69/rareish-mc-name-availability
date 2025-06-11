function fetchUsernames() {
    fetch('/usernames')
      .then(res => res.json())
      .then(data => {
        const list = document.getElementById('usernames');
        list.innerHTML = '';
        data.forEach(name => {
          const li = document.createElement('li');
          li.textContent = name;
          list.appendChild(li);
        });
      });
  }
  
  function fetchStatus() {
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
  
  function startChecker() {
    fetch('/start', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        alert(data.status);
      });
  }
  
  function stopChecker() {
    fetch('/stop', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        alert(data.status);
      });
  }
  
  // Poll every 3 seconds
  setInterval(() => {
    fetchUsernames();
    fetchStatus();
  }, 3000);
  
  fetchUsernames();
  fetchStatus();
  