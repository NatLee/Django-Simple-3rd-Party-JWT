document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const errorContainer = document.getElementById('error-container');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const submitButton = document.activeElement;
    const action = submitButton.value;
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
      let response;
      if (action === 'jwt') {
        response = await jwtLogin(data);
      } else if (action === 'session') {
        response = await sessionLogin(data);
      } else {
        throw new Error('未知的登入方式');
      }

      console.log(response);
      window.location.href = "/api/__hidden_dev_dashboard";
    } catch (error) {
      showError(error.message);
    }
  });
});

async function jwtLogin(data) {
  const response = await fetch("/api/auth/token", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data),
  });

  if (response.status === 401) {
    throw new Error('JWT 登入失敗：用戶名或密碼錯誤');
  } else if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'JWT 登入失敗，請稍後再試');
  }

  const responseData = await response.json();
  localStorage.setItem('refresh_token', responseData.refresh);
  localStorage.setItem('access_token', responseData.access);
  return responseData;
}

async function sessionLogin(data) {
  const response = await fetch("/api/__hidden_dev_dashboard/login", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data),
  });

  if (response.status === 401) {
    throw new Error('Session 登入失敗：用戶名或密碼錯誤');
  } else if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Session 登入失敗，請稍後再試');
  }

  return await response.json();
}

function showError(message) {
  const errorContainer = document.getElementById('error-container');
  errorContainer.textContent = message;
  errorContainer.classList.remove('d-none');
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
