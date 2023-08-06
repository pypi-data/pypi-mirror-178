const onclick = function(event) {
	for (const btn of document.querySelectorAll('div.code-tabs-outer-button')) {
	  console.log(btn.dataset, btn);
    btn.classList.toggle("selected", btn.dataset.id == this.dataset.id);
	}
	for (const book of document.querySelectorAll('div.code-tabs')) {
	  for (const page of book.children) {
	    if (page.hasAttribute('data-id')) {
	      page.classList.toggle('hidden', page.dataset.id != this.dataset.id);
			}
	  }
	}
};

window.addEventListener('load', function() {
  for (const book of document.querySelectorAll('div.code-tabs')) {
    let i = 0;
    let navbar = document.createElement('div');
		navbar.classList.add("code-tabs-menu");
		navbar.innerHTML = "<div class='code-tabs-menu-controls'>•••</div>";
    for (const page of book.children) {
      const button = document.createElement('div');
      if (i == 0) {
        button.classList.add("selected");
      }
      const innerButton = document.createElement('div');
      const rippleButton = document.createElement('div');
      button.appendChild(innerButton);
      button.appendChild(rippleButton);
      page.setAttribute('data-id', i);
			button.setAttribute('data-id', i);
      button.classList.add("code-tabs-outer-button");
      button.onclick = onclick;
      innerButton.innerText = page.getAttribute('data-title');
			innerButton.classList.add("code-tabs-menu-button");
			rippleButton.classList.add("code-tabs-ripple-button");
      page.classList.toggle('hidden', i != 0);
      navbar.appendChild(button);
      ++i;
    }
		book.prepend(navbar);
  }
}, false);
