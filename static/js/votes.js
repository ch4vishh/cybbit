// static/js/votes.js
// Intercept vote forms with class "ajax-vote", POST via fetch, update counts in-place.

document.addEventListener('DOMContentLoaded', function () {
  // select all vote forms that should use AJAX
  const forms = document.querySelectorAll('form.ajax-vote');

  forms.forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const url = form.action;
      const formData = new FormData(form);

      // fetch with credentials so cookies/session are sent
      fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest' // lets backend detect AJAX
        },
        credentials: 'same-origin'
      })
      .then(resp => {
        if (!resp.ok) throw new Error('Network response was not ok');
        return resp.json();
      })
      .then(data => {
        if (data && data.post_id !== undefined) {
          const pid = data.post_id;
          // update the upvote/downvote count elements if present
          const upEl = document.querySelector(`#up-${pid}`);
          const downEl = document.querySelector(`#down-${pid}`);

          if (upEl) upEl.textContent = data.upvotes;
          if (downEl) downEl.textContent = data.downvotes;

          // optionally show a small temp message
          // (you can customize; here we briefly flash the form)
          form.classList.add('voted');
          setTimeout(() => form.classList.remove('voted'), 700);
        } else {
          console.warn('Unexpected response', data);
        }
      })
      .catch(err => {
        console.error('Vote request failed', err);
        // optional: show a friendly error to user
        alert('Failed to submit vote. Please refresh the page and try again.');
      });
    });
  });
});