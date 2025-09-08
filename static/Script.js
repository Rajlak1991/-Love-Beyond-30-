document.addEventListener('DOMContentLoaded', () => {
  const signinForm = document.getElementById('signin-form');
  const signupForm = document.getElementById('signup-form');

  // Toggle forms
  document.getElementById('show-signup').addEventListener('click', () => {
    signinForm.style.display = 'none';
    signupForm.style.display = 'block';
  });
  document.getElementById('show-signin').addEventListener('click', () => {
    signupForm.style.display = 'none';
    signinForm.style.display = 'block';
  });

  // Form submission
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;

      try {
        const resp = await fetch(form.action, {
          method: form.method,
          body: new FormData(form),
          credentials: 'same-origin'
        });
        const text = await resp.text();
        showMessage(form, text, resp.ok);

        if (resp.ok) {
          if (text.toLowerCase() === 'admin') window.location.href = '/admin';
          else if (text.toLowerCase() === 'user_form') window.location.href = '/user_form';
          else if (text.toLowerCase().includes('registration successful')) {
            signupForm.style.display = 'none';
            signinForm.style.display = 'block';
            showMessage(signinForm, "Registration successful! Please sign in.", true);
          }
        }
      } catch (err) {
        showMessage(form, 'Network error: ' + err.message, false);
      } finally { if (submitBtn) submitBtn.disabled = false; }
    });
  });

  function showMessage(form, text, ok) {
    let msg = form.querySelector('.message');
    if (!msg) {
      msg = document.createElement('div');
      msg.className = 'message';
      form.appendChild(msg);
    }
    msg.textContent = text;
    msg.classList.toggle('success', !!ok);
    msg.classList.toggle('error', !ok);
  }
});
