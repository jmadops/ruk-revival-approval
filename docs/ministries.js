/* Source accordion interaction, with explicit accessible state. */
document.querySelectorAll('.rukm-faq-c__question').forEach(button => {
  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(expanded));
    button.parentElement.classList.toggle('active', expanded);
    document.getElementById(button.getAttribute('aria-controls')).hidden = !expanded;
  });
});
