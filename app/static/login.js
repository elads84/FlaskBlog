const submitButton = document.getElementById('submitButton')
const emailInput = document.getElementById('emailInput')
const passwordInput = document.getElementById('passwordInput')

submitButton.disabled = true;
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function toggleButton() {

  if (emailPattern.test(emailInput.value)) {
  emailInput.style.borderColor='green';
  } else {
  emailInput.style.borderColor='red';
  };

  if (passwordInput.value.length >= 4) {
  passwordInput.style.borderColor='green';
  } else {
  passwordInput.style.borderColor='red';
  };

  if (emailInput.value.length > 0 && passwordInput.value.length > 0) {
  submitButton.disabled = false;
  }
  else {
  submitButton.disabled = true;
  }
};

emailInput.addEventListener('input', toggleButton)
passwordInput.addEventListener('input', toggleButton)
